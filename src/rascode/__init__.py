"""
rascode 顶层包。

这里仅提供轻量级的创建入口，避免在导入时就初始化硬件。
"""

from __future__ import annotations

from importlib import metadata


def get_version() -> str:
    """返回当前包版本。"""
    try:
        return metadata.version("rascode")
    except metadata.PackageNotFoundError:
        return "0.0.0"


def create_app():
    """延迟导入 Application，避免循环依赖。"""
    from .core.app import Application  # type: ignore[attr-defined]
    from .config.base import load_config

    config = load_config()
    return Application.from_config(config)

