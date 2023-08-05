""" Base class definition for RhoModel

    TODO: more explanation of why that matters

    Definition of StoredModel container class for storage of RhoModel instances.

    A StoredModel needs to contain the data and logic to deserialize the
    underlying RhoModel.  In cases where the RhoModel instance requires
    specialized serialization logic (e.g. when it isn't pickleable), a
    StoredModel subclass should be created.
"""
import pickle
from typing import Any, Callable, Optional, Type, Union, Dict

import attr
from marshmallow import Schema

from rho_ml import Version, StoredModel


class ValidationFailedError(Exception):
    pass


# todo: consider alternate name for Predictor
@attr.s(auto_attribs=True)
class RhoModel(object):
    """ The most basic wrapper for an ML or other model.  Specific models should
    be a subclass of Predictor, and implement whatever appropriate subset of
    abstract methods defined here """
    version: Union[Version, Dict[str, int]]
    name: Optional[str] = None

    def __attrs_post_init__(self):
        """ If attr.asdict is used to help serialize a model, this will
        convert the version back to a Version from dict """
        if isinstance(self.version, dict):
            self.version = Version(**self.version)
        if not self.name:
            self.name = str(self.__class__.__name__)

    @property
    def version_string(self) -> str:
        """ Convenience property to provide the version as a string instead
            of a Version object
        """
        return self.version.to_string()

    @property
    def training_data_schema(self) -> Optional[Type[Schema]]:
        return None

    def validate_training_input(self, data: Any):
        """ Throw a ValidationFailedError if the data is not valid training data """
        raise NotImplementedError

    def validate_training_output(self, data: Any):
        """ Throw a ValidationFailedError if the data is not valid output from the train()
        method. """
        raise NotImplementedError

    def validate_prediction_input(self, data: Any):
        """ Throw a ValidationFailedError if the data is not valid prediction input data """
        raise NotImplementedError

    def validate_prediction_output(self, data: Any):
        """ Throw a ValidationFailedError if the data is not valid prediction output
        data """
        raise NotImplementedError

    def train_logic(self, training_data: Any, *args, **kwargs) -> Any:
        """ This method should be overridden with the appropriate logic to
        take training data, evaluation data, run training, and return
        relevant data (e.g. training and validation metrics for each epoch)."""
        raise NotImplementedError

    def train(self, training_data: Any, run_validation: bool,
              *args, **kwargs) -> Any:
        if run_validation:
            result = get_validated_result(
                model_method=self.train_logic,
                input_data=training_data,
                input_validator=self.validate_training_input,
                output_validator=self.validate_training_output,
                *args, **kwargs)
        else:
            result = self.train_logic(
                training_data=training_data, *args, **kwargs)
        return result

    def predict_logic(self, prediction_data: Any, *args, **kwargs) -> Any:
        """ This method should take a dict containing items with appropriate
        types for the model, and generate outputs with appropriate types."""
        raise NotImplementedError

    def predict(self, prediction_data: Any, run_validation: bool,
                *args, **kwargs) -> Any:
        if run_validation:
            result = get_validated_result(
                model_method=self.predict_logic,
                input_data=prediction_data,
                input_validator=self.validate_prediction_input,
                output_validator=self.validate_prediction_output,
                *args, **kwargs)
        else:
            result = self.predict_logic(
                prediction_data=prediction_data, *args, **kwargs)
        return result

    def serialize(self) -> bytes:
        """ Serialize the predictor object to a byte string.

        Note: this should be overridden if specialized serialization /
        deserialization is required. """
        return pickle.dumps(self, protocol=4)

    @classmethod
    def deserialize(cls, serialized: bytes):
        """ Instantiate a RhoModel object from a serialized byte string

        DEPRECATED: use build_stored_model instead """
        raise NotImplementedError

    def build_stored_model(self) -> StoredModel:
        """ Create a StoredModel object which can be used to properly
        reinstantiate the model later.

        Note: this *must* be implemented to use Sermos serialization utils
        """
        model_bytes = self.serialize()
        stored_model = StoredModel(model_bytes=model_bytes)
        return stored_model

    def save_to_disk(self, path_to_output: str):
        """ Logic to save a single Predictor object to disk."""
        serialized = self.serialize()
        with open(path_to_output, 'wb') as f:
            f.write(serialized)

    @classmethod
    def load_from_disk(cls, path_to_file: str):
        """ Logic to load the Predictor subclass from disk. """
        with open(path_to_file, 'rb') as f:
            loaded = cls.deserialize(f.read())
        return loaded


def get_validated_result(model_method: Callable,
                         input_data: Any,
                         input_validator: Callable[[Any], None],
                         output_validator: Callable[[Any], None],
                         *args, **kwargs) -> Any:
    input_validator(input_data)
    output_data = model_method(input_data, *args, **kwargs)
    output_validator(output_data)
    return output_data
