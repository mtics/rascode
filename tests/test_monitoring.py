"""系统状态监控与 OLED 格式化测试。"""

import pytest

from rascode.services.monitoring import (
    SystemMonitor,
    SystemStats,
    format_stats_for_oled,
)


def test_format_stats_for_oled_with_temp():
    """有温度时 format_stats_for_oled 返回 4 行且含 CPU/T/MEM/DSK。"""
    stats = SystemStats(
        cpu_percent=12.5,
        cpu_temp_c=45.0,
        mem_percent=60.2,
        disk_percent=70.0,
    )
    lines = format_stats_for_oled(stats)
    assert len(lines) == 4
    assert "CPU:" in lines[0] and "12.5" in lines[0]
    assert "T:" in lines[1] and "45.0" in lines[1]
    assert "MEM:" in lines[2]
    assert "DSK:" in lines[3]


def test_format_stats_for_oled_without_temp():
    """无温度时第二行为 N/A。"""
    stats = SystemStats(
        cpu_percent=0.0,
        cpu_temp_c=None,
        mem_percent=0.0,
        disk_percent=0.0,
    )
    lines = format_stats_for_oled(stats)
    assert len(lines) == 4
    assert "N/A" in lines[1]


def test_system_monitor_collect_returns_system_stats():
    """SystemMonitor.collect() 返回 SystemStats。"""
    monitor = SystemMonitor()
    stats = monitor.collect()
    assert isinstance(stats, SystemStats)
    assert 0 <= stats.cpu_percent <= 100
    assert 0 <= stats.mem_percent <= 100
    assert 0 <= stats.disk_percent <= 100
