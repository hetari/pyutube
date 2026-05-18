# Examples

## Video

```bash
pyutube "https://www.youtube.com/watch?v=dQw4w9WgXcQ"
pyutube "https://www.youtube.com/watch?v=dQw4w9WgXcQ" "/downloads"
pyutube "https://www.youtube.com/watch?v=dQw4w9WgXcQ" -f
```

## Audio

```bash
pyutube "https://www.youtube.com/watch?v=dQw4w9WgXcQ" -a
pyutube "https://www.youtube.com/watch?v=dQw4w9WgXcQ" -a --mp3
```

## Playlist

```bash
pyutube "https://www.youtube.com/playlist?list=PLAYLIST_ID"
```

## Extra yt-dlp Flags

```bash
pyutube "https://www.youtube.com/watch?v=dQw4w9WgXcQ" -- --ignore-errors --write-info-json
```
