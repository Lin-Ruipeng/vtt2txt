"""Path mapping module for VTT to TXT conversion."""

from pathlib import Path


def map_path(input_path: Path, input_dir: Path, output_dir: Path) -> Path:
    """Map VTT file path to corresponding TXT output path.

    Transforms paths by:
    - Replacing 'source_vtt' prefix with 'target_txt'
    - Replacing '.vtt' extension with '.txt'

    Args:
        input_path: Path to input VTT file
        input_dir: Base input directory (typically source_vtt)
        output_dir: Base output directory (typically target_txt)

    Returns:
        Path to corresponding output TXT file

    Example:
        source_vtt/xyz/ccc/file.vtt -> target_txt/xyz/ccc/file.txt
    """
    # Get relative path from input directory
    relative_path = input_path.relative_to(input_dir)
    # Replace .vtt extension with .txt
    output_path = (output_dir / relative_path).with_suffix('.txt')
    return output_path