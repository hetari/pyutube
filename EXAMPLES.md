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
```

## Playlist

```bash
pyutube "https://www.youtube.com/playlist?list=PLAYLIST_ID"
```

## Extra yt-dlp Flags
```bash
pyutube "https://www.youtube.com/watch?v=dQw4w9WgXcQ" -- --ignore-errors --write-info-json
```

> [!IMPORTANT]
> **Facing `Sign in to confirm you’re not a bot`, `HTTP Error 403: Forbidden`, or `The page needs to be reloaded`?**
>
> Forward your browser cookies and enable the remote JavaScript challenge solver (`ejs:github`):
>
> ```bash
> pyutube "https://www.youtube.com/watch?v=dQw4w9WgXcQ" -- --cookies-from-browser chrome --remote-components ejs:github
> ```
>
> - Replace `chrome` with your browser (e.g. `firefox`, `brave`, `edge`).
> - Remove any private playlist query parameters (e.g. `?list=LL`) from single video links.
