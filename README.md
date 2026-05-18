# 📹 Pyutube - The Simplest YouTube Downloader CLI

### Enjoying my project? Please show your appreciation by starring it on GitHub! ⭐

<a href="https://deepwiki.com/Hetari/pyutube">
    <img src="https://deepwiki.com/badge.svg" alt="Ask in DeepWiki" />
</a>
<a href="https://github.com/Hetari/pyutube">
  <img src="https://img.shields.io/pypi/v/pyutube.svg?style=flat&label=Version" alt="Version">
</a>
<a href="https://pepy.tech/projects/pyutube">
  <img src="https://static.pepy.tech/badge/pyutube" alt="Downloads">
</a>
<a href="https://pepy.tech/projects/pyutube">
  <img src="https://static.pepy.tech/badge/pyutube/month" alt="Downloads per Month">
</a>
<a href="https://pepy.tech/projects/pyutube">
  <img src="https://static.pepy.tech/badge/pyutube/week" alt="Downloads per Week">
</a>

<br />
<br />

> [!IMPORTANT]
> `ffmpeg` must be available on your `PATH` for video merging and audio conversion.

<a href="https://ibb.co/27wcFYN">
   <img src="https://i.ibb.co/MDbPg56/Screenshot-from-2024-04-08-21-38-02-transformed.png" alt="Pyutube" style="width: 100%;">
</a>

> [!NOTE]
> Have a feature request or bug report? [tell me](https://github.com/Hetari/pyutube/issues/new)

## Why Pyutube?

Pyutube is a small CLI wrapper around `yt-dlp`. It supports videos, shorts, audio-only downloads, and playlists with a simple prompt-driven flow. Video downloads are merged with the best available audio track, and audio downloads are transcoded to WAV by default with an optional MP3 conversion flag.

Because Pyutube delegates downloading to `yt-dlp`, it also inherits standard `yt-dlp` behavior such as:

- Resuming interrupted downloads when a partial file is still available
- Retrying transient network failures according to `yt-dlp`'s defaults
- Selecting the best matching format from the available stream list
- Merging the chosen video stream with the best available audio stream

Pyutube does not expose every `yt-dlp` option directly, but the downloader underneath is still `yt-dlp`, so its normal download handling applies.

## 🛠️ Installation

Make sure [Python](https://www.python.org) is installed:

```bash
python --version
```

If you are developing locally, clone the repository and install the dependencies:

```bash
pip install -r requirements.txt -r requirements-dev.txt
```

To install the published package:

```bash
pip install pyutube
```

> [!TIP]
> If the installation or update does not work, try running the command with the `pip install pyutube --break-system-packages` flag.

Then run `pyutube --help` to confirm the CLI is available.

## 📈 Upgrade

To upgrade the installed package:

```bash
pip install --upgrade pyutube
```

> [!TIP]
> If the installation or update does not work, try running the command with the `pip install --upgrade pyutube --break-system-packages` flag.

## 🚀 Run It

Use either of these commands to view the CLI help:

```bash
pyutube --help
python -m pyutube --help
```

Download a video, short, or playlist with:

```bash
pyutube "YOUTUBE_LINK"
pyutube "YOUTUBE_LINK" "/path/to/save"
```

Common examples:

```bash
pyutube "https://www.youtube.com/watch?v=dQw4w9WgXcQ"
pyutube "https://www.youtube.com/watch?v=dQw4w9WgXcQ" -a
pyutube "https://www.youtube.com/watch?v=dQw4w9WgXcQ" -a --mp3
pyutube "https://www.youtube.com/watch?v=dQw4w9WgXcQ" -f
pyutube "https://www.youtube.com/playlist?list=PLAYLIST_ID"
```

> [!NOTE]
> The URL is required. The path is optional and defaults to the current working directory.

## 👨‍💻 Usage

#### Arguments

| Arguments | Description                                                                                                          |
| --------- | -------------------------------------------------------------------------------------------------------------------- |
| `URL`     | The YouTube URL or video ID. This argument is required.                                                              |
| `PATH`    | The `path` to save the video. Defaults to the current working directory. <span style="color:green">[Optional]</span> |

### Options

| Option                                              | Description                                   |
| --------------------------------------------------- | --------------------------------------------- |
| `-v` <span style="color:cyan">or</span> `--version` | Display the current version number.           |
| `-a` <span style="color:cyan">or</span> `--audio`   | Download audio only as WAV, skipping prompts. |
| `--mp3`                                             | Convert audio downloads to MP3.               |
| `-f` <span style="color:cyan">or</span> `--footage` | Download video only, skipping prompts.        |

## 🛠️ Code Quality

Run these commands to check code health locally:

```bash
python -m compileall pyutube
ruff check pyutube
mypy pyutube
```

The repo also includes a short checklist in [QUALITY.md](QUALITY.md).

## 🕵️‍♂️ Examples

More examples are in [EXAMPLES.md](EXAMPLES.md).

## 🥰 Contributing

Pull requests are welcome. For larger changes, open an issue first and follow the [contributing guidelines](CONTRIBUTING.md).

## 📎 License

This project is licensed under the [MIT License](LICENSE).

## 📸 Screenshots

<!-- for pypi only -->
<div style="text-align: center;">
   <p>Download a video to a specific location</p>
   <a href="https://ibb.co/0JkdkQy">
      <img src="https://i.ibb.co/7yH6Hbt/image1.png" alt="Download video with specify the save location">
   </a>
   <p>Choose what type to download</p>
   <a href="https://ibb.co/Kb6qjmg">
      <img src="https://i.ibb.co/sbjwvt4/image2.png" alt="Chose what type you want to download">
   </a>
   <p>Choose a resolution when downloading video</p>
   <a href="https://ibb.co/7ymCS79">
      <img src="https://i.ibb.co/h8z9gpq/image4.png" alt="Chose what resolution you want to download">
   </a>
   <p>Select playlist items to download</p>
   <a href="https://ibb.co/0qwkQNm">
      <img src="https://i.ibb.co/1ZS3bV7/Screenshot-from-2024-04-11-16-42-29.png" alt="If you download a playlist, you can choose what video you want to download, or even all of them"/>
   </a>
<br /><br />
 <p>Need help? Run <code>pyutube --help</code></p>
  <a href="https://ibb.co/LhT6r3r">
      <img src="https://i.ibb.co/WprF0L0/image5.png" alt="image5">
   </a>
</div>

## ⏳ Todo List

- [x] **Notification System**
- [x] **Auto Update package if new version available**
- [x] **Support Optional Numbering for Downloaded Playlist Videos**
- [x] **Improve code health**
- [x] **Support downloading sounds (WAV by default, MP3 optional)**
- [ ] **Support Subtitles Download**
- [ ] **Support setting for downloading folder**
- [ ] **Download Thumbnails with Videos and Audio**
