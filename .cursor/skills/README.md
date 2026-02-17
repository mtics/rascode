# Cursor Skills

本目录下的 Skill 会在 Cursor 中作为「项目 Skill」出现，启用后 Agent 会在对应场景下使用相关能力。

## rascode-triple-screen

- **路径**：`rascode-triple-screen/SKILL.md`
- **作用**：在用户提到「显示到树莓派」「三联屏」「主屏/左屏/右屏」「恢复仪表盘」等时，引导 Agent 调用 rascode MCP 的 5 个工具。
- **依赖**：需同时配置并启用 MCP 服务 `rascode-triple-screen`（见项目根目录 `.cursor/mcp.json` 或 [docs/setup-mcp-and-skills.md](../docs/setup-mcp-and-skills.md)）。
