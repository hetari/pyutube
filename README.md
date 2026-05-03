# 📹 Pyutube - The Simplest YouTube Downloader CLI

### Enjoying my project? Please show your appreciation by starring it on GitHub! ⭐

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

> [!NOTE]
> Pyutube is built on top of `pytubefix`. If downloads stop working, update it first:
>
> ```bash
> pip install --upgrade pytubefix
> ```

<a href="https://ibb.co/27wcFYN">
   <img src="https://i.ibb.co/MDbPg56/Screenshot-from-2024-04-08-21-38-02-transformed.png" alt="Pyutube" style="width: 100%;">
</a>

> [!NOTE]
> Have a feature request or bug report? [tell me](https://github.com/Hetari/pyutube/issues/new)

## Why Pyutube?

Pyutube is a small CLI wrapper around `pytubefix`. It supports videos, shorts, audio-only downloads, and playlists with a simple prompt-driven flow.

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
pip install pyutube --break-system-packages
```

Then run `pyutube --help` to confirm the CLI is available.

## 📈 Upgrade

To upgrade the installed package:

```bash
pip install --upgrade pyutube --break-system-packages
```

## 🚀 Run It

Use either of these commands to view the CLI help:

```bash
pyutube --help
python -m pyutube --help
```

Download a video, short, or playlist with:

```bash
pyutube download "YOUTUBE_LINK"
pyutube download "YOUTUBE_LINK" "/path/to/save"
```

Common examples:

```bash
pyutube download "https://www.youtube.com/watch?v=dQw4w9WgXcQ"
pyutube download "https://www.youtube.com/watch?v=dQw4w9WgXcQ" -a
pyutube download "https://www.youtube.com/watch?v=dQw4w9WgXcQ" -f
pyutube download "https://www.youtube.com/playlist?list=PLAYLIST_ID"
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

| Option                                              | Description                            |
| --------------------------------------------------- | -------------------------------------- |
| `-v` <span style="color:cyan">or</span> `--version` | Display the current version number.    |
| `-a` <span style="color:cyan">or</span> `--audio`   | Download audio only, skipping prompts. |
| `-f` <span style="color:cyan">or</span> `--footage` | Download video only, skipping prompts. |

## 🧪 Test And Quality

Run these commands to check code health locally:

```bash
python -m compileall pyutube
pytest pyutube/tests -q
ruff check pyutube
mypy pyutube
coverage run -m pytest pyutube/tests -q
coverage report
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
- [ ] **Support downloading sounds (mp3 format not a audio/mp4)**
- [ ] **Support Subtitles Download**
- [ ] **Support setting for downloading folder**
- [ ] **Download Thumbnails with Videos and Audio**
