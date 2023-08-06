from typing import Optional

import torch


class PredictionPostprocessor:
    def __init__(self, thresholds: Optional[torch.Tensor] = None, default_threshold: float = 0.5) -> None:
        self._default_threshold = default_threshold
        self._thresholds = thresholds

    def postprocess(self, logits: torch.Tensor) -> torch.Tensor:
        pass
