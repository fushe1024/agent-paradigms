import re
from typing import Optional, Tuple

from ReAct.prompt import REACT_PROMPT_TEMPLATE


class ReActAgent:
    """ReAct 智能体：在 Thought → Action → Observation 之间循环，直至得出结论。"""

    def __init__(self, llm_client, tool_executor, max_steps: int = 5):
        self.llm_client = llm_client
        self.tool_executor = tool_executor
        self.max_steps = max_steps
        self.history: list[str] = []

    def run(self, question: str) -> Optional[str]:
        """运行 ReAct 智能体回答指定问题。

        Args:
            question: 用户提出的问题。

        Returns:
            最终答案；未能在 ``max_steps`` 内得出结论时返回 ``None``。
        """
        self.history = []  # 每次运行前重置历史记录
        current_step = 0

        while current_step < self.max_steps:
            current_step += 1
            print(f"--- 第 {current_step} 步 ---")

            # 1. 格式化提示词
            prompt = REACT_PROMPT_TEMPLATE.format(
                tools=self.tool_executor.get_available_tools(),
                question=question,
                history="\n".join(self.history),
            )

            # 2. 调用 LLM 进行推理
            response_text = self.llm_client.think(messages=[{"role": "user", "content": prompt}])
            if not response_text:
                print("错误：LLM 未能返回有效响应。")
                break

            # 3. 解析 LLM 的输出
            thought, action = self._parse_output(response_text)
            if thought:
                print(f"思考：{thought}")
            if not action:
                print("警告：未能解析出有效的 Action，流程终止。")
                break

            # 4. 执行 Action
            if action.startswith("Finish"):
                # Finish 指令：提取最终答案并结束
                match = re.match(r"Finish\[(.*)\]", action, re.DOTALL)
                final_answer = match.group(1) if match else action
                print(f"🎉 最终答案：{final_answer}")
                return final_answer

            tool_name, tool_input = self._parse_action(action)
            if not tool_name:
                print("警告：Action 格式无法解析，流程终止。")
                break

            print(f"🎬 行动：{tool_name}[{tool_input}]")

            tool_function = self.tool_executor.get_tool(tool_name)
            if not tool_function:
                observation = f"错误：未找到名为 '{tool_name}' 的工具。"
            else:
                observation = tool_function(tool_input)  # 调用真实工具

            print(f"👀 观察：{observation}")

            # 将本轮的 Action 与 Observation 追加到历史记录
            self.history.append(f"Action: {action}")
            self.history.append(f"Observation: {observation}")

        # 循环结束：达到最大步数仍未得到最终答案
        print("已达到最大步数，流程终止。")
        return None

    def _parse_output(self, text: str) -> Tuple[Optional[str], Optional[str]]:
        """解析 LLM 输出，提取 Thought 与 Action。"""
        # Thought 匹配到 Action 或文本末尾
        thought_match = re.search(r"Thought:\s*(.*?)(?=\nAction:|$)", text, re.DOTALL)
        # Action 匹配到文本末尾
        action_match = re.search(r"Action:\s*(.*?)$", text, re.DOTALL)
        thought = thought_match.group(1).strip() if thought_match else None
        action = action_match.group(1).strip() if action_match else None
        return thought, action

    def _parse_action(self, action_text: str) -> Tuple[Optional[str], Optional[str]]:
        """解析 Action 字符串，提取工具名称与输入。"""
        match = re.match(r"(\w+)\[(.*)\]", action_text, re.DOTALL)
        if match:
            return match.group(1), match.group(2)
        return None, None
