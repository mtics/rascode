"""基础应用配置与加载逻辑。"""

from __future__ import annotations

from dataclasses import dataclass
from enum import Enum
import os
from pathlib import Path


class AppEnvironment(str, Enum):
    """运行环境。"""

    DEV = "dev"
    TEST = "test"
    PROD = "prod"


@dataclass
class AppConfig:
    """顶层应用配置对象。

    后续可在此聚合硬件、网络等子配置。
    """

    env: AppEnvironment
    log_level: str
    project_root: Path


def _detect_env() -> AppEnvironment:
    value = os.getenv("RASCODE_ENV", "dev").lower()
    if value in {"dev", "development"}:
        return AppEnvironment.DEV
    if value in {"test", "testing"}:
        return AppEnvironment.TEST
    if value in {"prod", "production"}:
        return AppEnvironment.PROD
    return AppEnvironment.DEV


def load_config() -> AppConfig:
    """从环境变量与默认值加载应用配置。

    现阶段只提供最小可用集，后续再扩展为读取 YAML 等。
    """

    env = _detect_env()
    log_level = os.getenv("RASCODE_LOG_LEVEL", "INFO")
    project_root = Path(__file__).resolve().parents[3]
    return AppConfig(env=env, log_level=log_level, project_root=project_root)

