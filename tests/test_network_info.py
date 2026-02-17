"""网络信息与时间格式化测试。"""

from datetime import datetime

import pytest

from rascode.services.network_info import (
    NetworkInfo,
    format_time_network_for_oled,
)


def test_format_time_network_for_oled_structure():
    """format_time_network_for_oled 返回约 3 行，含 TIME / IP / IF。"""
    net = NetworkInfo(ip_address="192.168.1.1", is_up=True, active_interface="eth0")
    now = datetime(2025, 2, 16, 14, 30, 0)
    lines = format_time_network_for_oled(net, now=now)
    assert len(lines) >= 3
    assert "TIME" in lines[0] and "14:30:00" in lines[0]
    assert "IP" in lines[1] and "192.168.1.1" in lines[1]
    assert "IF" in lines[2]


def test_format_time_network_for_oled_no_ip():
    """无 IP 时第二行为 N/A。"""
    net = NetworkInfo(ip_address=None, is_up=False, active_interface=None)
    lines = format_time_network_for_oled(net)
    assert any("N/A" in line for line in lines)
    assert any("IP" in line for line in lines)
