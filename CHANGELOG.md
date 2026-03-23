# Changelog

All notable changes to TinyTranslate will be documented here.
Format: [Keep a Changelog](https://keepachangelog.com/en/1.0.0/)
Versioning: [Semantic Versioning](https://semver.org/spec/v2.0.0.html)

## [1.0.1] — 2026-03-23

### Added
- `core/registry.py` — rebuilds context menu from installed packs via `winreg`; called automatically after every language download so new languages appear in the flyout instantly
- Auto-install language model on first use — no error, just downloads and continues
- "Add more languages..." item at bottom of context menu flyout opens Settings
- Language search autocomplete in Settings (50+ languages, filters by name or code)

### Changed
- Context menu flyout is now dynamic — reflects installed packs, not a hardcoded list
- Settings UI simplified: full language names in dropdowns, single contextual "Download pack" button replaces the separate install section
- `LANGUAGES` dict moved to `config.py` as single source of truth
- `_register.ps1` now delegates to `core/registry.py` instead of duplicating logic
- Version bump to 1.0.1

---

## [1.0.0] — 2026-03-22

### Added
- Right-click context menu for `.txt`, `.docx`, `.pdf` files
- Offline translation via Argos Translate (no API key, no cloud)
- Progress window with Catppuccin Mocha theme
- Settings GUI — change source/target language, install new language packs
- Desktop and Start Menu shortcuts to Settings
- `install.ps1` — one-command setup, no admin required (HKCU registry)
- `uninstall.ps1` — clean removal of context menu and shortcuts
- `download_model.py` — CLI tool for adding language packs
- Chunked translation for large files (configurable chunk size)
- Error log at `error.log` for debugging
- Supports 20+ language pairs via Argos Translate package index
