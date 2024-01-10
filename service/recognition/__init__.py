from .vosk_model import VoskModel
from .model import RecognitionModel

_registry = {
    'VoskModel': VoskModel,
    'vosk': VoskModel,
}


def create_model(model_kind, *args, **kwargs) -> RecognitionModel:
    return _registry[model_kind](*args, **kwargs)
