from pathlib import Path

import torch
import torch.nn as nn
from torch.utils.data import DataLoader, random_split
from tqdm import tqdm

from dataset import BehaviorDataset
from model import create_model

DATASET_ROOT = "datasets/" "CCTV-Action-Recognition-Dataset-Kaggle/" "Videos/" "Videos"

BATCH_SIZE = 2
EPOCHS = 10
LEARNING_RATE = 1e-3

NUM_FRAMES = 16

CHECKPOINT_DIR = Path("checkpoints")


def main():
    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

    print(f"Using device: {device}")

    # --------------------------------------------------------
    # Model
    # --------------------------------------------------------

    model, weights = create_model()

    model = model.to(device)

    # --------------------------------------------------------
    # Dataset
    # --------------------------------------------------------

    dataset = BehaviorDataset(
        DATASET_ROOT,
        transform=weights.transforms(),
        num_frames=NUM_FRAMES,
    )

    print(f"Total videos: {len(dataset)}")

    # 80/20 train/validation split.
    train_size = int(0.8 * len(dataset))
    val_size = len(dataset) - train_size

    train_dataset, val_dataset = random_split(
        dataset,
        [train_size, val_size],
    )

    train_loader = DataLoader(
        train_dataset,
        batch_size=BATCH_SIZE,
        shuffle=True,
        num_workers=2,
    )

    val_loader = DataLoader(
        val_dataset,
        batch_size=BATCH_SIZE,
        shuffle=False,
        num_workers=2,
    )

    # --------------------------------------------------------
    # Optimizer
    # --------------------------------------------------------

    criterion = nn.CrossEntropyLoss()

    optimizer = torch.optim.AdamW(
        model.fc.parameters(),
        lr=LEARNING_RATE,
        weight_decay=1e-4,
    )

    # --------------------------------------------------------
    # Training
    # --------------------------------------------------------

    best_accuracy = 0.0

    CHECKPOINT_DIR.mkdir(
        parents=True,
        exist_ok=True,
    )

    for epoch in range(EPOCHS):

        model.train()

        running_loss = 0.0
        correct = 0
        total = 0

        progress = tqdm(
            train_loader,
            desc=f"Epoch {epoch + 1}/{EPOCHS}",
        )

        for videos, labels in progress:

            videos = videos.to(device)
            labels = labels.to(device)

            optimizer.zero_grad()

            outputs = model(videos)

            loss = criterion(
                outputs,
                labels,
            )

            loss.backward()

            optimizer.step()

            running_loss += loss.item()

            predictions = outputs.argmax(dim=1)

            correct += (predictions == labels).sum().item()

            total += labels.size(0)

            progress.set_postfix(
                loss=loss.item(),
                accuracy=correct / total,
            )

        train_accuracy = correct / total

        # ----------------------------------------------------
        # Validation
        # ----------------------------------------------------

        model.eval()

        correct = 0
        total = 0

        with torch.no_grad():

            for videos, labels in val_loader:

                videos = videos.to(device)
                labels = labels.to(device)

                outputs = model(videos)

                predictions = outputs.argmax(dim=1)

                correct += (predictions == labels).sum().item()

                total += labels.size(0)

        val_accuracy = correct / total

        print(
            f"\n"
            f"Epoch {epoch + 1}/{EPOCHS}\n"
            f"Train accuracy: {train_accuracy:.4f}\n"
            f"Val accuracy:   {val_accuracy:.4f}\n"
        )

        # ----------------------------------------------------
        # Save best model
        # ----------------------------------------------------

        if val_accuracy > best_accuracy:

            best_accuracy = val_accuracy

            torch.save(
                {
                    "model_state_dict": model.state_dict(),
                    "accuracy": val_accuracy,
                },
                CHECKPOINT_DIR / "behavior_best.pth",
            )

            print(f"Saved best model " f"({val_accuracy:.4f})")


if __name__ == "__main__":
    main()
