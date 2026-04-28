"""Unit tests for path_mapper module (TDD RED phase - tests should FAIL initially)."""

from pathlib import Path

import pytest

from vtt2txt.path_mapper import map_path


class TestMapPath:
    """Tests for map_path function."""

    def test_basic_path_mapping(self, tmp_path):
        """Test basic path mapping from source_vtt to target_txt with .vtt to .txt extension."""
        input_dir = tmp_path / "source_vtt"
        output_dir = tmp_path / "target_txt"
        input_dir.mkdir()
        output_dir.mkdir()

        input_path = input_dir / "file.vtt"

        result = map_path(input_path, input_dir, output_dir)

        assert result == output_dir / "file.txt"

    def test_nested_directories_preserved(self, tmp_path):
        """Test that nested directories are preserved in the mapping."""
        input_dir = tmp_path / "source_vtt"
        output_dir = tmp_path / "target_txt"
        nested_dir = input_dir / "xyz" / "ccc"
        nested_dir.mkdir(parents=True)
        (output_dir / "xyz" / "ccc").mkdir(parents=True)

        input_path = nested_dir / "file.vtt"

        result = map_path(input_path, input_dir, output_dir)

        assert result == output_dir / "xyz" / "ccc" / "file.txt"

    def test_extension_replacement_vtt_to_txt(self, tmp_path):
        """Test that .vtt extension is replaced with .txt."""
        input_dir = tmp_path / "source_vtt"
        output_dir = tmp_path / "target_txt"
        input_dir.mkdir()
        output_dir.mkdir()

        input_path = input_dir / "document.vtt"

        result = map_path(input_path, input_dir, output_dir)

        assert result.suffix == ".txt"
        assert result.name == "document.txt"

    def test_full_path_transformation_example(self, tmp_path):
        """Test full path transformation: source_vtt/xyz/ccc/file.vtt -> target_txt/xyz/ccc/file.txt."""
        input_dir = tmp_path / "source_vtt"
        output_dir = tmp_path / "target_txt"
        nested_dir = input_dir / "xyz" / "ccc"
        nested_dir.mkdir(parents=True)
        (output_dir / "xyz" / "ccc").mkdir(parents=True)

        input_path = nested_dir / "file.vtt"

        result = map_path(input_path, input_dir, output_dir)

        expected = output_dir / "xyz" / "ccc" / "file.txt"
        assert result == expected

    def test_multiple_nested_levels(self, tmp_path):
        """Test mapping with multiple levels of nested directories."""
        input_dir = tmp_path / "source_vtt"
        output_dir = tmp_path / "target_txt"
        nested_dir = input_dir / "a" / "b" / "c" / "d"
        nested_dir.mkdir(parents=True)
        (output_dir / "a" / "b" / "c" / "d").mkdir(parents=True)

        input_path = nested_dir / "deep.vtt"

        result = map_path(input_path, input_dir, output_dir)

        assert result == output_dir / "a" / "b" / "c" / "d" / "deep.txt"
