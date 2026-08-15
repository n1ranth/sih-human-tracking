from pathlib import Path

import cv2
import numpy as np
import torch
from torch.utils.data import Dataset


CLASS_TO_ID = {
    "stand": 0,
    "walk": 1,
    "run": 2,
}

VIDEO_EXTENSIONS = {
    ".mp4",
    ".avi",
    ".mov",
    ".mkv",
}


class BehaviorDataset(Dataset):
    def __init__(
        self,
        root,
        transform=None,
        num_frames=16,
    ):
        self.root = Path(root)
        self.transform = transform
        self.num_frames = num_frames

        self.samples = []

        for class_name, class_id in CLASS_TO_ID.items():
            class_dir = self.root / class_name

            if not class_dir.exists():
                continue

            for video_path in class_dir.iterdir():
                if video_path.suffix.lower() in VIDEO_EXTENSIONS:
                    self.samples.append(
                        (video_path, class_id)
                    )

        if not self.samples:
            raise RuntimeError(
                f"No videos found in {self.root}"
            )

    def __len__(self):
        return len(self.samples)

    def __getitem__(self, index):
        video_path, label = self.samples[index]

        frames = self._load_video(video_path)

        # NumPy:
        # [T, H, W, C]
        frames = torch.from_numpy(frames)

        # [T, H, W, C] -> [T, C, H, W]
        frames = frames.permute(0, 3, 1, 2)

        if self.transform is not None:
            # Torchvision R3D transform:
            # [T, C, H, W] -> [C, T, H, W]
            frames = self.transform(frames)

        return frames, torch.tensor(
            label,
            dtype=torch.long,
        )

    def _load_video(self, path):
        cap = cv2.VideoCapture(str(path))

        if not cap.isOpened():
            raise RuntimeError(
                f"Could not open video: {path}"
            )

        total_frames = int(
            cap.get(cv2.CAP_PROP_FRAME_COUNT)
        )

        if total_frames <= 0:
            cap.release()

            raise RuntimeError(
                f"Invalid video: {path}"
            )

        indices = torch.linspace(
            0,
            total_frames - 1,
            self.num_frames,
        ).long()

        frames = []

        for index in indices:
            cap.set(
                cv2.CAP_PROP_POS_FRAMES,
                int(index),
            )

            success, frame = cap.read()

            if not success:
                continue

            frame = cv2.cvtColor(
                frame,
                cv2.COLOR_BGR2RGB,
            )

            frames.append(frame)

        cap.release()

        if not frames:
            raise RuntimeError(
                f"Could not read frames: {path}"
            )

        while len(frames) < self.num_frames:
            frames.append(
                frames[-1].copy()
            )

        return np.stack(frames)