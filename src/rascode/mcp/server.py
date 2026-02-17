"""三联屏 MCP 服务：暴露主 LCD、左/右 OLED 为 Agent 可调用的工具。

在树莓派上运行：python -m rascode.mcp.server
或：fastmcp run rascode.mcp.server
Cursor 中配置 MCP 后，Agent 可调用工具更新三块屏内容。
"""

from __future__ import annotations

from typing import Literal

from fastmcp import FastMCP

mcp = FastMCP(
    "rascode-triple-screen",
    description="树莓派 OLED-LCD-HAT-A 三联屏显示控制：主屏 2 寸 LCD、左侧/右侧 0.96 寸 OLED。",
)

# 延迟初始化，避免非树莓派环境导入即崩
_lcd = None
_oled = None
_displays_initialized = False
_init_error: str | None = None


def _ensure_displays() -> bool:
    """首次调用时初始化三块屏；若失败则后续工具 no-op。"""
    global _lcd, _oled, _displays_initialized, _init_error
    if _displays_initialized:
        return _lcd is not None and _oled is not None
    _displays_initialized = True
    try:
        from rascode.hardware.display import DualOledDisplay, LcdHatMainDisplay, OledDisplayId

        _lcd = LcdHatMainDisplay()
        _lcd.init()
        _oled = DualOledDisplay()
        _oled.init()
        return True
    except Exception as e:
        _init_error = str(e)
        _lcd = None
        _oled = None
        return False


@mcp.tool()
def show_main_text(lines: list[str]) -> str:
    """在主屏（2 寸 LCD，240×320）上显示多行文本。最多约 20 行，每行建议不超过 42 个字符。

    Args:
        lines: 要显示的行列表，从上到下排列。
    """
    if not _ensure_displays() or _lcd is None:
        return f"主屏不可用：{_init_error or '未初始化'}"
    try:
        _lcd.show_lines(lines[:22])
        return "ok"
    except Exception as e:
        return f"主屏写入失败: {e}"


@mcp.tool()
def show_left_oled(lines: list[str]) -> str:
    """在左侧 0.96 寸 OLED（128×64）上显示多行文本。最多约 6 行，每行建议 16 字符内。

    Args:
        lines: 要显示的行列表。
    """
    if not _ensure_displays() or _oled is None:
        return f"左侧 OLED 不可用：{_init_error or '未初始化'}"
    try:
        from rascode.hardware.display import OledDisplayId

        _oled.show_lines(OledDisplayId.LEFT, lines[:6])
        return "ok"
    except Exception as e:
        return f"左侧 OLED 写入失败: {e}"


@mcp.tool()
def show_right_oled(lines: list[str]) -> str:
    """在右侧 0.96 寸 OLED（128×64）上显示多行文本。最多约 6 行，每行建议 16 字符内。

    Args:
        lines: 要显示的行列表。
    """
    if not _ensure_displays() or _oled is None:
        return f"右侧 OLED 不可用：{_init_error or '未初始化'}"
    try:
        from rascode.hardware.display import OledDisplayId

        _oled.show_lines(OledDisplayId.RIGHT, lines[:6])
        return "ok"
    except Exception as e:
        return f"右侧 OLED 写入失败: {e}"


@mcp.tool()
def clear_screen(screen: Literal["main", "left", "right", "all"]) -> str:
    """清空指定屏幕。主屏和双 OLED 会变为黑屏。

    Args:
        screen: 要清空的屏幕：main（主 LCD）、left（左 OLED）、right（右 OLED）、all（三块全清）。
    """
    if not _ensure_displays():
        return f"显示不可用：{_init_error or '未初始化'}"
    try:
        from rascode.hardware.display import OledDisplayId

        if screen in ("main", "all") and _lcd is not None:
            _lcd.clear()
        if screen in ("left", "all") and _oled is not None:
            _oled.clear_oled(OledDisplayId.LEFT)
        if screen in ("right", "all") and _oled is not None:
            _oled.clear_oled(OledDisplayId.RIGHT)
        return "ok"
    except Exception as e:
        return f"清屏失败: {e}"


@mcp.tool()
def restore_dashboard() -> str:
    """恢复默认仪表盘：左 OLED 显示系统状态（CPU/温度/内存/磁盘），右 OLED 显示时间与网络信息，主屏显示标题「Rascode Dashboard」。"""
    if not _ensure_displays():
        return f"显示不可用：{_init_error or '未初始化'}"
    try:
        from rascode.hardware.display import OledDisplayId
        from rascode.services.monitoring import SystemMonitor, format_stats_for_oled
        from rascode.services.network_info import collect_network_info, format_time_network_for_oled

        monitor = SystemMonitor()
        stats = monitor.collect()
        left_lines = format_stats_for_oled(stats)
        net = collect_network_info()
        right_lines = format_time_network_for_oled(net)

        if _lcd is not None:
            _lcd.show_lines(["Rascode Dashboard", ""])
        if _oled is not None:
            _oled.show_lines(OledDisplayId.LEFT, left_lines)
            _oled.show_lines(OledDisplayId.RIGHT, right_lines)
        return "ok"
    except Exception as e:
        return f"恢复仪表盘失败: {e}"


def main() -> None:
    mcp.run()


if __name__ == "__main__":
    main()
