# Python Video Editor

A command-line video editing tool built with Python and MoviePy.

## Installation

```bash
pip install -r requirements.txt
```

> **Note:** FFmpeg must be installed on your system.
> - macOS: `brew install ffmpeg`
> - Ubuntu/Debian: `sudo apt install ffmpeg`
> - Windows: Download from https://ffmpeg.org/download.html

## Usage

```bash
python -m video_editor <command> [options]
```

### Commands

#### trim — Cut a video clip
```bash
python -m video_editor trim input.mp4 output.mp4 --start 10 --end 30
```

#### merge — Concatenate multiple videos
```bash
python -m video_editor merge output.mp4 clip1.mp4 clip2.mp4 clip3.mp4
```

#### resize — Resize/scale a video
```bash
python -m video_editor resize input.mp4 output.mp4 --width 1280 --height 720
# Scale by percentage (50%)
python -m video_editor resize input.mp4 output.mp4 --scale 0.5
```

#### add-text — Overlay text on video
```bash
python -m video_editor add-text input.mp4 output.mp4 --text "Hello World" \
  --start 2 --end 8 --position bottom --fontsize 48 --color white
```

#### extract-audio — Save audio track to file
```bash
python -m video_editor extract-audio input.mp4 output.mp3
```

#### add-audio — Replace or mix audio
```bash
# Replace audio
python -m video_editor add-audio input.mp4 audio.mp3 output.mp4
# Mix with original audio
python -m video_editor add-audio input.mp4 audio.mp3 output.mp4 --mix
```

#### speed — Change playback speed
```bash
# Double speed
python -m video_editor speed input.mp4 output.mp4 --factor 2.0
# Half speed
python -m video_editor speed input.mp4 output.mp4 --factor 0.5
```

#### convert — Re-encode to a different format/codec
```bash
python -m video_editor convert input.mp4 output.avi
python -m video_editor convert input.mp4 output.mp4 --fps 30 --bitrate 2000k
```

#### info — Show video metadata
```bash
python -m video_editor info input.mp4
```

## Examples

```bash
# Trim, add title text, then extract audio
python -m video_editor trim raw.mp4 trimmed.mp4 --start 5 --end 60
python -m video_editor add-text trimmed.mp4 titled.mp4 --text "My Video" --start 0 --end 3
python -m video_editor extract-audio titled.mp4 audio.mp3
```

## Project Structure

```
python-video-editor/
├── video_editor/
│   ├── __init__.py
│   ├── __main__.py       # Entry point (python -m video_editor)
│   ├── cli.py            # Click CLI definitions
│   ├── editor.py         # Core editing functions
│   └── utils.py          # Helpers (validation, formatting)
├── tests/
│   ├── __init__.py
│   └── test_editor.py
├── requirements.txt
└── README.md
```
