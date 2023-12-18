import base64
import io
import json
from typing import Any, Dict

import librosa
from fastapi import APIRouter, Depends, UploadFile
from fastapi.responses import StreamingResponse
from pydub import AudioSegment

from service.recognition.model import RecognitionModel
from service.recognition.normalization import normalize
from service.recognition import create_model
from service.config import get_config

router = APIRouter(prefix="/api/v1")


async def get_model(config: Dict[str, Any] = Depends(get_config)):
    return create_model(config["recognition"]["kind"], **config["recognition"])


@router.post("/recognize")
async def recognize(
    audio: UploadFile,
    model: RecognitionModel = Depends(get_model),
):
    # Convert the uploaded audio to WAV format
    audio_data = await audio.read()
    audio_segment = AudioSegment.from_file(io.BytesIO(audio_data))
    audio_segment = normalize(audio_segment)
    wav_data = audio_segment.export(format="wav").read()
    # Process the WAV data using librosa
    y, sr = librosa.load(io.BytesIO(wav_data), sr=None)

    # Calculate the duration of the audio
    duration = librosa.get_duration(y=y, sr=sr)

    # Create a dictionary with the desired response data
    response_data = {
        "length": duration,
        "additional_info": model.recognize(io.BytesIO(wav_data)),
    }

    # Serialize the dictionary to JSON
    response_json = json.dumps(response_data)

    # Create a response with streaming audio and JSON data
    def generate_response():
        # Yield the JSON data
        yield response_json.encode("utf-8")
        yield "\n--boundary\n"
        # Yield the audio data
        yield base64.b64encode(wav_data).decode("utf-8")

    response_headers = {
        "Content-Disposition": "attachment; filename=original_audio.wav",
        "Content-Type": "multipart/mixed; boundary=boundary",
    }

    return StreamingResponse(
        generate_response(),
        media_type="multipart/mixed; boundary=boundary",
        headers=response_headers,
    )
