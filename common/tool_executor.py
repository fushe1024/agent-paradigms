from typing import Any, Callable, Dict, Optional


class ToolExecutor:
    """工具执行器。

    负责注册、检索并执行智能体可用的工具。
    """

    def __init__(self):
        self.tools: Dict[str, Dict[str, Any]] = {}

    def register_tool(self, name: str, description: str, func: Callable[..., str]) -> None:
        """向工具库中注册一个新工具。

        Args:
            name: 工具名称，供模型在 Action 中引用。
            description: 工具功能描述，会拼接进提示词供模型理解。
            func: 实际执行的函数。
        """
        if name in self.tools:
            print(f"警告：工具 '{name}' 已存在，将被覆盖。")
        self.tools[name] = {"description": description, "func": func}
        print(f"工具 '{name}' 已注册。")

    def get_tool(self, name: str) -> Optional[Callable[..., str]]:
        """按名称获取工具的执行函数，未注册时返回 ``None``。"""
        return self.tools.get(name, {}).get("func")

    def get_available_tools(self) -> str:
        """返回所有已注册工具的格式化描述文本，用于填充提示词。"""
        return "\n".join(
            f"- {name}: {info['description']}"
            for name, info in self.tools.items()
        )
