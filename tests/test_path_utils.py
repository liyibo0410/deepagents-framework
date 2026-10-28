"""
utils/path_utils.py — resolve_path() 单元测试

覆盖 docstring 中列出的全部场景：
- 虚拟路径清洗（/workspace, /mnt/data, /home/user）
- upload/ 特殊处理
- 无 session_dir 时的相对/绝对路径
- Windows Unix 风格绝对路径（/开头无盘符）
- 路径嵌套防护（session_name 重复）
- 相对路径含 session_name / output 前缀
- 普通相对路径
- 虚拟路径 + upload 组合
"""
import os
import pytest
from pathlib import Path
from utils.path_utils import resolve_path


SESSION_DIR = "D:/Project/output/session_123"
CWD = "D:/Project"


@pytest.fixture(autouse=True)
def _patch_cwd(monkeypatch):
    monkeypatch.chdir(CWD)


class TestVirtualPrefixStripping:
    def test_workspace_prefix(self):
        result = resolve_path("/workspace/report.md", SESSION_DIR)
        expected = str(Path(SESSION_DIR).resolve() / "report.md")
        assert result == expected

    def test_mnt_data_prefix(self):
        result = resolve_path("/mnt/data/report.md", SESSION_DIR)
        expected = str(Path(SESSION_DIR).resolve() / "report.md")
        assert result == expected

    def test_home_user_prefix(self):
        result = resolve_path("/home/user/report.md", SESSION_DIR)
        expected = str(Path(SESSION_DIR).resolve() / "report.md")
        assert result == expected


class TestUploadSpecialHandling:
    def test_upload_in_relative_path(self):
        result = resolve_path("abc/upload/upload/file.pdf", SESSION_DIR)
        expected = str(Path("upload/upload/file.pdf").resolve())
        assert result == expected

    def test_virtual_prefix_plus_upload(self):
        result = resolve_path("/mnt/data/upload/doc.md", SESSION_DIR)
        expected = str(Path("upload/doc.md").resolve())
        assert result == expected


class TestNoSessionDir:
    def test_relative_path_resolves_to_cwd(self):
        result = resolve_path("sub/test.md", None)
        expected = str(Path("sub/test.md").resolve())
        assert result == expected

    def test_absolute_path_returned_as_is(self):
        abs_path = "D:/other/file.md"
        result = resolve_path(abs_path, None)
        expected = str(Path(abs_path).resolve())
        assert result == expected


class TestAbsolutePathWithSessionDir:
    def test_absolute_inside_session(self):
        inside = "D:/Project/output/session_123/sub/report.md"
        result = resolve_path(inside, SESSION_DIR)
        expected = str(Path(inside).resolve())
        assert result == expected

    def test_absolute_outside_session(self):
        outside = "D:/OtherDir/file.md"
        result = resolve_path(outside, SESSION_DIR)
        expected = str(Path(outside).resolve())
        assert result == expected


class TestUnixStyleAbsolutePath:
    def test_slash_prefix_no_drive_on_windows(self):
        result = resolve_path("/sub/test.md", SESSION_DIR)
        expected = str(Path(SESSION_DIR).resolve() / "sub" / "test.md")
        assert result == expected


class TestNestedSessionPrevention:
    def test_duplicate_session_name_collapsed(self):
        nested = "D:/Project/output/session_123/session_123/report.md"
        result = resolve_path(nested, SESSION_DIR)
        expected = str(Path(SESSION_DIR).resolve() / "report.md")
        assert result == expected

    def test_relative_with_session_name_in_parts(self):
        result = resolve_path("session_123/report.md", SESSION_DIR)
        expected = str(Path(SESSION_DIR).resolve() / "report.md")
        assert result == expected

    def test_relative_with_output_prefix(self):
        result = resolve_path("output/report.md", SESSION_DIR)
        expected = str(Path(SESSION_DIR).resolve() / "report.md")
        assert result == expected


class TestNormalRelativePath:
    def test_plain_relative(self):
        result = resolve_path("sub1/sub2/test.md", SESSION_DIR)
        expected = str(Path(SESSION_DIR).resolve() / "sub1" / "sub2" / "test.md")
        assert result == expected

    def test_bare_filename(self):
        result = resolve_path("report.md", SESSION_DIR)
        expected = str(Path(SESSION_DIR).resolve() / "report.md")
        assert result == expected


class TestWindowsBackslash:
    def test_backslash_in_filename(self):
        result = resolve_path("sub1\\sub2\\test.md", SESSION_DIR)
        expected = str(Path(SESSION_DIR).resolve() / "sub1" / "sub2" / "test.md")
        assert result == expected
