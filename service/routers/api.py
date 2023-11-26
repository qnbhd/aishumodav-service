import base64
import io
import json
import tempfile

import librosa
from fastapi import APIRouter, Depends, UploadFile
from fastapi.responses import StreamingResponse
from pydub import AudioSegment
from df.enhance import load_audio, save_audio

from service.recognition.model import RecognitionModel
from service.recognition.vosk_model import VoskModel
from service.recognition.noise_reduction_model import NoiseReductionModel
from service.recognition.transcription_model import TranscriptionModel

router = APIRouter(prefix="/api/v1")


@router.post("/recognize")
async def recognize(
    audio: UploadFile,
    model: RecognitionModel = Depends(lambda: VoskModel()),
    denoise_model: RecognitionModel = Depends(lambda: NoiseReductionModel()),
    transcription_model: RecognitionModel = Depends(lambda: TranscriptionModel()),
):
    # Convert the uploaded audio to WAV format
    audio_data = await audio.read()
    audio_segment = AudioSegment.from_file(io.BytesIO(audio_data))
    wav_data = audio_segment.export(format="wav").read()
    # Process the WAV data using librosa
    y, sr = librosa.load(io.BytesIO(wav_data), sr=None)

    # Calculate the duration of the audio
    duration = librosa.get_duration(y=y, sr=sr)

    # Create a torch.Tensor from the audio data
    audio_tensor = load_audio(io.BytesIO(wav_data), sr=sr)

    # Noise reduction
    audio_tensor = denoise_model.recognize(audio_tensor)
    # Save the audio to temporary file
    with tempfile.NamedTemporaryFile(delete=False, suffix='.waw') as tmp_file:
        cleaned_audio_path = tmp_file.name
        save_audio(audio_tensor, cleaned_audio_path, sr=sr)

    # Transcription audio
    transcription = transcription_model.recognize(cleaned_audio_path)

    # Create a dictionary with the desired response data
    response_data = {
        "length": duration,
        "additional_info": transcription
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
