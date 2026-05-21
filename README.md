
## MaiBot Socket.IO 配置

本插件已切换到新版 `maim_message` 的 Socket.IO API Server。原有 `allow_group_list` 白名单功能仍保留，留空表示不过滤群聊。

### NoneBot 侧配置

在 NoneBot 配置中设置插件参数：

```env
url=ws://127.0.0.1:8090/ws
api_key=nonebot-adapter
platfrom=nonebot-qq
allow_group_list=[]
```

如果 MaiBot 和 NoneBot 不在同一台机器，把 `127.0.0.1` 改成 MaiBot 所在机器的地址。`platfrom` 是历史拼写，当前仍按原字段名保留。

### MaiBot 侧配置

编辑 MaiBot 的 `config/bot_config.toml`。

机器人账号映射需要包含 NoneBot 平台名和机器人 QQ：

```toml
platforms = ["nonebot-qq:你的机器人QQ号"]
```

新版 Socket.IO API Server 建议这样配置：

```toml
[maim_message]
ws_server_host = "127.0.0.1"
ws_server_port = 8091
auth_token = []

enable_api_server = true
api_server_host = "0.0.0.0"
api_server_port = 8090
api_server_use_wss = false
api_server_cert_file = ""
api_server_key_file = ""
api_server_allowed_api_keys = ["nonebot-adapter"]
```

`api_server_allowed_api_keys` 必须包含 NoneBot 侧的 `api_key`。如果设置为空列表，MaiBot 会允许所有 API Key 连接，不建议公网使用。

### 手动安装 GitHub 版 maim_message

在 MaiBot 的 Python 环境中执行：

```powershell
python -m pip install --upgrade --force-reinstall git+https://github.com/MaiM-with-u/maim_message.git
```

在 NoneBot 的虚拟环境中执行：

```powershell
.\.venv\Scripts\python.exe -m pip install --upgrade --force-reinstall git+https://github.com/MaiM-with-u/maim_message.git
```

检查版本和安装路径：

```powershell
python -c "import maim_message, socketio; print(maim_message.__version__); print(maim_message.__file__); print(socketio.AsyncClient)"
```

如果输出能正常导入 `socketio.AsyncClient`，说明 Socket.IO 依赖可用。

### 端口说明

- `8090`：新版 Socket.IO API Server，本插件连接这个端口。
- `8091`：旧版 Legacy WS Server，本插件不再连接这个端口。

修改配置后，需要重启 MaiBot 和 NoneBot。
