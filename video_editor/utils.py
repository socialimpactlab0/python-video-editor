"""Utility helpers for video_editor."""

import os
import sys


SUPPORTED_VIDEO_EXTS = {".mp4", ".avi", ".mov", ".mkv", ".webm", ".flv", ".wmv", ".m4v"}
SUPPORTED_AUDIO_EXTS = {".mp3", ".wav", ".aac", ".ogg", ".flac", ".m4a"}


def validate_input_file(path: str, allowed_exts: set = None) -> None:
    """Raise SystemExit if *path* does not exist or has an unsupported extension."""
    if not os.path.isfile(path):
        print(f"Error: File not found: {path}", file=sys.stderr)
        sys.exit(1)
    if allowed_exts:
        ext = os.path.splitext(path)[1].lower()
        if ext not in allowed_exts:
            print(
                f"Error: Unsupported file type '{ext}'. "
                f"Supported: {', '.join(sorted(allowed_exts))}",
                file=sys.stderr,
            )
            sys.exit(1)


def ensure_output_dir(path: str) -> None:
    """Create parent directories for *path* if they don't exist."""
    parent = os.path.dirname(os.path.abspath(path))
    os.makedirs(parent, exist_ok=True)


def format_duration(seconds: float) -> str:
    """Return a human-readable HH:MM:SS.mmm string."""
    hours = int(seconds // 3600)
    minutes = int((seconds % 3600) // 60)
    secs = seconds % 60
    return f"{hours:02d}:{minutes:02d}:{secs:06.3f}"


def format_size(path: str) -> str:
    """Return file size as a human-readable string."""
    size = os.path.getsize(path)
    for unit in ("B", "KB", "MB", "GB"):
        if size < 1024:
            return f"{size:.1f} {unit}"
        size /= 1024
    return f"{size:.1f} TB"
