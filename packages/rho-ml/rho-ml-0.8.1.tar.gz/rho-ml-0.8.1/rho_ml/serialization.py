""" Classes responsible for serializing models in order to be stored.
"""
import glob
import logging
import os
import tempfile
import pickle
from typing import Union

import attr

from rho_ml.model_locator import generate_model_locator, \
    find_highest_compatible_version

logger = logging.getLogger(__name__)


@attr.s(auto_attribs=True, frozen=True)
class StoredModel(object):
    """ This stores the bytes of a serialized model, along with the module and
    qualified class name needed to correctly deserialize the model later.

    If the base_class is provided, that is the class which will be imported,
    and then wrapped with class_name as a subclass which differs from base_class
    only in name.  This is useful for the case where the same underlying model
    is used for multiple separate applications. """
    model_bytes: bytes = attr.ib(repr=False)

    def load_model(self) -> 'RhoModel':
        """ Use the instantiated StoredPredictor to load the stored RhoModel
         instance.

         Note: this method should be overridden if the underlying RhoModel
         requires specialized deserialization logic. """
        return pickle.loads(self.model_bytes)

    def to_pickle(self) -> bytes:
        """ Pickle this StoredModel instance and return the byte string """
        return pickle.dumps(self, protocol=4)

    @classmethod
    def from_pickle(cls, stored_bytes: bytes) -> 'StoredModel':
        """ Load a StoredModel from it's pickled bytes
        """
        return pickle.loads(stored_bytes)


class PipelineStorageConfig(object):
    def store(self, model: 'RhoModel'):
        raise NotImplementedError

    def retrieve(self, *args, **kwargs) -> 'RhoModel':
        raise NotImplementedError

    def get_key_from_pattern(self,
                             model_name: str,
                             version_pattern: str) -> str:
        """ Given some pattern of the form 'name-1.2.3', 'name-1.2.*', or
        'name-1.*', etc., return the key that should be """
        raise NotImplementedError


@attr.s(auto_attribs=True)
class LocalModelStorage(PipelineStorageConfig):
    base_path: str = attr.ib(default=None)

    def __attrs_post_init__(self):
        """ Provide default temp directory if no base_path set.
        """
        if not self.base_path:
            self.base_path = tempfile.gettempdir()

    def store(self, model: 'RhoModel'):
        storage_key = generate_model_locator(
            model_name=model.name,
            model_version=model.version_string
        )
        storage_path = os.path.join(self.base_path, storage_key)
        stored_model = model.build_stored_model()
        store_bytes = stored_model.to_pickle()
        with open(storage_path, 'wb') as f:
            f.write(store_bytes)

    def retrieve(self, key: str) -> Union['RhoModel', None]:
        """ Attempt to retrieve model at a path that is stored locally. Return
            the loaded model if found, otherwise None.
        """
        storage_path = os.path.join(self.base_path, key)
        try:
            with open(storage_path, 'rb') as f:
                stored_model = StoredModel.from_pickle(stored_bytes=f.read())
                model = stored_model.load_model()
        except FileNotFoundError:
            return None
        return model

    def get_key_from_pattern(self,
                             model_name: str,
                             version_pattern: str) -> Union[str, None]:
        """ Attempt to find the path to a model that is stored locally. Return
            the full path to key if found, otherwise None.
        """
        search_pattern = generate_model_locator(
            model_name=model_name, model_version=version_pattern)
        search_path = os.path.join(self.base_path, search_pattern)
        local_candidates = glob.glob(search_path)
        result_key = find_highest_compatible_version(
            search_version=version_pattern,
            search_list=local_candidates)
        return result_key
