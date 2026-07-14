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
- Four modes:

  | Mode | Example |
  | --- | --- |
  | Single quotes + comma | `'apple','banana','cherry'` |
  | Double quotes + comma | `"apple","banana","cherry"` |
  | Single quotes + comma+space | `'apple', 'banana', 'cherry'` |
  | Double quotes + comma+space | `"apple", "banana", "cherry"` |

- Skips blank lines and escapes wrap characters / backslashes
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

## Development

```bash
python3 -m unittest discover -s tests -v
python3 filter.py
./package.sh
```

## Contributing

See [CONTRIBUTING.md](CONTRIBUTING.md) and [CODE_OF_CONDUCT.md](CODE_OF_CONDUCT.md).

## Security

Please follow [SECURITY.md](SECURITY.md).

## Changelog

See [CHANGELOG.md](CHANGELOG.md).

## License

[MIT](LICENSE)
