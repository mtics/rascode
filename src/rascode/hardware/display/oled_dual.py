"""双 0.96 寸 SSD1315 OLED 显示适配。

设计目标：
1. 尽量薄封装：上层只关心“写几行文本 / 一张小图”，不关心 I²C 细节。
2. 依赖 `luma.oled` 库，但如果未安装，给出清晰错误提示。
"""

from __future__ import annotations

from dataclasses import dataclass
from enum import Enum
from typing import Any, Iterable, List, Optional

try:
    from luma.core.interface.serial import i2c as luma_i2c
    from luma.oled.device import ssd1306
    from luma.core.render import canvas
except ImportError:  # pragma: no cover - 仅在未安装依赖时触发
    luma_i2c = None  # type: ignore[assignment]
    ssd1306 = None  # type: ignore[assignment]
    canvas = None  # type: ignore[assignment]

from .base import BaseDisplay, DisplayError


class OledDisplayId(str, Enum):
    """区分两块 OLED。"""

    LEFT = "left"
    RIGHT = "right"


@dataclass
class OledConfig:
    """双 OLED 配置。

    默认地址为 0x3C / 0x3D，对应文档中的两块屏。
    """

    i2c_port: int = 1
    addr_left: int = 0x3C
    addr_right: int = 0x3D
    width: int = 128
    height: int = 64


class DualOledDisplay(BaseDisplay):
    """双 OLED 显示封装。

    提供「文本行显示」的便捷方法，方便系统状态输出。
    """

    def __init__(self, config: Optional[OledConfig] = None) -> None:
        if luma_i2c is None or ssd1306 is None or canvas is None:
            raise DisplayError(
                "luma.oled 未安装，无法使用 DualOledDisplay。"
                "请先执行：sudo apt-get install python3-luma.oled 或 pip install luma.oled"
            )
        self._config = config or OledConfig()
        self._left = None
        self._right = None

    @classmethod
    def from_config(cls, config: OledConfig) -> "DualOledDisplay":
        return cls(config=config)

    def init(self) -> None:
        """初始化两块 OLED 设备。"""
        serial_left = luma_i2c(port=self._config.i2c_port, address=self._config.addr_left)
        serial_right = luma_i2c(port=self._config.i2c_port, address=self._config.addr_right)
        self._left = ssd1306(serial_left, width=self._config.width, height=self._config.height)
        self._right = ssd1306(serial_right, width=self._config.width, height=self._config.height)
        self.clear()

    def clear(self) -> None:
        """两块屏全部清空。"""
        for dev in (self._left, self._right):
            if dev is not None:
                dev.clear()
                dev.show()

    def clear_oled(self, oled: OledDisplayId) -> None:
        """只清空指定一侧的 OLED。"""
        dev = self._get_device(oled)
        dev.clear()
        dev.show()

    def shutdown(self) -> None:
        """目前不需要特别释放，保留接口。"""
        self.clear()

    def show_image(self, image: Any) -> None:
        """占位：当前不做通用图像显示，仅支持文本 API。

        如果后续需要，可将 image 视为 (OledDisplayId, PIL.Image) 的元组。
        """
        raise DisplayError("DualOledDisplay.show_image 暂未实现通用图像显示。")

    # === 文本显示便捷方法 ===

    def show_lines(self, oled: OledDisplayId, lines: Iterable[str]) -> None:
        """在指定 OLED 上显示多行文本。

        为减少依赖复杂字体，这里使用默认等宽字体。
        """
        device = self._get_device(oled)
        # 行高简单设为 10 像素，可根据字体调整
        line_height = 10
        with canvas(device) as draw:  # type: ignore[misc]
            for idx, line in enumerate(lines):
                y = idx * line_height
                if y >= self._config.height:
                    break
                draw.text((0, y), line, fill=255)

    def _get_device(self, oled: OledDisplayId):
        if oled == OledDisplayId.LEFT:
            if self._left is None:
                raise DisplayError("LEFT OLED 未初始化，请先调用 init()。")
            return self._left
        if oled == OledDisplayId.RIGHT:
            if self._right is None:
                raise DisplayError("RIGHT OLED 未初始化，请先调用 init()。")
            return self._right
        raise DisplayError(f"未知的 OledDisplayId: {oled}")

