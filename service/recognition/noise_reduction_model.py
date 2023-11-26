"""
Noise-reduction module
"""

from typing import Any

import torch
from df.enhance import enhance, init_df

from .model import RecognitionModel


class NoiseReductionModel(RecognitionModel):
    """
    Class for noise-reduction model
    """
    def __init__(self):
        self.model = self.load_model()[0]
        self.df_state = self.load_model()[1]

    def load_model(self) -> Any:
        model, df_state, _ = init_df()
        return model, df_state

    def recognize(self, audio: torch.Tensor, **kwargs) -> torch.Tensor:
        """
        Process an audio file to reduce noise
        :param audio: torch.Tensor
        :return: torch.Tensor
        """
        enhanced = enhance(self.model, self.df_state, audio)
        return enhanced



