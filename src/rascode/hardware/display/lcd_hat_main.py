"""OLED-LCD-HAT-A 2 寸主屏（ST7789 SPI）显示适配。

实现基于 `luma.lcd` 的 ST7789 设备：
- SPI: /dev/spidev0.0 （port=0, device=0）
- DC: GPIO22 （物理引脚 15）
- RST: GPIO27（物理引脚 13）

如果你的接线不同，可以在此处调整 GPIO 编号。
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Optional

from PIL import Image

try:
    from luma.core.interface.serial import spi
    from luma.lcd.device import st7789
    from luma.core.render import canvas
except ImportError:  # pragma: no cover - 仅在未安装依赖时触发
    spi = None  # type: ignore[assignment]
    st7789 = None  # type: ignore[assignment]
    canvas = None  # type: ignore[assignment]

from .base import BaseDisplay, DisplayError


@dataclass
class LcdConfig:
    """2 寸 ST7789 主屏配置。"""

    width: int = 240
    height: int = 320
    spi_port: int = 0
    spi_device: int = 0
    gpio_dc: int = 22
    gpio_rst: int = 27
    rotation: int = 0  # 取值通常为 0/90/180/270


class LcdHatMainDisplay(BaseDisplay):
    """HAT 主屏显示封装。"""

    def __init__(self, config: Optional[LcdConfig] = None) -> None:
        if spi is None or st7789 is None or canvas is None:
            raise DisplayError(
                "未找到 luma.lcd 相关依赖。\n"
                "请在树莓派上安装：\n"
                "  pip install luma.lcd\n"
                "并确保已开启 SPI 接口（raspi-config）。"
            )
        self._config = config or LcdConfig()
        self._device = None

    @classmethod
    def from_config(cls, config: LcdConfig) -> "LcdHatMainDisplay":
        return cls(config=config)

    def init(self) -> None:
        serial = spi(
            port=self._config.spi_port,
            device=self._config.spi_device,
            gpio_DC=self._config.gpio_dc,
            gpio_RST=self._config.gpio_rst,
        )
        self._device = st7789(
            serial,
            width=self._config.width,
            height=self._config.height,
            rotate=self._config.rotation,
        )
        self.clear()

    def clear(self) -> None:
        if self._device is None:
            return
        # 用黑色填充整屏
        with canvas(self._device) as draw:  # type: ignore[misc]
            draw.rectangle(
                (0, 0, self._config.width, self._config.height),
                fill="black",
                outline="black",
            )
        self._device.show()  # type: ignore[attr-defined]

    def shutdown(self) -> None:
        self.clear()

    def show_lines(self, lines: list[str], line_height: int = 14) -> None:
        """在主屏上显示多行文本（等宽、白字黑底）。"""
        if self._device is None:
            raise DisplayError("LCD 未初始化，请先调用 init()。")
        with canvas(self._device) as draw:  # type: ignore[misc]
            draw.rectangle(
                (0, 0, self._config.width, self._config.height),
                fill="black",
                outline="black",
            )
            for i, line in enumerate(lines):
                y = i * line_height
                if y >= self._config.height:
                    break
                # 截断过长行，避免溢出
                draw.text((0, y), line[:42], fill="white")  # type: ignore[attr-defined]
        self._device.show()  # type: ignore[attr-defined]

    def show_image(self, image: Any) -> None:
        """显示一张 PIL Image 图像，自动缩放/旋转以适配屏幕。"""
        if self._device is None:
            raise DisplayError("LCD 未初始化，请先调用 init()。")
        if not isinstance(image, Image.Image):
            raise DisplayError("LcdHatMainDisplay 目前仅支持 PIL.Image.Image 类型。")

        # 调整尺寸以适配屏幕
        img = image.convert("RGB")
        img = img.resize((self._config.width, self._config.height))
        self._device.display(img)  # type: ignore[call-arg]

