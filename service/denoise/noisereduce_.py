from scipy.io import wavfile
import noisereduce as nr
import io
from service.denoise.model import DenoiseModel


class NoiseReduce(DenoiseModel):

    def __init__(self, **kwargs):
        super().__init__()

    def denoise(self, audio: io.BytesIO) -> io.BytesIO:
        rate, data = wavfile.read(audio)
        reduced_noise = nr.reduce_noise(y=data, sr=rate)
        audio = io.BytesIO()
        wavfile.write(audio, rate, reduced_noise)
        return audio
