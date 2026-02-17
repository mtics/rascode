# 三联屏运行说明（无需 daemon）

当前方案**不使用** systemd 或 display daemon，保持简洁：

- **仪表盘**：`python scripts/run_triple_screen.py`
- **MCP 控制**：`python -m rascode.mcp.server`，直接由本进程操作三联屏

**要求**：树莓派上安装 **rpi-lgpio** + **spidev**，并开启 SPI、I²C；用户需能访问相应设备（通常将用户加入 `spi`、`i2c`、`gpio` 组即可，无需 root）。

```bash
pip install -e ".[pi-noroot]"   # rpi-lgpio，与 RPi.GPIO 二选一
# 或 pip install spidev 若未随项目安装
sudo usermod -aG spi,i2c,gpio $USER   # 重新登录后生效
```

若出现 `No access to /dev/mem`，请改用 rpi-lgpio（见 README）。
