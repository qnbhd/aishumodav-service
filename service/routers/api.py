import io

from fastapi import APIRouter, UploadFile
from pydub import AudioSegment
import librosa

router = APIRouter(prefix="/api/v1")


@router.post("/recognize")
async def recognize(audio: UploadFile):
    # Convert the uploaded audio to WAV format
    audio_data = await audio.read()
    audio_segment = AudioSegment.from_file(io.BytesIO(audio_data))
    wav_data = audio_segment.export(format="wav").read()
    # Process the WAV data using librosa
    y, sr = librosa.load(io.BytesIO(wav_data), sr=None)
    return {"length": librosa.get_duration(y=y, sr=sr)}
