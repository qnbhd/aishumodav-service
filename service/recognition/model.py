import abc
import io


class RecognitionModel(metaclass=abc.ABCMeta):
    @abc.abstractmethod
    def recognize(self, audio: io.BytesIO) -> str:
        raise NotImplementedError()
