# --- Reflection Agent 使用示例 ---
from common.llm import LLMClient
from Reflection.agent import ReflectionAgent


def build_agent(max_iterations: int = 2) -> ReflectionAgent:
    """组装一个可运行的 Reflection 智能体。"""
    llm_client = LLMClient()
    return ReflectionAgent(llm_client=llm_client, max_iterations=max_iterations)


if __name__ == "__main__":
    agent = build_agent(max_iterations=2)

    # 目标问题（AI 大模型方向）：Top-K 采样是 LLM 解码的经典操作，
    # 代码短、优化点明确（排序 → 堆），反思与优化都很快，适合快速演示。
    task = (
        "编写一个 Python 函数，实现大模型解码时的 Top-K 采样："
        "给定一组词的概率分布，返回概率最高的 K 个词的索引。"
    )
    agent.run(task)
