# vtt2txt

A Python tool to convert Bilibili VTT subtitle files to plain TXT text.

## Features

- Convert VTT subtitle files to plain text format
- Recursively process entire directory structures
- Preserve directory structure in output
- Simple command-line interface
- Batch conversion of multiple files

## Installation

This project uses [uv](https://github.com/astral-sh/uv) for dependency management.

```bash
# Install dependencies
uv sync

# Or install in development mode
uv pip install -e .
```

## Usage

```bash
uv run python -m vtt2txt source_vtt/ target_txt/
```

Arguments:
- `source_vtt/`: Input directory containing VTT files
- `target_txt/`: Output directory for converted TXT files

## How it works

1. The CLI recursively finds all `.vtt` files in the input directory
2. For each VTT file:
   - Reads the file content as UTF-8 text
   - Parses the VTT format, extracting subtitle text blocks
   - Skips WEBVTT headers and timestamp lines
   - Maps the output path preserving directory structure
   - Writes the plain text content to the corresponding TXT file

The converter extracts subtitle text by:
- Identifying timestamp lines (format: `00:00:00.000 --> 00:00:00.000`)
- Accumulating text lines between timestamps
- Joining subtitle blocks with blank lines

## Project Structure

```
vtt2txt/
├── src/
│   └── vtt2txt/
│       ├── __init__.py      # Package init with version
│       ├── __main__.py      # Entry point for python -m vtt2txt
│       ├── cli.py           # CLI argument parsing and file processing
│       ├── converter.py     # VTT to TXT conversion logic
│       └── path_mapper.py   # Path transformation utilities
├── tests/
│   ├── unit/                # Unit tests for individual modules
│   └── integration/         # Integration tests for full conversions
├── source_vtt/              # Sample input directory
├── target_txt/              # Sample output directory
├── pyproject.toml           # Project configuration
└── README.md
```

## Running Tests

```bash
# Run all tests
uv run pytest

# Run with verbose output
uv run pytest -v
```

## Git

This project uses git for local version control. Initialize a repository if needed:

```bash
git init
git add .
git commit -m "Initial commit"
```

## License

MIT License
