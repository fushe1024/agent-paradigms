import ast
from typing import List, Optional

from PlanAndSolve.prompt import PLANNER_PROMPT_TEMPLATE, EXECUTOR_PROMPT_TEMPLATE


class Planner:
    """规划器：将复杂问题拆解成有序的子任务列表。"""

    def __init__(self, llm_client):
        self.llm_client = llm_client

    def plan(self, question: str) -> List[str]:
        """根据用户问题生成行动计划。

        Args:
            question: 用户提出的问题。

        Returns:
            子任务字符串列表；解析失败时返回空列表。
        """
        prompt = PLANNER_PROMPT_TEMPLATE.format(question=question)
        messages = [{"role": "user", "content": prompt}]

        print("--- 正在生成计划 ---")
        response_text = self.llm_client.think(messages=messages) or ""

        print(f"✅ 计划已生成：\n{response_text}")

        # 解析 LLM 输出的列表字符串
        try:
            # 提取 ```python 与 ``` 之间的内容
            plan_str = response_text.split("```python")[1].split("```")[0].strip()
            # 使用 ast.literal_eval 安全地把字符串转换为 Python 列表
            plan = ast.literal_eval(plan_str)
            return plan if isinstance(plan, list) else []
        except (ValueError, SyntaxError, IndexError) as e:
            print(f"❌ 解析计划时出错：{e}")
            print(f"原始响应：{response_text}")
            return []
        except Exception as e:  # noqa: BLE001 - 规划失败不应中断整体流程
            print(f"❌ 解析计划时发生未知错误：{e}")
            return []


class Executor:
    """执行器：严格按照计划逐步求解问题。"""

    def __init__(self, llm_client):
        self.llm_client = llm_client

    def execute(self, question: str, plan: List[str]) -> Optional[str]:
        """按计划逐步执行并返回最终答案。

        Args:
            question: 原始问题。
            plan: 规划器生成的子任务列表。

        Returns:
            最后一步的输出，即最终答案。
        """
        history = ""  # 累积历史步骤与结果的字符串
        response_text = ""

        print("\n--- 正在执行计划 ---")

        for i, step in enumerate(plan):
            print(f"\n-> 正在执行步骤 {i + 1}/{len(plan)}：{step}")

            prompt = EXECUTOR_PROMPT_TEMPLATE.format(
                question=question,
                plan=plan,
                history=history if history else "无",  # 第一步时历史为空
                current_step=step,
            )
            messages = [{"role": "user", "content": prompt}]

            response_text = self.llm_client.think(messages=messages) or ""

            # 更新历史记录，为下一步做准备
            history += f"步骤 {i + 1}: {step}\n结果: {response_text}\n\n"

            print(f"✅ 步骤 {i + 1} 已完成，结果：{response_text}")

        # 最后一步的响应即最终答案
        return response_text


class PlanAndSolveAgent:
    """Plan-and-Solve 智能体：先规划，再逐步执行。"""

    def __init__(self, llm_client):
        """初始化智能体，并创建规划器与执行器实例。"""
        self.llm_client = llm_client
        self.planner = Planner(self.llm_client)
        self.executor = Executor(self.llm_client)

    def run(self, question: str) -> Optional[str]:
        """运行完整流程：先规划，后执行。

        Args:
            question: 用户提出的问题。

        Returns:
            最终答案；计划生成失败时返回 ``None``。
        """
        print(f"\n--- 开始处理问题 ---\n问题：{question}")

        # 1. 生成计划
        plan = self.planner.plan(question)
        if not plan:
            print("\n--- 任务终止 ---\n无法生成有效的行动计划。")
            return None

        # 2. 执行计划
        final_answer = self.executor.execute(question, plan)

        print(f"\n--- 任务完成 ---\n最终答案：{final_answer}")
        return final_answer
