"""基础配置加载与环境检测测试。"""

import pytest


def test_app_environment_values():
    """AppEnvironment 枚举值符合预期。"""
    from rascode.config.base import AppEnvironment

    assert AppEnvironment.DEV.value == "dev"
    assert AppEnvironment.TEST.value == "test"
    assert AppEnvironment.PROD.value == "prod"


def test_load_config_returns_app_config():
    """load_config() 返回 AppConfig，且 project_root 为 Path。"""
    from rascode.config.base import AppConfig, load_config

    config = load_config()
    assert isinstance(config, AppConfig)
    assert config.env is not None
    assert isinstance(config.log_level, str) and len(config.log_level) > 0
    assert config.project_root is not None
    assert config.project_root.is_dir() or not config.project_root.exists()


def test_load_config_respects_rascode_env(monkeypatch):
    """RASCODE_ENV 能切换环境。"""
    from rascode.config.base import AppEnvironment, load_config

    monkeypatch.setenv("RASCODE_ENV", "test")
    config = load_config()
    assert config.env == AppEnvironment.TEST

    monkeypatch.setenv("RASCODE_ENV", "prod")
    config = load_config()
    assert config.env == AppEnvironment.PROD
