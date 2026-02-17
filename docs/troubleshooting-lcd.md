# 主屏 2 寸 LCD 花屏 / 黑屏排查

参考：[斑梨电子 OLED-LCD-HAT-A 说明](https://spotpear.cn/wiki/0.96inch-OLED-2inch-LCD-HAT-A.html)、[Waveshare OLED/LCD HAT (A) 维基](https://www.waveshare.com/wiki/OLED/LCD_HAT_(A))（含 arm64 WiringPi 与 C/Python 例程）。

**花屏已修复**：若用官方 C 例程 `./main 2` 主屏正常而本项目花屏，多为 luma 的 ST7789 默认 **MADCTL (0x36)** 与 Waveshare 2 寸屏不一致。本项目已在 `lcd_hat_main.py` 的 init 后补发 `0x36 0x00` 与官方 `LCD_2inch.c` 对齐，主屏应可正常显示。若仍异常，可暂时用 `RASCODE_DISABLE_MAIN_LCD=1` 仅开双 OLED（见下文）。

## 官方说明中的要点

### 引脚（与代码一致）

| 功能 | Board 物理引脚 | 本项目中 BCM GPIO |
|------|----------------|-------------------|
| DC   | 15             | 22                |
| RST  | 13             | 27                |
| SPI  | MOSI 19, SCLK 23, CS 24 | spidev0.0 |

### FAQ 中与花屏/黑屏相关的建议

1. **LCD 黑屏**
   - 确认已开启 SPI：`sudo raspi-config` → Interfacing Options → SPI → Yes，然后重启。
   - **背光**：若背光引脚无输出，可尝试**悬空 BL 控制线**（部分 HAT 背光单独接线）。

2. **混用多种驱动库导致异常**
   - 若曾用 **wiringPi** 或 **BCM2835** 的例程驱动过该屏，再运行 Python（或本项目的 luma/rpi-lgpio）可能导致屏无法正常刷新。
   - 官方建议：**重启树莓派**后再用 Python 驱动。

3. **用官方例程对比**
   - 官方 zip 内带**预编译的 main**。若之前用 `sudo` 解压或编译过，目录可能属 root，直接 `unzip -o` 会报 Permission denied，需先删再解压。**不要**在解压后执行 `make clean` 或 `make`（会删/重编 main 且依赖 wiringPi，Bookworm 可能编不过）。推荐步骤：
     ```bash
     cd /tmp
     sudo rm -rf OLED_LCD_HAT_A_Demo
     wget -q -O OLED_LCD_HAT_A_Demo.zip https://www.waveshare.net/w/upload/2/21/OLED_LCD_HAT_A_Demo.zip
     unzip -o OLED_LCD_HAT_A_Demo.zip
     cd OLED_LCD_HAT_A_Demo/c
     sudo ./main 2
     ```
   - 若执行 `sudo ./main 2` 报 **command not found**：zip 内预编译的 main 多为 **32 位 ARM**，在 **64 位**（aarch64）上无法运行。可按下面「64 位系统下编译官方 C 例程」安装 Waveshare 提供的 arm64 WiringPi 后重新编译并运行；或继续用 `RASCODE_DISABLE_MAIN_LCD=1` 仅开双 OLED。
   - 若官方 `./main 2` 能运行且正常而本项目花屏，可对比初始化顺序；若官方也花屏，则更可能是排线、背光或屏体问题。

4. **64 位系统下编译并运行官方 C 例程**（参考 [Waveshare 维基](https://www.waveshare.com/wiki/OLED/LCD_HAT_(A))）  
   - 维基提供 **arm64 版 WiringPi**，安装后可在 64 位树莓派上编译官方 demo 并运行 `./main 2`：
     ```bash
     cd /tmp
     wget -q -O WiringPi.zip https://files.waveshare.com/wiki/OLED-LCD-HAT-A/WiringPi.zip
     unzip -o WiringPi.zip && cd WiringPi
     sudo ./build debian
     sudo mv debian-template/wiringpi_3.10_arm64.deb .
     sudo apt install -y ./wiringpi_3.10_arm64.deb
     gpio -v
     ```
   - 再进入官方 demo 的 C 目录编译并运行仅 2 寸屏：
     ```bash
     cd /tmp/OLED_LCD_HAT_A_Demo/c
     sudo make clean && sudo make -j8
     sudo ./main 2
     ```
   - 若编译仍报错或 `gpio -v` 不可用，可能需根据维基或系统版本调整；成功后即可用官方例程对比主屏是否花屏。

5. **不安装 deb、仅用本地库运行**（适合已在本机编译过 WiringPi 与 demo 的情况）  
   - 若 `/tmp/WiringPi` 下已执行过 `./build debian`（无需 sudo），会生成 `debian-template/wiringpi_3.10_arm64.deb`。可解压该 deb 并用其头文件/库编译 demo，无需 `sudo apt install`：
     ```bash
     # 解压 deb 得到 usr/include 与 usr/lib
     dpkg -x /tmp/WiringPi/debian-template/wiringpi_3.10_arm64.deb /tmp/wiringpi_usr
     # 编译官方 demo（demo 目录需已存在，如 /tmp/OLED_LCD_HAT_A_Demo）
     cd /tmp/OLED_LCD_HAT_A_Demo/c
     make clean
     make -j8 CFLAGS="-g -O0 -Wall -D USE_WIRINGPI_LIB -I/tmp/wiringpi_usr/usr/include" LIB="-L/tmp/wiringpi_usr/usr/lib -lwiringPi -lm"
     # 运行 2 寸屏测试（需 sudo 访问 SPI/GPIO；须用 sudo env 传入 LD_LIBRARY_PATH，否则 sudo 会清空环境变量）
     sudo env LD_LIBRARY_PATH=/tmp/wiringpi_usr/usr/lib ./main 2
     ```
   - 若上述步骤已在当前树莓派上完成，只需在终端执行最后一行即可对比主屏显示是否正常。

## 本项目已做的软件缓解

- 默认 SPI 速率 2MHz，可通过环境变量 `RASCODE_LCD_SPI_SPEED`（Hz）调整，例如 `1000000` 试 1MHz。
- 复位时序：`reset_hold_time=0.1s`，`reset_release_time=0.15s`。
- 初始化时清屏两次，并显式使用 **SPI mode 0**（与官方“第一下降沿采样”一致）。

## 建议排查顺序

1. **重启树莓派**后只运行本项目或只运行官方 2 寸屏例程，看是否仍花屏。
2. 运行官方 **`sudo ./main 2`**，确认同硬件下官方例程是否正常。
   - 若官方也花屏 → 多为排线、背光或屏体问题，可试悬空 BL、换排线或换屏。
   - 若官方正常 → 可对比官方 C 与 luma 的初始化序列，或暂时关闭主屏仅用双 OLED。
3. 检查背光：若有单独 BL 线，尝试悬空或接 3.3V 再试。
4. 换一根排线或换一块同型号 2 寸屏，排除屏/排线损坏。

## 花屏时仅用双 OLED

若暂时无法解决主屏花屏，可**关闭主屏**，仅使用左右两块 0.96 寸 OLED（仪表盘与 MCP 照常）：

```bash
# 仪表盘（仅双 OLED）
RASCODE_DISABLE_MAIN_LCD=1 python scripts/run_triple_screen.py
```

MCP 在同样环境下（先设置 `export RASCODE_DISABLE_MAIN_LCD=1` 再启动）也会跳过主屏；`show_main_text` 会返回「主屏已禁用」提示，`show_left_oled` / `show_right_oled` / `restore_dashboard` 正常可用。
