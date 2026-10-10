"""公共基础能力包。

集中放置所有范式共享的组件，并在包初始化时统一处理标准输出编码，
避免 Windows 默认 GBK 控制台下输出中文或 emoji 时抛出 ``UnicodeEncodeError``。
"""

import sys

# 在导入 common 下的任意模块时自动生效（common.llm / common.tools 等）。
for _stream in (sys.stdout, sys.stderr):
    if hasattr(_stream, "reconfigure"):
        _stream.reconfigure(encoding="utf-8")
