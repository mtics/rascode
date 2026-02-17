#!/usr/bin/env python3
"""在树莓派上验证主屏是否可用（直接调用 display_backend，需 rpi-lgpio + spidev）。

用法：
  python scripts/test_main_screen.py

成功时主屏会显示两行 "Test" / "OK" 并打印 Result: ok。
"""

from __future__ import annotations

import sys
from pathlib import Path

# 便于未安装时从项目根运行
root = Path(__file__).resolve().parents[1]
src = root / "src"
if src.is_dir() and str(src) not in sys.path:
    sys.path.insert(0, str(src))


def main() -> int:
    try:
        from rascode.display_backend import show_main_text

        result = show_main_text(["Test", "OK"])
        print("Result:", result)
        if result == "ok":
            print("主屏测试通过。")
            return 0
        if "/dev/mem" in result:
            print(
                "主屏需要 GPIO。推荐改用 rpi-lgpio：",
                "  pip uninstall -y RPi.GPIO && pip install rpi-lgpio",
                file=sys.stderr,
                sep="\n",
            )
        elif "spidev" in result:
            print("主屏需要 spidev。请安装： pip install spidev", file=sys.stderr)
        else:
            print("主屏返回非 ok，可能设备不可用。", file=sys.stderr)
        return 1
    except Exception as e:
        print("Error:", e, file=sys.stderr)
        return 1


if __name__ == "__main__":
    sys.exit(main())
