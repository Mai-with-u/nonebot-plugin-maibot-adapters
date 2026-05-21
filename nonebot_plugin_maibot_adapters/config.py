from pydantic import BaseModel


class Config(BaseModel):
    """Plugin Config Here"""

    url: str = "ws://127.0.0.1:8090/ws"  # MaiBot Additional API Server Socket.IO 地址
    api_key: str = "nonebot-adapter"  # 需要与 MaiBot api_server_allowed_api_keys 匹配
    platfrom: str = "nonebot-qq"  # 历史字段名，保持兼容
    allow_group_list: list[str | int] = []  # 留空则不启用 QQ 端白名单
