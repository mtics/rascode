"""三联屏仪表盘：主 LCD 显示标题，左 OLED 系统状态，右 OLED 时间与网络。

前提：已开启 SPI 与 I²C（raspi-config），并安装 luma.oled、luma.lcd 及本项目依赖。
"""

from __future__ import annotations

import time

from rascode.hardware.display import DualOledDisplay, OledDisplayId, LcdHatMainDisplay
from rascode.services import SystemMonitor
from rascode.services.monitoring import format_stats_for_oled
from rascode.services.network_info import collect_network_info, format_time_network_for_oled


def main() -> None:
    lcd = LcdHatMainDisplay()
    oled = DualOledDisplay()
    monitor = SystemMonitor()

    lcd.init()
    oled.init()

    try:
        while True:
            lcd.show_lines(["Rascode Dashboard", ""])
            stats = monitor.collect()
            oled.show_lines(OledDisplayId.LEFT, format_stats_for_oled(stats))
            net = collect_network_info()
            oled.show_lines(OledDisplayId.RIGHT, format_time_network_for_oled(net))
            time.sleep(1.0)
    except KeyboardInterrupt:
        pass
    finally:
        lcd.shutdown()
        oled.shutdown()


if __name__ == "__main__":
    main()
