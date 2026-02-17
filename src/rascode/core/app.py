"""应用主对象定义。"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Optional

from ..config.base import AppConfig
from ..utils.logging import get_logger, init_logging


LOGGER_NAME = "rascode.app"


@dataclass
class Application:
    """顶层应用。

    目前只包含最小骨架：配置与生命周期方法。
    """

    config: AppConfig
    _running: bool = False

    @classmethod
    def from_config(cls, config: AppConfig) -> "Application":
        """根据配置创建应用实例，并初始化日志。"""
        init_logging(config)
        logger = get_logger(LOGGER_NAME)
        logger.debug("Creating Application with env=%s", config.env.value)
        return cls(config=config)

    def start(self) -> None:
        """启动主循环。现阶段仅作为占位。"""
        logger = get_logger(LOGGER_NAME)
        if self._running:
            logger.warning("Application already running.")
            return
        self._running = True
        logger.info("Application started.")

    def stop(self) -> None:
        """停止应用。"""
        logger = get_logger(LOGGER_NAME)
        if not self._running:
            logger.warning("Application is not running.")
            return
        self._running = False
        logger.info("Application stopped.")

    def run_once(self) -> None:
        """执行单步循环，占位方法。

        用于后续在 REPL 或测试中驱动一帧处理。
        """
        logger = get_logger(LOGGER_NAME)
        logger.debug("run_once called (no-op skeleton).")

