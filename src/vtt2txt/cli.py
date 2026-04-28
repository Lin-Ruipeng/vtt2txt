"""CLI for vtt2txt - Convert VTT subtitle files to plain text."""

import sys
from pathlib import Path

from vtt2txt.converter import convert_vtt
from vtt2txt.path_mapper import map_path


def main() -> int:
    """Main CLI entry point.

    Returns:
        Exit code (0 for success, 1 for error)
    """
    if len(sys.argv) != 3:
        print("Usage: python -m vtt2txt <input_dir> <output_dir>", file=sys.stderr)
        return 1

    input_dir = Path(sys.argv[1])
    output_dir = Path(sys.argv[2])

    # Validate input directory
    if not input_dir.exists():
        print(f"Error: Input directory does not exist: {input_dir}", file=sys.stderr)
        return 1

    if not input_dir.is_dir():
        print(f"Error: Input path is not a directory: {input_dir}", file=sys.stderr)
        return 1

    # Find all VTT files recursively
    vtt_files = list(input_dir.rglob("*.vtt"))

    if not vtt_files:
        print(f"No .vtt files found in {input_dir}", file=sys.stderr)
        return 1

    print(f"Found {len(vtt_files)} VTT file(s) to convert")

    success_count = 0
    error_count = 0

    for vtt_file in vtt_files:
        print(f"Processing: {vtt_file.relative_to(input_dir)}")

        try:
            # Read VTT file
            content = vtt_file.read_text(encoding="utf-8")

            # Convert content
            converted = convert_vtt(content)

            # Map output path
            output_path = map_path(vtt_file, input_dir, output_dir)

            # Create output directory if needed
            output_path.parent.mkdir(parents=True, exist_ok=True)

            # Write converted content
            output_path.write_text(converted, encoding="utf-8")

            success_count += 1

        except FileNotFoundError:
            print(f"  Error: File not found: {vtt_file}", file=sys.stderr)
            error_count += 1
        except PermissionError:
            print(f"  Error: Permission denied: {vtt_file}", file=sys.stderr)
            error_count += 1
        except Exception as e:
            print(f"  Error: Failed to convert {vtt_file}: {e}", file=sys.stderr)
            error_count += 1

    print(f"\nConversion complete: {success_count} succeeded, {error_count} failed")

    return 1 if error_count > 0 else 0


if __name__ == "__main__":
    sys.exit(main())