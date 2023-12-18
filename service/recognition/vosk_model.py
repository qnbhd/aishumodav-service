from __future__ import annotations
import io
import json
import wave

from vosk import KaldiRecognizer, Model

from .model import RecognitionModel


class VoskModel(RecognitionModel):
    def __init__(self, *args, model: Model | str = Model(lang="ru"), buff_size: int = 4000, **kwargs):
        self.vosk_model = model if isinstance(model, Model) else Model(lang=model)
        self.buff_size = buff_size

    def recognize(self, audio: io.BytesIO) -> str:
        with wave.open(audio) as wf:
            rec = KaldiRecognizer(self.vosk_model, wf.getframerate())
            # To store our results
            transcription = []

            while len(data := wf.readframes(self.buff_size)) > 0:
                if rec.AcceptWaveform(data):
                    # Convert json output to dict
                    result_dict = json.loads(rec.Result())
                    # Extract text values and append them to transcription list
                    transcription.append(result_dict.get("text", ""))

            # Get final bits of audio and flush the pipeline
            final_result = json.loads(rec.FinalResult())
            transcription.append(final_result.get("text", ""))

            return " ".join(transcription)
