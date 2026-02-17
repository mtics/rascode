"""显示设备抽象基类。"""

from __future__ import annotations

from abc import ABC, abstractmethod
from typing import Any


class DisplayError(RuntimeError):
    """显示相关错误。"""


class BaseDisplay(ABC):
    """所有显示设备的统一接口。"""

    @abstractmethod
    def init(self) -> None:
        """初始化显示设备。"""

    @abstractmethod
    def clear(self) -> None:
        """清屏。"""

    @abstractmethod
    def shutdown(self) -> None:
        """关闭显示设备并释放资源。"""

    @abstractmethod
    def show_image(self, image: Any) -> None:
        """显示一张图像。

        具体图像类型由子类定义，可以是 PIL.Image、帧缓冲等。
        """

