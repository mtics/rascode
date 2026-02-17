"""MCP 三联屏工具测试（不依赖真实硬件，仅校验返回类型与内容）。"""

import pytest

try:
    import fastmcp  # noqa: F401
except ImportError:
    fastmcp = None


@pytest.mark.skipif(fastmcp is None, reason="fastmcp not installed")
def test_show_main_text_returns_str():
    """show_main_text 返回字符串（无硬件时为不可用提示）。"""
    from rascode.mcp.server import _show_main_text

    result = _show_main_text([])
    assert isinstance(result, str)
    assert len(result) > 0
    assert result in ("ok",) or "不可用" in result or "失败" in result


@pytest.mark.skipif(fastmcp is None, reason="fastmcp not installed")
def test_show_left_oled_returns_str():
    """show_left_oled 返回字符串。"""
    from rascode.mcp.server import _show_left_oled

    result = _show_left_oled([])
    assert isinstance(result, str)
    assert len(result) > 0


@pytest.mark.skipif(fastmcp is None, reason="fastmcp not installed")
def test_show_right_oled_returns_str():
    """show_right_oled 返回字符串。"""
    from rascode.mcp.server import _show_right_oled

    result = _show_right_oled([])
    assert isinstance(result, str)
    assert len(result) > 0


@pytest.mark.skipif(fastmcp is None, reason="fastmcp not installed")
def test_clear_screen_returns_str():
    """clear_screen 返回字符串。"""
    from rascode.mcp.server import _clear_screen

    result = _clear_screen("all")
    assert isinstance(result, str)
    assert len(result) > 0


@pytest.mark.skipif(fastmcp is None, reason="fastmcp not installed")
def test_restore_dashboard_returns_str():
    """restore_dashboard 返回字符串。"""
    from rascode.mcp.server import _restore_dashboard

    result = _restore_dashboard()
    assert isinstance(result, str)
    assert len(result) > 0
