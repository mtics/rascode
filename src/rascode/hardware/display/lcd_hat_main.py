"""OLED-LCD-HAT-A 2 寸主屏（ST7789 SPI）显示适配。

引脚与官方说明一致（见 https://spotpear.cn/wiki/0.96inch-OLED-2inch-LCD-HAT-A.html）：
- SPI: /dev/spidev0.0（port=0, device=0）；DC=物理15→BCM22，RST=物理13→BCM27。
- 通信时序：SCLK 第一个下降沿采样，即 SPI mode 0（CPOL=0, CPHA=0）。
花屏排查见 docs/troubleshooting-lcd.md。
"""

from __future__ import annotations

import os
import time
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


def _default_spi_speed_hz() -> int:
    """环境变量 RASCODE_LCD_SPI_SPEED（Hz）可覆盖默认速率，花屏时试 2000000 或 1000000。"""
    v = os.environ.get("RASCODE_LCD_SPI_SPEED")
    if v is not None:
        try:
            return int(v)
        except ValueError:
            pass
    return 2_000_000  # 默认 2MHz，尽量减轻花屏


@dataclass
class LcdConfig:
    """2 寸 ST7789 主屏配置。"""

    width: int = 240
    height: int = 320
    spi_port: int = 0
    spi_device: int = 0
    spi_speed_hz: int = 0  # 0 表示用 _default_spi_speed_hz()
    gpio_dc: int = 22
    gpio_rst: int = 27
    rotation: int = 0  # 取值通常为 0/90/180/270
    reset_hold_s: float = 0.1  # 复位低电平保持时间
    reset_release_s: float = 0.15  # 复位释放后等待再初始化


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
        raw = config or LcdConfig()
        speed = raw.spi_speed_hz or _default_spi_speed_hz()
        self._config = LcdConfig(
            width=raw.width,
            height=raw.height,
            spi_port=raw.spi_port,
            spi_device=raw.spi_device,
            spi_speed_hz=speed,
            gpio_dc=raw.gpio_dc,
            gpio_rst=raw.gpio_rst,
            rotation=raw.rotation,
            reset_hold_s=raw.reset_hold_s,
            reset_release_s=raw.reset_release_s,
        )
        self._device = None

    @classmethod
    def from_config(cls, config: LcdConfig) -> "LcdHatMainDisplay":
        return cls(config=config)

    def init(self) -> None:
        serial = spi(
            port=self._config.spi_port,
            device=self._config.spi_device,
            bus_speed_hz=self._config.spi_speed_hz,
            gpio_DC=self._config.gpio_dc,
            gpio_RST=self._config.gpio_rst,
            reset_hold_time=self._config.reset_hold_s,
            reset_release_time=self._config.reset_release_s,
            spi_mode=0,  # 与官方说明一致：第一下降沿采样
        )
        self._device = st7789(
            serial,
            width=self._config.width,
            height=self._config.height,
            rotate=self._config.rotation,
        )
        # 与官方 C 例程对齐：luma 默认 MADCTL=0x70，Waveshare 2 寸屏用 0x00，否则易花屏
        self._device.command(0x36, 0x00)  # MADCTL: 与 LCD_2inch.c 一致
        time.sleep(0.1)
        self.clear()
        time.sleep(0.05)
        self.clear()  # 再清一次，减少首帧花屏

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

