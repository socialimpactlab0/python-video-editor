"""Core video editing functions backed by MoviePy."""

from __future__ import annotations

import os
from typing import List, Optional, Tuple

try:
    # moviepy 1.x
    from moviepy.editor import (
        AudioFileClip,
        ColorClip,
        CompositeAudioClip,
        CompositeVideoClip,
        TextClip,
        VideoFileClip,
        concatenate_videoclips,
    )
except ImportError:
    # moviepy 2.x
    from moviepy import (
        AudioFileClip,
        ColorClip,
        CompositeAudioClip,
        CompositeVideoClip,
        TextClip,
        VideoFileClip,
        concatenate_videoclips,
    )


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def _write(clip, output: str, fps: Optional[int], bitrate: Optional[str]) -> None:
    """Write *clip* to *output* with optional fps / bitrate overrides."""
    kwargs: dict = {"logger": None}
    if fps:
        kwargs["fps"] = fps
    if bitrate:
        kwargs["bitrate"] = bitrate
    clip.write_videofile(output, **kwargs)


# ---------------------------------------------------------------------------
# Editing operations
# ---------------------------------------------------------------------------

def trim(input_path: str, output_path: str, start: float, end: Optional[float]) -> None:
    """Trim *input_path* from *start* to *end* seconds."""
    with VideoFileClip(input_path) as clip:
        t_end = end if end is not None else clip.duration
        if start >= t_end:
            raise ValueError(
                f"--start ({start}s) must be less than --end ({t_end}s)."
            )
        trimmed = clip.subclip(start, t_end)
        _write(trimmed, output_path, fps=None, bitrate=None)


def merge(input_paths: List[str], output_path: str) -> None:
    """Concatenate all clips in *input_paths* into *output_path*."""
    clips = [VideoFileClip(p) for p in input_paths]
    try:
        final = concatenate_videoclips(clips, method="compose")
        _write(final, output_path, fps=None, bitrate=None)
    finally:
        for c in clips:
            c.close()


def resize(
    input_path: str,
    output_path: str,
    width: Optional[int],
    height: Optional[int],
    scale: Optional[float],
) -> None:
    """Resize video by explicit dimensions or a scale factor."""
    with VideoFileClip(input_path) as clip:
        if scale is not None:
            resized = clip.resize(scale)
        elif width and height:
            resized = clip.resize((width, height))
        elif width:
            resized = clip.resize(width=width)
        elif height:
            resized = clip.resize(height=height)
        else:
            raise ValueError("Provide --scale, --width, or --height.")
        _write(resized, output_path, fps=None, bitrate=None)


def add_text(
    input_path: str,
    output_path: str,
    text: str,
    start: float,
    end: Optional[float],
    position: str,
    fontsize: int,
    color: str,
    font: str,
) -> None:
    """Overlay *text* on the video between *start* and *end* seconds."""
    position_map = {
        "center": "center",
        "top": ("center", "top"),
        "bottom": ("center", "bottom"),
        "top-left": ("left", "top"),
        "top-right": ("right", "top"),
        "bottom-left": ("left", "bottom"),
        "bottom-right": ("right", "bottom"),
    }
    pos = position_map.get(position, "center")

    with VideoFileClip(input_path) as clip:
        t_end = end if end is not None else clip.duration
        txt_clip = (
            TextClip(text, fontsize=fontsize, color=color, font=font)
            .set_position(pos)
            .set_start(start)
            .set_end(t_end)
        )
        final = CompositeVideoClip([clip, txt_clip])
        _write(final, output_path, fps=None, bitrate=None)


def extract_audio(input_path: str, output_path: str) -> None:
    """Extract the audio track from *input_path* and save to *output_path*."""
    with VideoFileClip(input_path) as clip:
        if clip.audio is None:
            raise ValueError("The video has no audio track.")
        clip.audio.write_audiofile(output_path, logger=None)


def add_audio(
    input_path: str,
    audio_path: str,
    output_path: str,
    mix: bool,
    audio_volume: float,
) -> None:
    """Replace or mix the audio track of *input_path* with *audio_path*."""
    with VideoFileClip(input_path) as clip:
        new_audio = AudioFileClip(audio_path).volumex(audio_volume)
        # Trim new audio to video length if needed
        if new_audio.duration > clip.duration:
            new_audio = new_audio.subclip(0, clip.duration)

        if mix and clip.audio is not None:
            combined = CompositeAudioClip([clip.audio, new_audio])
            final = clip.set_audio(combined)
        else:
            final = clip.set_audio(new_audio)

        _write(final, output_path, fps=None, bitrate=None)


def change_speed(input_path: str, output_path: str, factor: float) -> None:
    """Speed up or slow down the video by *factor*."""
    if factor <= 0:
        raise ValueError("--factor must be greater than 0.")
    with VideoFileClip(input_path) as clip:
        sped = clip.fx(__import__("moviepy.effects", fromlist=["vfx"]).vfx.speedx, factor)
        _write(sped, output_path, fps=None, bitrate=None)


def convert(
    input_path: str,
    output_path: str,
    fps: Optional[int],
    bitrate: Optional[str],
) -> None:
    """Re-encode *input_path* to *output_path* (format inferred from extension)."""
    with VideoFileClip(input_path) as clip:
        _write(clip, output_path, fps=fps, bitrate=bitrate)


def video_info(input_path: str) -> dict:
    """Return a dict of metadata for *input_path*."""
    with VideoFileClip(input_path) as clip:
        return {
            "duration": clip.duration,
            "fps": clip.fps,
            "size": clip.size,
            "has_audio": clip.audio is not None,
        }
