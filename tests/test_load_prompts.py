"""
agent/load_prompts.py — YAML 配置加载单元测试

覆盖：
- _load_yaml 正确解析 YAML 文件
- main_agent_config 和 sub_agents_config 非空
- 配置文件缺失时的异常行为
"""
import pytest
import tempfile
import os
from pathlib import Path


class TestLoadYaml:
    def test_load_valid_yaml(self, tmp_path):
        from agent.load_prompts import _load_yaml

        yaml_file = tmp_path / "test.yml"
        yaml_file.write_text("key1: value1\nkey2:\n  - a\n  - b\n", encoding="utf-8")

        result = _load_yaml(str(yaml_file))
        assert result == {"key1": "value1", "key2": ["a", "b"]}

    def test_load_empty_yaml(self, tmp_path):
        from agent.load_prompts import _load_yaml

        yaml_file = tmp_path / "empty.yml"
        yaml_file.write_text("", encoding="utf-8")

        result = _load_yaml(str(yaml_file))
        assert result is None

    def test_load_nonexistent_file(self):
        from agent.load_prompts import _load_yaml

        with pytest.raises(FileNotFoundError):
            _load_yaml("/nonexistent/path/file.yml")


class TestProjectConfig:
    def test_main_agent_config_not_empty(self):
        from agent.load_prompts import main_agent_config
        assert main_agent_config is not None
        assert isinstance(main_agent_config, dict)
        assert len(main_agent_config) > 0

    def test_sub_agents_config_not_empty(self):
        from agent.load_prompts import sub_agents_config
        assert sub_agents_config is not None
        assert isinstance(sub_agents_config, (dict, list))
        assert len(sub_agents_config) > 0

    def test_config_has_expected_keys(self):
        from agent.load_prompts import _config
        assert "main_agent" in _config
        assert "sub_agents" in _config
