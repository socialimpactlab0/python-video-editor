"""Unit tests for video_editor.editor using synthetic clips."""

from __future__ import annotations

import os
import tempfile

import numpy as np
import pytest

# Build a tiny synthetic video so tests run without real media files.
try:
    from moviepy.editor import ColorClip, AudioFileClip, CompositeAudioClip
    from moviepy.audio.AudioClip import AudioClip

    MOVIEPY_AVAILABLE = True
except ImportError:
    MOVIEPY_AVAILABLE = False

pytestmark = pytest.mark.skipif(not MOVIEPY_AVAILABLE, reason="moviepy not installed")


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def _make_video(path: str, duration: float = 3.0, fps: int = 10) -> None:
    """Write a small solid-colour video (no audio) to *path*."""
    clip = ColorClip(size=(160, 90), color=(0, 128, 255), duration=duration)
    clip.write_videofile(path, fps=fps, audio=False, logger=None)
    clip.close()


def _make_video_with_audio(path: str, duration: float = 3.0, fps: int = 10) -> None:
    """Write a small video with a synthetic sine-wave audio track."""
    from moviepy.audio.AudioClip import AudioClip
    import numpy as np

    def make_frame_audio(t):
        return np.sin(2 * np.pi * 440 * t) * 0.3

    video = ColorClip(size=(160, 90), color=(255, 0, 0), duration=duration)
    audio = AudioClip(make_frame_audio, duration=duration, fps=44100)
    final = video.set_audio(audio)
    final.write_videofile(path, fps=fps, logger=None)
    final.close()


# ---------------------------------------------------------------------------
# Tests
# ---------------------------------------------------------------------------

class TestTrim:
    def test_basic_trim(self, tmp_path):
        from video_editor import editor

        src = str(tmp_path / "src.mp4")
        out = str(tmp_path / "out.mp4")
        _make_video(src, duration=5.0)

        editor.trim(src, out, start=1.0, end=3.0)

        assert os.path.isfile(out)
        from moviepy.editor import VideoFileClip
        with VideoFileClip(out) as c:
            assert abs(c.duration - 2.0) < 0.2

    def test_trim_to_end(self, tmp_path):
        from video_editor import editor
        from moviepy.editor import VideoFileClip

        src = str(tmp_path / "src.mp4")
        out = str(tmp_path / "out.mp4")
        _make_video(src, duration=4.0)

        editor.trim(src, out, start=2.0, end=None)

        with VideoFileClip(out) as c:
            assert abs(c.duration - 2.0) < 0.2

    def test_invalid_range_raises(self, tmp_path):
        from video_editor import editor

        src = str(tmp_path / "src.mp4")
        out = str(tmp_path / "out.mp4")
        _make_video(src, duration=3.0)

        with pytest.raises(ValueError, match="--start"):
            editor.trim(src, out, start=5.0, end=3.0)


class TestMerge:
    def test_merge_two_clips(self, tmp_path):
        from video_editor import editor
        from moviepy.editor import VideoFileClip

        a = str(tmp_path / "a.mp4")
        b = str(tmp_path / "b.mp4")
        out = str(tmp_path / "out.mp4")
        _make_video(a, duration=2.0)
        _make_video(b, duration=2.0)

        editor.merge([a, b], out)

        with VideoFileClip(out) as c:
            assert abs(c.duration - 4.0) < 0.3


class TestResize:
    def test_resize_by_scale(self, tmp_path):
        from video_editor import editor
        from moviepy.editor import VideoFileClip

        src = str(tmp_path / "src.mp4")
        out = str(tmp_path / "out.mp4")
        _make_video(src, duration=2.0)

        editor.resize(src, out, width=None, height=None, scale=0.5)

        with VideoFileClip(out) as c:
            assert c.size == (80, 45)

    def test_resize_by_dimensions(self, tmp_path):
        from video_editor import editor
        from moviepy.editor import VideoFileClip

        src = str(tmp_path / "src.mp4")
        out = str(tmp_path / "out.mp4")
        _make_video(src, duration=2.0)

        editor.resize(src, out, width=320, height=180, scale=None)

        with VideoFileClip(out) as c:
            assert c.size == (320, 180)

    def test_no_params_raises(self, tmp_path):
        from video_editor import editor

        src = str(tmp_path / "src.mp4")
        out = str(tmp_path / "out.mp4")
        _make_video(src, duration=2.0)

        with pytest.raises(ValueError):
            editor.resize(src, out, width=None, height=None, scale=None)


class TestExtractAudio:
    def test_extract_audio(self, tmp_path):
        from video_editor import editor

        src = str(tmp_path / "src.mp4")
        out = str(tmp_path / "out.mp3")
        _make_video_with_audio(src, duration=2.0)

        editor.extract_audio(src, out)

        assert os.path.isfile(out)
        assert os.path.getsize(out) > 0

    def test_no_audio_raises(self, tmp_path):
        from video_editor import editor

        src = str(tmp_path / "src.mp4")
        out = str(tmp_path / "out.mp3")
        _make_video(src, duration=2.0)  # no audio

        with pytest.raises(ValueError, match="no audio"):
            editor.extract_audio(src, out)


class TestVideoInfo:
    def test_info_keys(self, tmp_path):
        from video_editor import editor

        src = str(tmp_path / "src.mp4")
        _make_video(src, duration=2.0, fps=10)

        info = editor.video_info(src)

        assert "duration" in info
        assert "fps" in info
        assert "size" in info
        assert "has_audio" in info
        assert info["has_audio"] is False
        assert info["size"] == (160, 90)


class TestConvert:
    def test_convert_format(self, tmp_path):
        from video_editor import editor
        from moviepy.editor import VideoFileClip

        src = str(tmp_path / "src.mp4")
        out = str(tmp_path / "out.avi")
        _make_video(src, duration=2.0)

        editor.convert(src, out, fps=None, bitrate=None)

        assert os.path.isfile(out)
        with VideoFileClip(out) as c:
            assert abs(c.duration - 2.0) < 0.3
