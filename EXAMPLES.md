# 🕵️‍♂️ Examples

> [!IMPORTANT]
> For all commands, the **`[the_download_path]`** is optional. If not specified, the video/audio will be saved in the current working directory.

## **1. Show Version:**

Check the current version of `Pyutube`:

```bash
pyutube -v
```

## **2. Download Playlists:**

Eager to grab an entire playlist? Just run:

```bash
pyutube "YOUTUBE_PLAYLIST_LINK" [the_download_path]
```

1. Choose the download format: video or audio.
2. If you select video, pick your desired resolution. For audio, it’ll download everything right away as WAV unless you add `--mp3`! 🔥

The tool will check all available resolutions from the first video in the playlist and download them in that resolution. 👍

## **3. Download Shorts, Videos, or Audio:**

Ready to download a single short, video, or audio track? Use:

```bash
pyutube "YOUTUBE_LINK" OR "SHORT_LINK" [the_download_path]
```

1. Select the format: video or audio.
2. If it’s a video, choose the resolution; otherwise, the audio downloads immediately as WAV unless you add `--mp3`! 🔥

Examples:

```bash
pyutube youtu.be/cMPnY7EuZvo
pyutube https://youtube.com/watch?v=cMPnY7EuZvo
```

## **4. Download Audio Immediately:**

Want to grab just the audio? Run:

```bash
pyutube "YOUTUBE_LINK" OR "SHORT_LINK" [the_download_path] -a
```

Examples:

```bash
pyutube cMPnY7EuZvo -a
pyutube -a youtu.be/cMPnY7EuZvo
pyutube -a --mp3 youtu.be/cMPnY7EuZvo
```

And you’re all set! 🎉

## **5. Download Videos Immediately:**

Need the video fast? Use:

```bash
pyutube <Y"OUTUBE_LINK" OR "SHORT_LINK" [the_download_path] -f
```

1. Choose your desired resolution.

Examples:

```bash
pyutube cMPnY7EuZvo -f
pyutube -f youtu.be/cMPnY7EuZvo
```

Sit back, relax, and enjoy your video! 🎉
