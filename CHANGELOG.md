# Changelog

## [1.2.0] - 2026-04-30

### Added
- `worker.py` — unified entry point routing to all backends (DeepSeek Pro/Flash, Groq, Ollama)
- `--context-file <path>` — inject file content into prompt so Boss doesn't burn tokens copying code
- `--code-only` — system prompt forcing clean code output (no markdown, no explanations)
- `--output-file <path>` — Worker writes result directly to file; Boss only runs tests, near-zero output tokens

## [1.1.0] - 2026-04-29

### Added
- `.claude-plugin/plugin.json` — installable as a Claude Code plugin
- `workers/` — ready-made Python worker scripts (DeepSeek, Groq, Ollama)
- `examples/EXAMPLES.md` — 6 copy-paste delegation prompt examples
- `setup.sh` — guided install script with automatic path patching
- `CHANGELOG.md`, `.gitignore`
- `.github/ISSUE_TEMPLATE/` — bug report and feature request templates
- Chinese README section

## [1.0.0] - 2026-04-29

### Added
- Initial release: `SKILL.md` with three-tier model, Boss Loop, delegation protocol
- `README.md` with English and Chinese documentation
- `banner.png` hero image
