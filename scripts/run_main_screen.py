"""仅主屏 2 寸 LCD 测试：显示标题与当前时间，用于验证主屏硬件。

前提：SPI 已开启，已安装 luma.lcd、RPi.GPIO。因使用 GPIO，需 root 运行。
"""

from __future__ import annotations

import sys
import time
from datetime import datetime

from rascode.hardware.display import LcdHatMainDisplay


def main() -> None:
    lcd = LcdHatMainDisplay()
    try:
        lcd.init()
    except RuntimeError as e:
        if "/dev/mem" in str(e):
            print("主屏 LCD 需要访问 GPIO，请使用 root 运行，例如：", file=sys.stderr)
            print(f"  sudo {sys.executable} scripts/run_main_screen.py", file=sys.stderr)
            sys.exit(1)
        raise

    try:
        while True:
            now = datetime.now()
            lcd.show_lines(
                [
                    "Rascode Main LCD",
                    "----------------",
                    "",
                    now.strftime("  %Y-%m-%d"),
                    now.strftime("  %H:%M:%S"),
                    "",
                    "Ctrl+C exit",
                ]
            )
            time.sleep(1.0)
    except KeyboardInterrupt:
        pass
    finally:
        lcd.shutdown()


if __name__ == "__main__":
    try:
        main()
    except RuntimeError as e:
        if "/dev/mem" in str(e):
            print("主屏 LCD 需要访问 GPIO，请使用 root 运行，例如：", file=sys.stderr)
            print(f"  sudo {sys.executable} scripts/run_main_screen.py", file=sys.stderr)
            sys.exit(1)
        raise
