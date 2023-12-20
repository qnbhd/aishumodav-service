import abc
import io


class DenoiseModel(metaclass=abc.ABCMeta):
    @abc.abstractmethod
    def denoise(self, audio: io.BytesIO) -> io.BytesIO:
        raise NotImplementedError()
