"""系统状态监控服务。

主要用于在 OLED 上显示的轻量信息：
CPU 使用率、CPU 温度、内存使用率、磁盘使用率等。
"""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Optional

import psutil


CPU_TEMP_PATHS = [
    Path("/sys/class/thermal/thermal_zone0/temp"),
]


@dataclass
class SystemStats:
    """系统状态快照。"""

    cpu_percent: float
    cpu_temp_c: Optional[float]
    mem_percent: float
    disk_percent: float


class SystemMonitor:
    """收集树莓派系统状态的简单封装。"""

    def __init__(self, disk_path: str = "/") -> None:
        self._disk_path = disk_path

    def collect(self) -> SystemStats:
        """采集一次系统状态。"""
        cpu_percent = psutil.cpu_percent(interval=None)
        mem = psutil.virtual_memory()
        disk = psutil.disk_usage(self._disk_path)
        temp_c = _read_cpu_temp()
        return SystemStats(
            cpu_percent=cpu_percent,
            cpu_temp_c=temp_c,
            mem_percent=mem.percent,
            disk_percent=disk.percent,
        )


def _read_cpu_temp() -> Optional[float]:
    """从标准路径读取 CPU 温度（单位 ℃）。"""
    for path in CPU_TEMP_PATHS:
        try:
            if path.exists():
                text = path.read_text().strip()
                # 常见格式为 millidegree，例如 53000 表示 53.0℃
                value = float(text) / 1000.0
                return value
        except (OSError, ValueError):
            continue
    return None


def format_stats_for_oled(stats: SystemStats) -> list[str]:
    """格式化为适合 128x64 OLED 的多行文本。"""
    lines: list[str] = []
    lines.append(f"CPU: {stats.cpu_percent:5.1f}%")
    if stats.cpu_temp_c is not None:
        lines.append(f"T:   {stats.cpu_temp_c:5.1f} C")
    else:
        lines.append("T:   N/A")
    lines.append(f"MEM: {stats.mem_percent:5.1f}%")
    lines.append(f"DSK: {stats.disk_percent:5.1f}%")
    return lines

