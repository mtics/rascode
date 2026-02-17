"""pytest 配置：确保未安装 rascode 时也能从 src 导入。"""
import sys
from pathlib import Path

# 项目根目录 = tests/ 的上一级
_root = Path(__file__).resolve().parents[1]
_src = _root / "src"
if _src.exists() and str(_src) not in sys.path:
    sys.path.insert(0, str(_src))
