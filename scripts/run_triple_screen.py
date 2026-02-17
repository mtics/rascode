"""三联屏仪表盘：主 LCD 显示标题，左 OLED 系统状态，右 OLED 时间与网络。

前提：已开启 SPI 与 I²C，并安装 luma.oled、luma.lcd、spidev 及 rpi-lgpio（或 RPi.GPIO）。无需 root。
主屏花屏时可仅用双 OLED：RASCODE_DISABLE_MAIN_LCD=1 python scripts/run_triple_screen.py
"""

from __future__ import annotations

import os
import sys
import time

from rascode.hardware.display import DualOledDisplay, OledDisplayId, LcdHatMainDisplay
from rascode.services import SystemMonitor
from rascode.services.monitoring import format_stats_for_oled
from rascode.services.network_info import collect_network_info, format_time_network_for_oled


def _main_lcd_disabled() -> bool:
    return os.environ.get("RASCODE_DISABLE_MAIN_LCD", "").strip() in ("1", "true", "yes")


def main() -> None:
    oled = DualOledDisplay()
    monitor = SystemMonitor()
    lcd = None

    if not _main_lcd_disabled():
        lcd = LcdHatMainDisplay()
        try:
            lcd.init()
        except RuntimeError as e:
            if "/dev/mem" in str(e):
                print("主屏 LCD 需要访问 GPIO，请使用 root 运行，或禁用主屏：", file=sys.stderr)
                print("  RASCODE_DISABLE_MAIN_LCD=1 python scripts/run_triple_screen.py", file=sys.stderr)
                sys.exit(1)
            raise
    else:
        print("主屏已禁用，仅运行双 OLED 仪表盘。", file=sys.stderr)

    oled.init()

    try:
        while True:
            if lcd is not None:
                lcd.show_lines(["Rascode Dashboard", ""])
            stats = monitor.collect()
            oled.show_lines(OledDisplayId.LEFT, format_stats_for_oled(stats))
            net = collect_network_info()
            oled.show_lines(OledDisplayId.RIGHT, format_time_network_for_oled(net))
            time.sleep(1.0)
    except KeyboardInterrupt:
        pass
    finally:
        if lcd is not None:
            lcd.shutdown()
        oled.shutdown()


if __name__ == "__main__":
    try:
        main()
    except RuntimeError as e:
        if "/dev/mem" in str(e):
            print("主屏 LCD 需要访问 GPIO，请使用 root 运行，例如：", file=sys.stderr)
            print(f"  sudo {sys.executable} scripts/run_triple_screen.py", file=sys.stderr)
            sys.exit(1)
        raise
