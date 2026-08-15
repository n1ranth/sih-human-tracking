import torch.nn as nn
from torchvision.models.video import R3D_18_Weights, r3d_18

NUM_CLASSES = 3


def create_model():
    weights = R3D_18_Weights.DEFAULT

    model = r3d_18(weights=weights)

    # Freeze pretrained backbone initially.
    for param in model.parameters():
        param.requires_grad = False

    # Replace Kinetics-400 classifier.
    model.fc = nn.Linear(
        model.fc.in_features,
        NUM_CLASSES,
    )

    return model, weights
