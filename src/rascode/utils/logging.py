"""日志初始化与获取封装。"""

from __future__ import annotations

from logging import Logger, StreamHandler, Formatter, getLogger, basicConfig
import logging
from typing import Optional

from ..config.base import AppConfig


def init_logging(config: Optional[AppConfig] = None) -> None:
    """初始化标准库 logging。

    这里先使用最简单的 stdout 输出，后续可以接入 loguru。
    """

    level_name = (config.log_level if config is not None else "INFO").upper()
    level = getattr(logging, level_name, logging.INFO)

    basicConfig(
        level=level,
        format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
    )


def get_logger(name: str = "rascode") -> Logger:
    """获取命名 logger。"""
    return getLogger(name)

