"""网络与时间信息采集与格式化，用于右侧 OLED 显示。"""

from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime
from typing import Optional

import psutil
import socket


@dataclass
class NetworkInfo:
    """网络信息快照。"""

    ip_address: Optional[str]
    is_up: bool
    active_interface: Optional[str]


def _get_ip_address() -> Optional[str]:
    """获取首个非回环 IPv4 地址。"""
    addrs = psutil.net_if_addrs()
    stats = psutil.net_if_stats()
    for iface, addr_list in addrs.items():
        st = stats.get(iface)
        if not st or not st.isup:
            continue
        for addr in addr_list:
            if addr.family == socket.AF_INET and not addr.address.startswith("127."):
                return addr.address
    return None


def collect_network_info() -> NetworkInfo:
    addrs = psutil.net_if_addrs()
    stats = psutil.net_if_stats()
    ip = None
    active_iface = None
    is_up = False

    for iface, st in stats.items():
        if not st.isup:
            continue
        # 跳过纯回环接口
        addrs_list = addrs.get(iface, [])
        for addr in addrs_list:
            if addr.family == socket.AF_INET and not addr.address.startswith("127."):
                ip = addr.address
                active_iface = iface
                is_up = True
                break
        if is_up:
            break

    if ip is None:
        ip = _get_ip_address()
        is_up = ip is not None

    return NetworkInfo(ip_address=ip, is_up=is_up, active_interface=active_iface)


def format_time_network_for_oled(net: NetworkInfo, now: Optional[datetime] = None) -> list[str]:
    """格式化当前时间 + IP + 网络状态为多行文本，用于右侧 OLED."""
    if now is None:
        now = datetime.now()

    lines: list[str] = []
    # 时间：HH:MM:SS
    lines.append(now.strftime("TIME %H:%M:%S"))

    # IP 行
    if net.ip_address:
        lines.append(f"IP   {net.ip_address}")
    else:
        lines.append("IP   N/A")

    # 接口与状态行
    if net.active_interface:
        status = "UP" if net.is_up else "DOWN"
        lines.append(f"IF   {net.active_interface} {status}")
    else:
        lines.append("IF   NONE")

    return lines

