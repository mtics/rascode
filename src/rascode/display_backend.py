"""三联屏显示后端：唯一直接操作硬件的模块。

供 MCP 服务与仪表盘脚本调用；需本机具备设备权限（rpi-lgpio + spidev）。
环境变量 RASCODE_DISABLE_MAIN_LCD=1 时跳过主屏（仅用双 OLED），花屏时可使用。
"""
from __future__ import annotations

import os
from typing import Literal

_lcd = None
_oled = None
_displays_initialized = False
_init_error: str | None = None


def _main_lcd_disabled() -> bool:
    return os.environ.get("RASCODE_DISABLE_MAIN_LCD", "").strip() in ("1", "true", "yes")


def _ensure_displays() -> bool:
    global _lcd, _oled, _displays_initialized, _init_error
    if _displays_initialized:
        return _lcd is not None or _oled is not None
    _displays_initialized = True
    try:
        from rascode.hardware.display import DualOledDisplay, LcdHatMainDisplay, OledDisplayId

        if not _main_lcd_disabled():
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


def show_main_text(lines: list[str]) -> str:
    if _main_lcd_disabled():
        return "主屏已禁用（RASCODE_DISABLE_MAIN_LCD），仅双 OLED 可用。"
    if not _ensure_displays() or _lcd is None:
        return f"主屏不可用：{_init_error or '未初始化'}"
    try:
        _lcd.show_lines(lines[:22])
        return "ok"
    except Exception as e:
        return f"主屏写入失败: {e}"


def show_left_oled(lines: list[str]) -> str:
    if not _ensure_displays() or _oled is None:
        return f"左侧 OLED 不可用：{_init_error or '未初始化'}"
    try:
        from rascode.hardware.display import OledDisplayId

        _oled.show_lines(OledDisplayId.LEFT, lines[:6])
        return "ok"
    except Exception as e:
        return f"左侧 OLED 写入失败: {e}"


def show_right_oled(lines: list[str]) -> str:
    if not _ensure_displays() or _oled is None:
        return f"右侧 OLED 不可用：{_init_error or '未初始化'}"
    try:
        from rascode.hardware.display import OledDisplayId

        _oled.show_lines(OledDisplayId.RIGHT, lines[:6])
        return "ok"
    except Exception as e:
        return f"右侧 OLED 写入失败: {e}"


def clear_screen(screen: Literal["main", "left", "right", "all"]) -> str:
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


def restore_dashboard() -> str:
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
