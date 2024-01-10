from .noisereduce_ import NoiseReduce
from .model import DenoiseModel

_registry = {
    'default': NoiseReduce,
    'nr': NoiseReduce
}


def create_denoiser(model_kind, *args, **kwargs) -> NoiseReduce:
    return _registry[model_kind](*args, **kwargs)
