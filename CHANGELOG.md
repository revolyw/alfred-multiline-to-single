# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

## [1.2.0] - 2026-07-15

### Added

- **Custom modes** Workflow Configuration: define any wrap/separator combinations
  (`WRAPPER||SEPARATOR||optional title`, with `\s` / `\t` escapes)
- Default presets now also include unquoted joins (comma, semicolon, colon+space)

### Changed

- Removed the fixed “Default mode” popup; mode order is controlled by the custom modes list
- Bumped workflow version to 1.2.0

## [1.1.0] - 2026-07-14

### Added

- 256×256 workflow icon (`icon.png`)
- Workflow Configuration: keyword, default mode, UI language (English / Chinese)
- English Alfred Forum post draft in `docs/FORUM_POST.md`

### Changed

- Default result labels are English (switchable to Chinese)
- Preferred mode can be pinned to the top of the result list
- Bumped workflow packaging to include the icon

## [1.0.1] - 2026-07-14

### Fixed

- Published `.alfredworkflow` asset via GitHub Release workflow

## [1.0.0] - 2026-07-14

### Added

- Alfred Script Filter keyword `m2s` to convert multiline text into a single line
- Four wrap/separator modes: `'…'` / `"…"` with `,` or `, `
- Clipboard fallback when Alfred query is empty
- Hotkey trigger that accepts macOS selection
- Copy-to-clipboard output with notification
- Packaging script `package.sh` and unit tests

[Unreleased]: https://github.com/revolyw/alfred-multiline-to-single/compare/v1.2.0...HEAD
[1.2.0]: https://github.com/revolyw/alfred-multiline-to-single/releases/tag/v1.2.0
[1.1.0]: https://github.com/revolyw/alfred-multiline-to-single/releases/tag/v1.1.0
[1.0.1]: https://github.com/revolyw/alfred-multiline-to-single/releases/tag/v1.0.1
[1.0.0]: https://github.com/revolyw/alfred-multiline-to-single/releases/tag/v1.0.0
