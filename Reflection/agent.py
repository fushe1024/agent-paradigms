from Reflection.memory import ReflectionMemory
from Reflection.prompt import (
    INITIAL_PROMPT_TEMPLATE,
    REFLECT_PROMPT_TEMPLATE,
    REFINE_PROMPT_TEMPLATE,
)


class ReflectionAgent:
    """Reflection 智能体：生成 → 反思 → 优化，循环迭代直至满意。"""

    def __init__(self, llm_client, max_iterations: int = 3):
        self.llm_client = llm_client
        self.memory = ReflectionMemory()
        self.max_iterations = max_iterations

    def run(self, task: str) -> str:
        """运行反思式迭代，生成并持续优化解决方案。

        Args:
            task: 待完成的任务描述。

        Returns:
            迭代结束后的最终输出（通常为代码）。
        """
        print(f"\n--- 开始处理任务 ---\n任务：{task}")

        # --- 1. 初始执行 ---
        print("\n--- 正在进行初始尝试 ---")
        initial_prompt = INITIAL_PROMPT_TEMPLATE.format(task=task)
        initial_output = self._get_llm_response(initial_prompt)
        self.memory.add_record("execution", initial_output)

        # --- 2. 迭代循环：反思与优化 ---
        for i in range(self.max_iterations):
            print(f"\n--- 第 {i + 1}/{self.max_iterations} 轮迭代 ---")

            # a. 反思
            print("\n-> 正在进行反思...")
            last_output = self.memory.get_last_execution()
            reflect_prompt = REFLECT_PROMPT_TEMPLATE.format(task=task, code=last_output)
            feedback = self._get_llm_response(reflect_prompt)
            self.memory.add_record("reflection", feedback)

            # b. 判断是否可以停止
            if "无需改进" in feedback:
                print("\n✅ 评审认为已无需改进，任务完成。")
                break

            # c. 优化
            print("\n-> 正在进行优化...")
            refine_prompt = REFINE_PROMPT_TEMPLATE.format(
                task=task,
                last_code_attempt=last_output,
                feedback=feedback,
            )
            refined_output = self._get_llm_response(refine_prompt)
            self.memory.add_record("execution", refined_output)

        final_output = self.memory.get_last_execution()
        print(f"\n--- 任务完成 ---\n最终结果：\n{final_output}")
        return final_output

    def _get_llm_response(self, prompt: str) -> str:
        """辅助方法：调用 LLM 并返回完整的流式响应文本。"""
        messages = [{"role": "user", "content": prompt}]
        return self.llm_client.think(messages=messages) or ""
