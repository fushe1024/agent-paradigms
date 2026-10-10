# --- Plan-and-Solve Agent 使用示例 ---
from common.llm import LLMClient
from PlanAndSolve.agent import PlanAndSolveAgent


def build_agent() -> PlanAndSolveAgent:
    """组装一个可运行的 Plan-and-Solve 智能体。"""
    llm_client = LLMClient()
    return PlanAndSolveAgent(llm_client=llm_client)


if __name__ == "__main__":
    agent = build_agent()

    # 目标问题（AI 大模型方向）：可拆成少量有序子步骤，每步答案都很短，
    # 既能体现「先规划、再执行」，又能快速跑完，适合入门演示。
    question = (
        "某公司每天调用大模型 API 1000 次，每次消耗约 1000 个输入 token 和 500 个输出 token。"
        "输入价格 1 元/百万 token，输出价格 2 元/百万 token，求每天的总成本。"
    )
    agent.run(question)
