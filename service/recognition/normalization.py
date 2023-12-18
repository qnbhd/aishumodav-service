from pydub import AudioSegment


def normalize(audio_segment: AudioSegment,
              sample_rate: int = 16_000,
              channels: int = 1,
              sample_width: int = 2) -> AudioSegment:
    return audio_segment.set_frame_rate(sample_rate).set_channels(channels).set_sample_width(sample_width)
