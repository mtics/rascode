"""rascode 顶层包：三联屏控制与 MCP 集成。"""

from __future__ import annotations

from importlib import metadata


def get_version() -> str:
    """返回当前包版本。"""
    try:
        return metadata.version("rascode")
    except metadata.PackageNotFoundError:
        return "0.0.0"

