# ComfyUI-Env-Loader

一个 ComfyUI 的自定义节点，用于在启动时读取项目根目录的 `.env` 文件，自动分析并提供可选择的环境变量 key，下拉选择后输出对应的 value。启动时会在日志中打印已加载的 key，便于排查配置问题。

## 特性

- 自动读取 ComfyUI 根目录下的 `.env` 文件
- 在节点输入处显示可选 key 的下拉菜单
- 输出选中 key 的值（`STRING`）
- 启动日志打印：加载的 `.env` 路径与已解析出的 key 列表
- 变更检测：当 `.env` 文件修改后，节点选项和输出会刷新

## 安装

- 通过 ComfyUI-Manager：选择“Install via URL”，填入本仓库地址即可安装
- 手动安装：将仓库克隆到 `ComfyUI/custom_nodes/ComfyUI-Env-Loader`

```bash
# 示例（请替换为你的实际路径）
cd path/to/ComfyUI/custom_nodes
git clone https://github.com/hubo502/ComfyUI-Env-Loader.git
```

## 使用

- 在 ComfyUI 的节点面板中找到 `Utils / Env Key Selector`
- 输入：`key`（下拉选择从 `.env` 中解析出的 key）
- 输出：`value`（选中 key 的字符串值）

### `.env` 示例

```
API_KEY=12345
MODEL_PATH="C:/Models"
DEBUG=true
```

- 支持 `#` 注释与空行
- 支持用单引号或双引号包裹的值

## 工作原理

- 节点在模块导入时根据 `custom_nodes` 目录定位 ComfyUI 根目录，并读取根目录下的 `.env`：
  - `ENV_PATH = <ComfyUI 根目录>/.env`
  - 启动时打印：`[Env Loader] Loading env from ...` 和已加载的 key 列表
- `INPUT_TYPES` 返回下拉菜单元数据，展示所有可用 key
- `IS_CHANGED` 返回 `.env` 的 `mtime`，确保 ComfyUI 在文件变更后刷新节点

## 依赖

- 仅使用 Python 标准库，无额外依赖

## 许可

- 本仓库使用 MIT 许可，详情见 `LICENSE`

## 贡献

- 欢迎提交 Issue 和 PR

## 常见问题

- 没有看到 key：确认 `.env` 位于 ComfyUI 根目录（与 `custom_nodes` 同级），且包含合法的 `KEY=VALUE`
- 值未刷新：修改 `.env` 后重新触发图或重启 ComfyUI；节点会依据 `mtime` 变化刷新
