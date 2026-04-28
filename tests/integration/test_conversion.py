"""Integration tests for end-to-end VTT to TXT conversion."""

from vtt2txt.converter import convert_vtt
from vtt2txt.path_mapper import map_path


class TestSingleFileConversion:
    """Tests for single VTT file conversion."""

    def test_single_file_conversion(self, tmp_path):
        """Convert a single VTT file and verify TXT output."""
        # Create input directory and file
        input_dir = tmp_path / "source_vtt"
        output_dir = tmp_path / "target_txt"
        input_dir.mkdir()

        vtt_content = """WEBVTT

00:00:00.100 --> 00:00:01.140
这是第一条字幕测试文本

00:00:01.140 --> 00:00:01.980
欢迎使用 VTT 转 TXT 工具
"""
        input_file = input_dir / "video.vtt"
        input_file.write_text(vtt_content, encoding="utf-8")

        # Run conversion
        content = input_file.read_text(encoding="utf-8")
        result = convert_vtt(content)

        # Map output path
        output_file = map_path(input_file, input_dir, output_dir)
        output_file.parent.mkdir(parents=True, exist_ok=True)
        output_file.write_text(result, encoding="utf-8")

        # Verify output
        assert output_file.exists()
        output_content = output_file.read_text(encoding="utf-8")
        assert "这是第一条字幕测试文本" in output_content
        assert "欢迎使用 VTT 转 TXT 工具" in output_content
        assert "WEBVTT" not in output_content
        assert "-->" not in output_content

    def test_output_contains_only_subtitle_text(self, tmp_path):
        """Verify output file contains only subtitle text, no timestamps or empty lines."""
        input_dir = tmp_path / "source_vtt"
        output_dir = tmp_path / "target_txt"
        input_dir.mkdir()

        vtt_content = """WEBVTT

00:00:00.100 --> 00:00:01.140
第一条字幕

00:00:01.140 --> 00:00:01.980
第二条字幕
"""
        input_file = input_dir / "test.vtt"
        input_file.write_text(vtt_content, encoding="utf-8")

        # Convert
        content = input_file.read_text(encoding="utf-8")
        result = convert_vtt(content)

        output_file = map_path(input_file, input_dir, output_dir)
        output_file.parent.mkdir(parents=True, exist_ok=True)
        output_file.write_text(result, encoding="utf-8")

        # Verify clean output
        output_content = output_file.read_text(encoding="utf-8")
        lines = output_content.strip().split("\n")

        # Should have exactly 2 lines (2 subtitles)
        assert len(lines) == 2
        assert lines[0] == "第一条字幕"
        assert lines[1] == "第二条字幕"

        # No timestamps, no WEBVTT, no empty lines
        assert "-->" not in output_content
        assert "WEBVTT" not in output_content
        assert "00:00" not in output_content
        assert output_content == "第一条字幕\n第二条字幕"


class TestNestedDirectoryStructure:
    """Tests for nested directory structure preservation."""

    def test_nested_directory_preserved(self, tmp_path):
        """Verify nested directory structure is preserved in output."""
        input_dir = tmp_path / "source_vtt"
        output_dir = tmp_path / "target_txt"
        input_dir.mkdir(parents=True)

        # Create nested structure: source_vtt/folder1/folder2/file.vtt
        nested_dir = input_dir / "folder1" / "folder2"
        nested_dir.mkdir(parents=True)
        input_file = nested_dir / "video.vtt"
        input_file.write_text(
            "WEBVTT\n\n00:00:00.100 --> 00:00:01.140\n嵌套目录测试",
            encoding="utf-8"
        )

        # Convert
        content = input_file.read_text(encoding="utf-8")
        result = convert_vtt(content)

        output_file = map_path(input_file, input_dir, output_dir)
        output_file.parent.mkdir(parents=True, exist_ok=True)
        output_file.write_text(result, encoding="utf-8")

        # Verify output path preserves structure
        expected_output = output_dir / "folder1" / "folder2" / "video.txt"
        assert output_file == expected_output
        assert output_file.exists()

        # Verify content
        assert output_file.read_text(encoding="utf-8") == "嵌套目录测试"

    def test_deep_nesting_levels(self, tmp_path):
        """Test conversion with multiple nesting levels."""
        input_dir = tmp_path / "source_vtt"
        output_dir = tmp_path / "target_txt"
        input_dir.mkdir()

        # Create deep structure
        deep_dir = input_dir / "a" / "b" / "c" / "d"
        deep_dir.mkdir(parents=True)
        input_file = deep_dir / "deep.vtt"
        input_file.write_text(
            "WEBVTT\n\n00:00:00.100 --> 00:00:01.140\n深层嵌套",
            encoding="utf-8"
        )

        # Convert
        content = input_file.read_text(encoding="utf-8")
        result = convert_vtt(content)

        output_file = map_path(input_file, input_dir, output_dir)
        output_file.parent.mkdir(parents=True, exist_ok=True)
        output_file.write_text(result, encoding="utf-8")

        # Verify structure
        expected = output_dir / "a" / "b" / "c" / "d" / "deep.txt"
        assert output_file == expected
        assert output_file.exists()
        assert output_file.read_text(encoding="utf-8") == "深层嵌套"


class TestMultipleFiles:
    """Tests for multiple files in same directory."""

    def test_multiple_files_same_directory(self, tmp_path):
        """Test converting multiple VTT files in the same directory."""
        input_dir = tmp_path / "source_vtt"
        output_dir = tmp_path / "target_txt"
        input_dir.mkdir()

        # Create multiple VTT files
        file1 = input_dir / "video1.vtt"
        file1.write_text(
            "WEBVTT\n\n00:00:00.100 --> 00:00:01.140\n第一个文件字幕",
            encoding="utf-8"
        )

        file2 = input_dir / "video2.vtt"
        file2.write_text(
            "WEBVTT\n\n00:00:00.100 --> 00:00:01.140\n第二个文件字幕",
            encoding="utf-8"
        )

        file3 = input_dir / "video3.vtt"
        file3.write_text(
            "WEBVTT\n\n00:00:00.100 --> 00:00:01.140\n第三个文件字幕",
            encoding="utf-8"
        )

        # Convert each file
        for input_file in [file1, file2, file3]:
            content = input_file.read_text(encoding="utf-8")
            result = convert_vtt(content)

            output_file = map_path(input_file, input_dir, output_dir)
            output_file.parent.mkdir(parents=True, exist_ok=True)
            output_file.write_text(result, encoding="utf-8")

        # Verify all output files exist
        assert (output_dir / "video1.txt").exists()
        assert (output_dir / "video2.txt").exists()
        assert (output_dir / "video3.txt").exists()

        # Verify content
        assert (output_dir / "video1.txt").read_text(encoding="utf-8") == "第一个文件字幕"
        assert (output_dir / "video2.txt").read_text(encoding="utf-8") == "第二个文件字幕"
        assert (output_dir / "video3.txt").read_text(encoding="utf-8") == "第三个文件字幕"

    def test_mixed_nested_and_flat_files(self, tmp_path):
        """Test conversion with both nested and flat file structures."""
        input_dir = tmp_path / "source_vtt"
        output_dir = tmp_path / "target_txt"
        input_dir.mkdir()

        # Flat file
        flat_file = input_dir / "flat.vtt"
        flat_file.write_text(
            "WEBVTT\n\n00:00:00.100 --> 00:00:01.140\n扁平文件",
            encoding="utf-8"
        )

        # Nested file
        nested_dir = input_dir / "sub"
        nested_dir.mkdir()
        nested_file = nested_dir / "nested.vtt"
        nested_file.write_text(
            "WEBVTT\n\n00:00:00.100 --> 00:00:01.140\n嵌套文件",
            encoding="utf-8"
        )

        # Convert both
        for input_file in [flat_file, nested_file]:
            content = input_file.read_text(encoding="utf-8")
            result = convert_vtt(content)

            output_file = map_path(input_file, input_dir, output_dir)
            output_file.parent.mkdir(parents=True, exist_ok=True)
            output_file.write_text(result, encoding="utf-8")

        # Verify
        assert (output_dir / "flat.txt").exists()
        assert (output_dir / "sub" / "nested.txt").exists()

        assert (output_dir / "flat.txt").read_text(encoding="utf-8") == "扁平文件"
        assert (output_dir / "sub" / "nested.txt").read_text(encoding="utf-8") == "嵌套文件"


class TestBilibiliFormat:
    """Tests for Bilibili VTT format specifics."""

    def test_bilibili_format_with_timestamps(self, tmp_path):
        """Test conversion of typical Bilibili VTT format with Chinese content."""
        input_dir = tmp_path / "source_vtt"
        output_dir = tmp_path / "target_txt"
        input_dir.mkdir()

        # Bilibili-style VTT content
        vtt_content = """WEBVTT

00:00:00.100 --> 00:00:01.140
这是第一条字幕测试文本

00:00:01.140 --> 00:00:01.980
欢迎使用 VTT 转 TXT 工具

00:00:01.980 --> 00:00:03.300
这是一个示例字幕文件

00:00:03.300 --> 00:00:04.500
支持中文和英文混合内容
"""
        input_file = input_dir / "bilibili.vtt"
        input_file.write_text(vtt_content, encoding="utf-8")

        # Convert
        content = input_file.read_text(encoding="utf-8")
        result = convert_vtt(content)

        output_file = map_path(input_file, input_dir, output_dir)
        output_file.parent.mkdir(parents=True, exist_ok=True)
        output_file.write_text(result, encoding="utf-8")

        # Verify output
        output_content = output_file.read_text(encoding="utf-8")
        lines = output_content.strip().split("\n")

        assert len(lines) == 4
        assert lines[0] == "这是第一条字幕测试文本"
        assert lines[1] == "欢迎使用 VTT 转 TXT 工具"
        assert lines[2] == "这是一个示例字幕文件"
        assert lines[3] == "支持中文和英文混合内容"

        # Ensure no timestamps or VTT headers
        assert "-->" not in output_content
        assert "WEBVTT" not in output_content
        assert "00:00" not in output_content

    def test_multiline_bilibili_subtitle(self, tmp_path):
        """Test Bilibili format with multiline subtitles."""
        input_dir = tmp_path / "source_vtt"
        output_dir = tmp_path / "target_txt"
        input_dir.mkdir()

        vtt_content = """WEBVTT

00:00:00.100 --> 00:00:01.140
第一行
第二行

00:00:01.140 --> 00:00:01.980
单独一行
"""
        input_file = input_dir / "multiline.vtt"
        input_file.write_text(vtt_content, encoding="utf-8")

        # Convert
        content = input_file.read_text(encoding="utf-8")
        result = convert_vtt(content)

        output_file = map_path(input_file, input_dir, output_dir)
        output_file.parent.mkdir(parents=True, exist_ok=True)
        output_file.write_text(result, encoding="utf-8")

        # Verify multiline preserved
        output_content = output_file.read_text(encoding="utf-8")
        assert "第一行\n第二行" in output_content
        assert "单独一行" in output_content
