from typing import Any, Dict, List, Optional


class ReflectionMemory:
    """短期记忆模块，按时间顺序记录智能体的执行与反思轨迹。"""

    def __init__(self):
        self.records: List[Dict[str, Any]] = []

    def add_record(self, record_type: str, content: str) -> None:
        """向记忆中添加一条新记录。

        Args:
            record_type: 记录类型，``"execution"``（执行）或 ``"reflection"``（反思）。
            content: 记录内容，例如生成的代码或评审反馈。
        """
        self.records.append({"type": record_type, "content": content})
        print(f"📝 记忆已更新，新增一条 '{record_type}' 记录。")

    def get_trajectory(self) -> str:
        """将所有记录格式化为连贯文本，用于构建提示词。"""
        trajectory_parts = []
        for record in self.records:
            if record["type"] == "execution":
                trajectory_parts.append(f"--- 上一轮尝试（代码）---\n{record['content']}")
            elif record["type"] == "reflection":
                trajectory_parts.append(f"--- 评审员反馈 ---\n{record['content']}")
        return "\n\n".join(trajectory_parts)

    def get_last_execution(self) -> Optional[str]:
        """返回最近一次的执行结果（如最新生成的代码），不存在时返回 ``None``。"""
        for record in reversed(self.records):
            if record["type"] == "execution":
                return record["content"]
        return None
