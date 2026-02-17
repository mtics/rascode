"""开发环境入口脚本。

在命令行中可以通过 `python -m rascode.scripts.run_dev` 或直接运行此文件启动。
"""

from __future__ import annotations

from rascode import create_app


def main() -> None:
    app = create_app()
    app.start()


if __name__ == "__main__":
    main()

