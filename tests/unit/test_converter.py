import pytest
from vtt2txt.converter import convert_vtt


class TestConvertVtt:
    """Tests for convert_vtt function - RED phase of TDD."""

    def test_skip_webvtt_header(self):
        """WEBVTT header line should be skipped."""
        vtt = "WEBVTT\n\n00:00:00.100 --> 00:00:01.140\nText"
        result = convert_vtt(vtt)
        assert "WEBVTT" not in result

    def test_skip_timestamp_line(self):
        """Timestamp lines (00:00:00.100 --> 00:00:01.140) should be skipped."""
        vtt = "WEBVTT\n\n00:00:00.100 --> 00:00:01.140\nSubtitle text"
        result = convert_vtt(vtt)
        assert "-->" not in result
        assert "00:00:00.100" not in result

    def test_keep_subtitle_text(self):
        """Subtitle text lines should be kept."""
        vtt = "WEBVTT\n\n00:00:00.100 --> 00:00:01.140\n这是第一条字幕"
        result = convert_vtt(vtt)
        assert "这是第一条字幕" in result

    def test_multiple_subtitles_joined_by_newline(self):
        """Multiple subtitles should be joined by newlines."""
        vtt = """WEBVTT

00:00:00.100 --> 00:00:01.140
这是第一条字幕

00:00:01.140 --> 00:00:01.980
这是第二条字幕
"""
        result = convert_vtt(vtt)
        lines = result.strip().split("\n")
        assert len(lines) == 2
        assert lines[0] == "这是第一条字幕"
        assert lines[1] == "这是第二条字幕"

    def test_empty_lines_are_skipped(self):
        """Empty lines should not appear in output."""
        vtt = """WEBVTT

00:00:00.100 --> 00:00:01.140
Subtitle

00:00:01.140 --> 00:00:01.980
Another subtitle
"""
        result = convert_vtt(vtt)
        assert result != ""
        # Should not have consecutive newlines (empty lines)
        assert "\n\n" not in result

    def test_multiline_subtitle(self):
        """Subtitles spanning multiple lines should be kept as single unit."""
        vtt = """WEBVTT

00:00:00.100 --> 00:00:01.140
Line one of subtitle
Line two of subtitle

00:00:01.140 --> 00:00:01.980
Second subtitle
"""
        result = convert_vtt(vtt)
        # Multiline subtitle blocks are preserved with internal newlines
        assert "Line one of subtitle\nLine two of subtitle" in result
        assert "Second subtitle" in result
        # Count subtitle blocks by counting timestamps (2 timestamps = 2 blocks)
        # We can verify by counting timestamp matches in the original
        assert result.count("Line one") == 1
        assert result.count("Second subtitle") == 1
