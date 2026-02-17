# rascode

树莓派 **OLED-LCD-HAT-A 三联屏**控制与 **MCP / Agent** 集成。

- **硬件**：2 寸 ST7789 SPI 主屏 + 双 0.96 寸 SSD1315 I²C OLED（左/右）。
- **能力**：仪表盘（系统状态、时间、网络）、通过 MCP 供 Agent 写主屏与双 OLED；配套 Cursor Skill。
- **工具链**：Python 3.11+，依赖管理 `rye`，代码风格 `ruff`，测试 `pytest`。项目为 `src` 布局，包名 `rascode`。

## 快速运行

- **三联屏仪表盘**（主屏标题 + 左屏系统状态 + 右屏时间/网络）：
  ```bash
  python scripts/run_triple_screen.py
  ```
  若报错 `No access to /dev/mem`：可改用 **rpi-lgpio** 实现无需 root 的 GPIO（`pip uninstall -y RPi.GPIO && pip install rpi-lgpio`），或临时用 root 运行：`sudo python scripts/run_triple_screen.py`。
- **仅双 OLED 状态**（仅 I²C，通常无需 root）：
  ```bash
  python scripts/run_dashboard.py
  ```
- **仅主屏 2 寸 LCD 测试**：
  ```bash
  python scripts/run_main_screen.py
  ```
  用于单独验证主屏是否正常显示（与仪表盘相同，需 rpi-lgpio + spidev）。

## MCP 与 Cursor Skill

- **MCP**：在树莓派或已连接 HAT 的环境下，Cursor 通过 MCP 调用三联屏工具（需本机 rpi-lgpio + spidev 及设备权限）。项目内已包含 **`.cursor/mcp.json`**，用 Cursor 打开本项目根目录即可加载；若需全局或自定义，见 [docs/setup-mcp-and-skills.md](docs/setup-mcp-and-skills.md)。
- **Skill**：`.cursor/skills/rascode-triple-screen/SKILL.md` 已配置，在 Cursor 中启用 **rascode-triple-screen** 后，Agent 会在「显示到树莓派」「三联屏」「恢复仪表盘」等场景下自动使用 MCP 工具。详细配置步骤见 [docs/setup-mcp-and-skills.md](docs/setup-mcp-and-skills.md)。

本地启动 MCP 服务（可选，用于调试）：`python -m rascode.mcp.server`。工具：`show_main_text`、`show_left_oled`、`show_right_oled`、`clear_screen`、`restore_dashboard`。

## 测试

在已安装项目依赖的环境（如 `conda activate rascode` 后 `pip install -e .`）中运行：

```bash
pytest tests/ -v
```

未安装 `fastmcp` 时，MCP 相关 5 个测试会被跳过；安装后即可全部运行。

## 依赖与系统要求

- 树莓派上开启 **SPI** 与 **I²C**（`raspi-config`）。
- 安装：`luma.oled`、`luma.lcd`、`psutil`、`pillow`、`spidev`、`fastmcp`（见 `pyproject.toml`）。
- **三联屏与 MCP**：主屏需 GPIO + SPI，推荐 `pip install -e ".[pi-noroot]"`（rpi-lgpio，无需 root）；或 `pip install -e ".[pi]"`（RPi.GPIO）。二者不能同时安装。详见 [docs/display-daemon.md](docs/display-daemon.md)。
- **主屏花屏/黑屏**：见 [docs/troubleshooting-lcd.md](docs/troubleshooting-lcd.md)（含官方说明与排查顺序）。