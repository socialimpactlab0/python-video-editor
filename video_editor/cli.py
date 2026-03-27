"""Click-based CLI for video_editor."""

from __future__ import annotations

import sys
from typing import Optional

import click

from video_editor import __version__
from video_editor import editor
from video_editor.utils import (
    SUPPORTED_AUDIO_EXTS,
    SUPPORTED_VIDEO_EXTS,
    ensure_output_dir,
    format_duration,
    format_size,
    validate_input_file,
)


# ---------------------------------------------------------------------------
# Root group
# ---------------------------------------------------------------------------

@click.group()
@click.version_option(__version__, prog_name="video-editor")
def cli() -> None:
    """Python Video Editor — trim, merge, resize, and more."""


# ---------------------------------------------------------------------------
# trim
# ---------------------------------------------------------------------------

@cli.command()
@click.argument("input", type=click.Path(exists=True))
@click.argument("output")
@click.option("--start", default=0.0, show_default=True, help="Start time in seconds.")
@click.option("--end", default=None, type=float, help="End time in seconds (default: end of video).")
def trim(input: str, output: str, start: float, end: Optional[float]) -> None:
    """Trim INPUT from --start to --end seconds."""
    validate_input_file(input, SUPPORTED_VIDEO_EXTS)
    ensure_output_dir(output)
    click.echo(f"Trimming '{input}' [{start}s – {end or 'end'}s] → '{output}' …")
    try:
        editor.trim(input, output, start, end)
    except ValueError as exc:
        click.echo(f"Error: {exc}", err=True)
        sys.exit(1)
    click.echo(f"Done. Output: {output} ({format_size(output)})")


# ---------------------------------------------------------------------------
# merge
# ---------------------------------------------------------------------------

@cli.command()
@click.argument("output")
@click.argument("inputs", nargs=-1, required=True, type=click.Path(exists=True))
def merge(output: str, inputs: tuple) -> None:
    """Concatenate INPUTS and write to OUTPUT."""
    for f in inputs:
        validate_input_file(f, SUPPORTED_VIDEO_EXTS)
    ensure_output_dir(output)
    click.echo(f"Merging {len(inputs)} clips → '{output}' …")
    editor.merge(list(inputs), output)
    click.echo(f"Done. Output: {output} ({format_size(output)})")


# ---------------------------------------------------------------------------
# resize
# ---------------------------------------------------------------------------

@cli.command()
@click.argument("input", type=click.Path(exists=True))
@click.argument("output")
@click.option("--width", default=None, type=int, help="Target width in pixels.")
@click.option("--height", default=None, type=int, help="Target height in pixels.")
@click.option("--scale", default=None, type=float, help="Scale factor, e.g. 0.5 for 50%.")
def resize(input: str, output: str, width: Optional[int], height: Optional[int], scale: Optional[float]) -> None:
    """Resize INPUT and write to OUTPUT."""
    validate_input_file(input, SUPPORTED_VIDEO_EXTS)
    ensure_output_dir(output)
    if not any([width, height, scale]):
        click.echo("Error: Provide at least one of --width, --height, or --scale.", err=True)
        sys.exit(1)
    click.echo(f"Resizing '{input}' → '{output}' …")
    try:
        editor.resize(input, output, width, height, scale)
    except ValueError as exc:
        click.echo(f"Error: {exc}", err=True)
        sys.exit(1)
    click.echo(f"Done. Output: {output} ({format_size(output)})")


# ---------------------------------------------------------------------------
# add-text
# ---------------------------------------------------------------------------

@cli.command("add-text")
@click.argument("input", type=click.Path(exists=True))
@click.argument("output")
@click.option("--text", required=True, help="Text to overlay.")
@click.option("--start", default=0.0, show_default=True, help="When text appears (seconds).")
@click.option("--end", default=None, type=float, help="When text disappears (default: end of video).")
@click.option(
    "--position",
    default="bottom",
    show_default=True,
    type=click.Choice(["center", "top", "bottom", "top-left", "top-right", "bottom-left", "bottom-right"]),
    help="Text position.",
)
@click.option("--fontsize", default=48, show_default=True, help="Font size in points.")
@click.option("--color", default="white", show_default=True, help="Text color (name or hex).")
@click.option("--font", default="Arial", show_default=True, help="Font name (must be installed).")
def add_text(
    input: str,
    output: str,
    text: str,
    start: float,
    end: Optional[float],
    position: str,
    fontsize: int,
    color: str,
    font: str,
) -> None:
    """Overlay TEXT on INPUT and write to OUTPUT."""
    validate_input_file(input, SUPPORTED_VIDEO_EXTS)
    ensure_output_dir(output)
    click.echo(f"Adding text overlay to '{input}' → '{output}' …")
    editor.add_text(input, output, text, start, end, position, fontsize, color, font)
    click.echo(f"Done. Output: {output} ({format_size(output)})")


# ---------------------------------------------------------------------------
# extract-audio
# ---------------------------------------------------------------------------

@cli.command("extract-audio")
@click.argument("input", type=click.Path(exists=True))
@click.argument("output")
def extract_audio(input: str, output: str) -> None:
    """Extract audio track from INPUT and save to OUTPUT (e.g. .mp3, .wav)."""
    validate_input_file(input, SUPPORTED_VIDEO_EXTS)
    ensure_output_dir(output)
    click.echo(f"Extracting audio from '{input}' → '{output}' …")
    try:
        editor.extract_audio(input, output)
    except ValueError as exc:
        click.echo(f"Error: {exc}", err=True)
        sys.exit(1)
    click.echo(f"Done. Output: {output} ({format_size(output)})")


# ---------------------------------------------------------------------------
# add-audio
# ---------------------------------------------------------------------------

@cli.command("add-audio")
@click.argument("input", type=click.Path(exists=True))
@click.argument("audio", type=click.Path(exists=True))
@click.argument("output")
@click.option("--mix", is_flag=True, default=False, help="Mix new audio with existing track.")
@click.option("--volume", default=1.0, show_default=True, type=float, help="Volume multiplier for new audio.")
def add_audio(input: str, audio: str, output: str, mix: bool, volume: float) -> None:
    """Replace (or mix) audio in INPUT with AUDIO and write to OUTPUT."""
    validate_input_file(input, SUPPORTED_VIDEO_EXTS)
    validate_input_file(audio, SUPPORTED_AUDIO_EXTS)
    ensure_output_dir(output)
    mode = "Mixing" if mix else "Replacing"
    click.echo(f"{mode} audio in '{input}' → '{output}' …")
    editor.add_audio(input, audio, output, mix, volume)
    click.echo(f"Done. Output: {output} ({format_size(output)})")


# ---------------------------------------------------------------------------
# speed
# ---------------------------------------------------------------------------

@cli.command()
@click.argument("input", type=click.Path(exists=True))
@click.argument("output")
@click.option("--factor", required=True, type=float, help="Speed multiplier (e.g. 2.0 = double speed, 0.5 = half speed).")
def speed(input: str, output: str, factor: float) -> None:
    """Change the playback speed of INPUT and write to OUTPUT."""
    validate_input_file(input, SUPPORTED_VIDEO_EXTS)
    ensure_output_dir(output)
    click.echo(f"Changing speed of '{input}' by {factor}x → '{output}' …")
    try:
        editor.change_speed(input, output, factor)
    except ValueError as exc:
        click.echo(f"Error: {exc}", err=True)
        sys.exit(1)
    click.echo(f"Done. Output: {output} ({format_size(output)})")


# ---------------------------------------------------------------------------
# convert
# ---------------------------------------------------------------------------

@cli.command()
@click.argument("input", type=click.Path(exists=True))
@click.argument("output")
@click.option("--fps", default=None, type=int, help="Output frames per second.")
@click.option("--bitrate", default=None, help="Output bitrate, e.g. '2000k'.")
def convert(input: str, output: str, fps: Optional[int], bitrate: Optional[str]) -> None:
    """Re-encode INPUT to OUTPUT (format inferred from file extension)."""
    validate_input_file(input, SUPPORTED_VIDEO_EXTS)
    ensure_output_dir(output)
    click.echo(f"Converting '{input}' → '{output}' …")
    editor.convert(input, output, fps, bitrate)
    click.echo(f"Done. Output: {output} ({format_size(output)})")


# ---------------------------------------------------------------------------
# info
# ---------------------------------------------------------------------------

@cli.command()
@click.argument("input", type=click.Path(exists=True))
def info(input: str) -> None:
    """Show metadata for INPUT video."""
    validate_input_file(input, SUPPORTED_VIDEO_EXTS)
    meta = editor.video_info(input)
    w, h = meta["size"]
    click.echo(f"File     : {input}")
    click.echo(f"Duration : {format_duration(meta['duration'])} ({meta['duration']:.3f}s)")
    click.echo(f"FPS      : {meta['fps']}")
    click.echo(f"Size     : {w} × {h} px")
    click.echo(f"Audio    : {'yes' if meta['has_audio'] else 'no'}")
    click.echo(f"File size: {format_size(input)}")
