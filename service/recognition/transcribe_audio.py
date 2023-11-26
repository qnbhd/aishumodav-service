"""
Transcribe audio to text model module
"""
from typing import Any

import nemo.collections.asr as nemo_asr

from .model import RecognitionModel


class TranscribeAudioModel(RecognitionModel):
    """
    Class for transcribe audio to text model
    """
    def __init__(self, model_path: str):
        self.model = self.load_model(model_path=model_path)

    def load_model(self, model_path: str = 'nvidia/stt_ru_conformer_transducer_large') -> Any:
        """
        Load the transcribing model
        :return: The loaded model.
        """
        model = nemo_asr.models.EncDecCTCModel.from_pretrained(model_path).cuda()
        return model

    def recognize(self, audio_file_path, **kwargs) -> str:
        """
        Process an audio file to transcribe
        :param audio_file_path: The path to the audio file
        :return: str
        """
        transcribe_text = self.model.transcribe(paths2audio_files=audio_file_path, batch_size=4)[0]
        return transcribe_text
