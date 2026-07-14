# Alfred Forum Post Draft

Published: https://www.alfredforum.com/topic/23902-multiline-to-single-join-lines-with-quotes-separators/

Originally for: [Share your Workflows](https://www.alfredforum.com/forum/3-share-your-workflows/)

Suggested title: **Multiline to Single — join lines with quotes & separators**

---

Hi everyone,

I built a small workflow that turns multiline text into a single line with selectable quote wrappers and separators — handy for SQL `IN (...)` lists, JSON-ish string arrays, CSV cells, etc.

### Download

Latest release: https://github.com/revolyw/alfred-multiline-to-single/releases/latest

Source: https://github.com/revolyw/alfred-multiline-to-single

### Usage

1. Copy multiline text (or select text and trigger the Hotkey).
2. Type **`m2s`** (configurable).
3. Use ↑↓ to pick a mode and press ↩ — the result is copied to the clipboard.

Example input:

```text
apple
banana
cherry
```

Modes:

- `'apple','banana','cherry'`
- `"apple","banana","cherry"`
- `'apple', 'banana', 'cherry'`
- `"apple", "banana", "cherry"`

Blank lines are skipped. Quotes inside lines are escaped.

### Configuration

In Alfred → Workflows → **Multiline to Single** → `[x]`:

- **Keyword** (default `m2s`)
- **Default mode** (which option appears first)
- **UI language** (English / Chinese)

### Requirements

- macOS
- Alfred 4+ with Powerpack
- System `python3`

Feedback, bug reports, and feature ideas are very welcome. Thanks!

---

## Notes for posting

1. Attach or link the `.alfredworkflow` from the Release page.
2. Add 1–2 screenshots of the Alfred results list (Alfred window only, no wallpaper): https://alfred.app/submit/screenshots/
3. After the post is live, share the forum URL on the GitHub README.
