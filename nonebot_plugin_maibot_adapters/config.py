from pydantic import BaseModel


class Config(BaseModel):
    """Plugin Config Here"""
    url : str = "ws://127.0.0.1:8090/ws"  # MaiBot Additional API Server Socket.IO 地址
    api_key : str = "nonebot-adapter"      # 需要与 MaiBot api_server_allowed_api_keys 匹配
    platfrom :str = "nonebot-qq"    #如果你不知道这是什么那你就不要动它
    allow_group_list :list[str]  = []     #留空则为不启动QQ端白名单
