# Alfred Multiline → Single

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
[![Alfred](https://img.shields.io/badge/Alfred-4%2B%20Powerpack-purple.svg)](https://www.alfredapp.com/)
[![Python](https://img.shields.io/badge/Python-3.9%2B-blue.svg)](https://www.python.org/)
[![CI](https://github.com/revolyw/alfred-multiline-to-single/actions/workflows/ci.yml/badge.svg)](https://github.com/revolyw/alfred-multiline-to-single/actions/workflows/ci.yml)
[![GitHub release](https://img.shields.io/github/v/release/revolyw/alfred-multiline-to-single?include_prereleases)](https://github.com/revolyw/alfred-multiline-to-single/releases)

English · [简体中文](README.md)

An [Alfred](https://www.alfredapp.com/) workflow that joins multiline text into a single line. Use ↑/↓ to pick a wrap and separator mode, then press Enter to copy the result.

## Features

- Reads multiline text from the **clipboard** by default (keyword argument / selection hotkey also supported)
- Pick a wrap/separator mode with ↑↓; define **your own combinations** in Workflow Configuration
- Sensible built-in defaults, for example:

  | Mode | Example |
  | --- | --- |
  | Single quotes + comma | `'apple','banana','cherry'` |
  | Double quotes + comma | `"apple","banana","cherry"` |
  | No wrap + comma / semicolon / colon+space | `apple,banana` · `apple;banana` · `apple: banana` |

- Skips blank lines; escapes wrap characters / backslashes when wrapping
- Copies the result to the clipboard and shows a notification

## Requirements

- macOS
- Alfred 4+ with Powerpack
- Python 3.9+ (`python3` on PATH)

## Install

### From Releases (recommended)

1. Open [Releases](https://github.com/revolyw/alfred-multiline-to-single/releases)
2. Download `Multiline.to.Single.alfredworkflow`
3. Double-click to import into Alfred

### From source

```bash
git clone https://github.com/revolyw/alfred-multiline-to-single.git
cd alfred-multiline-to-single
./package.sh
open "Multiline to Single.alfredworkflow"
```

## Usage

1. Copy multiline text, e.g.

   ```text
   apple
   banana
   cherry
   ```

2. Invoke Alfred and type `m2s`
3. Choose a mode with ↑/↓ and press Enter

Optional: bind the Hotkey object in the workflow (argument = Selection in macOS).

### Configuration

Alfred → Workflows → **Multiline to Single** → `[x]`:

- **Keyword** (default `m2s`)
- **Custom modes** — one mode per line: `WRAPPER||SEPARATOR||optional title`
  - Empty `WRAPPER` = no quotes
  - Escapes: `\s` space, `\t` tab, `\\` backslash
  - Lines starting with `#` are comments; reorder lines to change the result order
- **UI language** (English / Chinese) for auto-generated titles/hints

Example:

```text
'||,||Single quotes + comma
||;||Join with semicolon
||,\s||Comma + space (no quotes)
```

### Community / Gallery

- Alfred forum thread: [Multiline to Single](https://www.alfredforum.com/topic/23902-multiline-to-single-join-lines-with-quotes-separators/)
- Post draft archive: [`docs/FORUM_POST.md`](docs/FORUM_POST.md)

## Development

```bash
python3 -m unittest discover -s tests -v
python3 filter.py
./package.sh
```

## Releasing

Releases follow [SemVer](https://semver.org/). Pushing a `v*` tag runs GitHub Actions ([`.github/workflows/release.yml`](.github/workflows/release.yml)): tests → `./package.sh` → GitHub Release with `Multiline.to.Single.alfredworkflow`.

1. Bump `version` in `info.plist` and update [CHANGELOG.md](CHANGELOG.md)
2. Commit and push to `master`
3. Tag and push:

```bash
git tag -a v1.2.0 -m "v1.2.0: short summary"
git push origin v1.2.0
```

4. Confirm the Release workflow in [Actions](https://github.com/revolyw/alfred-multiline-to-single/actions), then check [Releases](https://github.com/revolyw/alfred-multiline-to-single/releases)

Prefer a new patch/minor tag over force-updating an existing tag. CI builds the installable workflow; local `./package.sh` is for smoke-testing.

## Contributing

See [CONTRIBUTING.md](CONTRIBUTING.md) and [CODE_OF_CONDUCT.md](CODE_OF_CONDUCT.md).

## Security

Please follow [SECURITY.md](SECURITY.md).

## Changelog

See [CHANGELOG.md](CHANGELOG.md).

## License

[MIT](LICENSE)
