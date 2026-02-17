# 配置 MCP 与 Skills

## 一、MCP 服务（rascode-triple-screen）

MCP 服务暴露三联屏的 5 个工具，供 Cursor / 其他 Agent 调用。

### 方式 A：使用项目内配置（推荐）

项目已包含 **`.cursor/mcp.json`**，在 Cursor 中**以本项目根目录为工作区**打开时，会自动加载该 MCP 服务。

1. 用 Cursor 打开本项目根目录（`RasCode`）。
2. 确认已安装依赖：`pip install -e .`（树莓派上需 rpi-lgpio + spidev，见 [display-daemon.md](display-daemon.md)）。
3. 若 MCP 未出现在 Cursor 中：命令面板执行 **「MCP: Open MCP Settings」** 或 **「View: Open MCP Settings」**，确认列表中有 `rascode-triple-screen`。
4. 若启动失败（例如找不到 `rascode`）：将 `.cursor/mcp.json` 里的 `"cwd": "."` 改为本项目根目录的**绝对路径**，例如 `"cwd": "/home/pi/RasCode"`。

### 方式 B：使用全局配置

把 MCP 配置写到用户级文件，任意工作区均可使用（需在能访问树莓派或本机 HAT 的环境下）：

1. 打开或创建 **`~/.cursor/mcp.json`**（Windows：`%USERPROFILE%\.cursor\mcp.json`）。
2. 写入以下内容，并把 `cwd` 改为 RasCode 项目根目录的绝对路径：

```json
{
  "mcpServers": {
    "rascode-triple-screen": {
      "command": "python",
      "args": ["-m", "rascode.mcp.server"],
      "cwd": "/path/to/RasCode"
    }
  }
}
```

3. 保存后重启 Cursor 或重新加载 MCP 设置。

### 验证

- 在 Cursor 对话中让 Agent「把 Hello 显示到主屏」或「恢复仪表盘」，若 Agent 能调用 `show_main_text` / `restore_dashboard` 且无报错，即表示 MCP 已生效。
- 工具在无硬件或无权限时会返回「不可用」等提示，属正常。

---

## 二、Cursor Skill（rascode-triple-screen）

Skill 告诉 Agent 在什么场景下使用三联屏 MCP 工具、以及如何用。

### 位置

- **项目内**：`.cursor/skills/rascode-triple-screen/SKILL.md`
- **文档副本**：`docs/skills/rascode-triple-screen/SKILL.md`（内容一致，便于阅读与修改）

### 启用方式

1. 在 Cursor 中打开本项目。
2. 打开 **Skills** 设置（例如命令面板搜索「Skill」或设置中的 Skills 相关项）。
3. 在可用的项目 Skill 中启用 **rascode-triple-screen**。

启用后，当用户说「显示到树莓派」「推到主屏」「三联屏」「恢复仪表盘」等时，Agent 会优先使用本 MCP 的 5 个工具。

### 修改 Skill

编辑 `.cursor/skills/rascode-triple-screen/SKILL.md` 即可；若希望文档与之一致，可同步修改 `docs/skills/rascode-triple-screen/SKILL.md`。
