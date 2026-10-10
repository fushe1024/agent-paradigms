# --- ReAct Agent 使用示例 ---
from common.llm import LLMClient
from common.tool_executor import ToolExecutor
from common.tools import search
from ReAct.agent import ReActAgent


def build_agent(max_steps: int = 5) -> ReActAgent:
    """组装一个可运行的 ReAct 智能体。"""
    # 1. 初始化大模型客户端
    llm_client = LLMClient()

    # 2. 初始化工具执行器并注册工具
    tool_executor = ToolExecutor()
    tool_executor.register_tool(
        name="Search",
        description="基于 Kimi（Moonshot）的联网搜索引擎。输入为查询关键词，返回相关网页的标题、来源与摘要。",
        func=search,
    )

    # 3. 初始化 ReAct 智能体
    return ReActAgent(llm_client=llm_client, tool_executor=tool_executor, max_steps=max_steps)


if __name__ == "__main__":
    agent = build_agent(max_steps=5)

    # 目标问题（AI 大模型方向）：时效性强、需要联网检索，但足够聚焦、答案简短，适合快速演示。
    question = "OpenAI 最新发布的大语言模型是什么？"
    agent.run(question)
