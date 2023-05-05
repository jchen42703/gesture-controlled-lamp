import torch
import cv2
import numpy as np

from generate import generate_model
from dataclasses import dataclass

JESTER_LABELS = [
    "Doing other things",
    "Drumming fingers",
    "No gesture",
    "Pulling hand in",
    "Pulling two fingers in",
    "Pushing hand away",
    "Pushing two fingers away",
    "Rolling hand backward",
    "Rolling hand forward",
    "Shaking hand",
    "Sliding two fingers down",
    "Sliding two fingers left",
    "Sliding two fingers right",
    "Sliding two fingers up",
    "Stop sign",
    "Swiping down",
    "Swiping left",
    "Swiping right",
    "Swiping up",
    "Thumbs down",
    "Thumbs up",
    "Turning hand clockwise",
    "Turning hand counterclockwise",
    "Zooming in with full hand",
    "Zooming in with two fingers",
    "Zooming out with full hand",
    "Zooming out with two fingers"
]


@dataclass(init=True)
class ModelConfig:
    n_classes: int
    width_mult: float
    sample_size: int
    model: str
    arch: str
    no_cuda: bool
    pretrain_path: str
    finetune: bool


@dataclass(init=True)
class ShuffleNetConfig(ModelConfig):
    groups: int


def create_mobilenetv2(pretrained_weights_path: str = "/home/joseph/Desktop/jester_mobilenetv2_0.7x_RGB_16_best.pth"):
    cfg = ModelConfig(
        n_classes=27,
        width_mult=0.7,
        sample_size=112,
        model="mobilenetv2",
        arch="mobilenetv2",
        no_cuda=True,
        pretrain_path=pretrained_weights_path,
        finetune=False
    )

    model, _ = generate_model(cfg)
    model.eval()
    return model


def create_shufflenet(pretrained_weights_path: str):
    cfg = ShuffleNetConfig(
        n_classes=27,
        width_mult=0.5,
        sample_size=112,
        model="shufflenet",
        arch="shufflenet",
        no_cuda=True,
        pretrain_path=pretrained_weights_path,
        finetune=False,
        groups=3,
    )

    model, _ = generate_model(cfg)
    model.eval()
    return model


def get_mean(norm_value=255, dataset='activitynet'):
    assert dataset in ['activitynet', 'kinetics']

    if dataset == 'activitynet':
        return [
            114.7748 / norm_value, 107.7354 / norm_value, 99.4750 / norm_value
        ]
    elif dataset == 'kinetics':
        # Kinetics (10 videos for each class)
        return [
            110.63666788 / norm_value, 103.16065604 / norm_value,
            96.29023126 / norm_value
        ]


def preprocess_mobilenetv2_from_cv2(frame, reshape_size=(112, 112)):
    reshaped = cv2.resize(frame, reshape_size).transpose(2, 0, 1)
    frame = cv2.flip(frame, 1)
    return reshaped, frame


def normalize_activitynet(tensor: torch.Tensor, norm_value=1) -> torch.Tensor:
    """Subtract the mean across each channel.

    Args:
        tensor: of shape (sample_duration, 3, x, y)

    Returns:
        tensor of same shape
    """
    mean = torch.Tensor(get_mean(norm_value=norm_value))
    return tensor.sub(mean.view(1, 3, 1, 1))


def preprocess_mobilenetv2_queued(gathered_frames: np.ndarray, norm_value=1) -> torch.Tensor:
    """
    Args:
        gathered_frames: of shape (sample_duration, 3, x, y)
    """
    input_tensor = torch.from_numpy(gathered_frames).div(norm_value).float()
    input_tensor = normalize_activitynet(input_tensor)
    return input_tensor.permute(1, 0, 2, 3).unsqueeze(0)
