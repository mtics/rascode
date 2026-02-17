"""仅双 OLED 仪表盘：左屏系统状态，右屏时间与网络。

前提：I²C 已开启，已安装 luma.oled；HAT 双 OLED 地址 0x3C / 0x3D。
"""

from __future__ import annotations

import time

from rascode.hardware.display import DualOledDisplay, OledDisplayId
from rascode.services import SystemMonitor
from rascode.services.monitoring import format_stats_for_oled
from rascode.services.network_info import collect_network_info, format_time_network_for_oled


def main() -> None:
    monitor = SystemMonitor()
    display = DualOledDisplay()
    display.init()

    try:
        while True:
            display.show_lines(OledDisplayId.LEFT, format_stats_for_oled(monitor.collect()))
            display.show_lines(OledDisplayId.RIGHT, format_time_network_for_oled(collect_network_info()))
            time.sleep(1.0)
    except KeyboardInterrupt:
        display.shutdown()


if __name__ == "__main__":
    main()

