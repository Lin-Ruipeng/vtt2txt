"""VTT to TXT converter module."""

import re

# Regex pattern to match timestamp lines in VTT format
# Pattern: 00:00:00.000 --> 00:00:00.000
TIMESTAMP_PATTERN = re.compile(r"^\d{2}:\d{2}:\d{2}\.\d{3} --> \d{2}:\d{2}:\d{2}\.\d{3}$")


def convert_vtt(content: str) -> str:
    """Convert VTT subtitle content to plain text.

    Args:
        content: The VTT file content as a string.

    Returns:
        Plain text with subtitle blocks joined by newlines.
        Returns empty string if no subtitles found.
    """
    lines = content.split("\n")
    subtitle_blocks = []
    current_block_lines = []
    in_subtitle_block = False

    for line in lines:
        stripped = line.strip()

        # Skip empty lines
        if not stripped:
            continue

        # Skip WEBVTT header (case-sensitive)
        if stripped == "WEBVTT":
            continue

        # Check if line is a timestamp
        if TIMESTAMP_PATTERN.match(stripped):
            # When we hit a new timestamp, save the current block if it has content
            if current_block_lines:
                subtitle_blocks.append("\n".join(current_block_lines))
                current_block_lines = []
            in_subtitle_block = True
            continue

        # Keep subtitle text lines (accumulate in current block)
        if in_subtitle_block:
            current_block_lines.append(stripped)

    # Don't forget the last block
    if current_block_lines:
        subtitle_blocks.append("\n".join(current_block_lines))

    return "\n".join(subtitle_blocks)