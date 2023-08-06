from typing import Optional

import torch


class PredictionPostprocessor:
    _DEFAULT_THRESHOLD = 0.5

    def __init__(self, thresholds: Optional[torch.Tensor] = None) -> None:
        self._thresholds = thresholds

    def postprocess(self, logits: torch.Tensor) -> torch.Tensor:
        pass
