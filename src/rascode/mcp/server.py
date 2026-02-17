"""三联屏 MCP 服务：暴露主 LCD、左/右 OLED 为 Agent 可调用的工具。

直接使用 display_backend 操作硬件。需本机已安装 rpi-lgpio + spidev，用户具备设备访问权限（或加入 spi/i2c/gpio 组）。
"""

from __future__ import annotations

from typing import Literal

from fastmcp import FastMCP

mcp = FastMCP("rascode-triple-screen")


def _show_main_text(lines: list[str]) -> str:
    from rascode.display_backend import show_main_text as backend_show

    return backend_show(lines)


@mcp.tool()
def show_main_text(lines: list[str]) -> str:
    """在主屏（2 寸 LCD，240×320）上显示多行文本。最多约 20 行，每行建议不超过 42 个字符。

    Args:
        lines: 要显示的行列表，从上到下排列。
    """
    return _show_main_text(lines)


def _show_left_oled(lines: list[str]) -> str:
    from rascode.display_backend import show_left_oled as backend_show

    return backend_show(lines)


@mcp.tool()
def show_left_oled(lines: list[str]) -> str:
    """在左侧 0.96 寸 OLED（128×64）上显示多行文本。最多约 6 行，每行建议 16 字符内。

    Args:
        lines: 要显示的行列表。
    """
    return _show_left_oled(lines)


def _show_right_oled(lines: list[str]) -> str:
    from rascode.display_backend import show_right_oled as backend_show

    return backend_show(lines)


@mcp.tool()
def show_right_oled(lines: list[str]) -> str:
    """在右侧 0.96 寸 OLED（128×64）上显示多行文本。最多约 6 行，每行建议 16 字符内。

    Args:
        lines: 要显示的行列表。
    """
    return _show_right_oled(lines)


def _clear_screen(screen: Literal["main", "left", "right", "all"]) -> str:
    from rascode.display_backend import clear_screen as backend_clear

    return backend_clear(screen)


@mcp.tool()
def clear_screen(screen: Literal["main", "left", "right", "all"]) -> str:
    """清空指定屏幕。主屏和双 OLED 会变为黑屏。

    Args:
        screen: 要清空的屏幕：main（主 LCD）、left（左 OLED）、right（右 OLED）、all（三块全清）。
    """
    return _clear_screen(screen)


def _restore_dashboard() -> str:
    from rascode.display_backend import restore_dashboard as backend_restore

    return backend_restore()


@mcp.tool()
def restore_dashboard() -> str:
    """恢复默认仪表盘：左 OLED 显示系统状态（CPU/温度/内存/磁盘），右 OLED 显示时间与网络信息，主屏显示标题「Rascode Dashboard」。"""
    return _restore_dashboard()


def main() -> None:
    mcp.run()


if __name__ == "__main__":
    main()
