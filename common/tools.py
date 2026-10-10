import os

import requests
from dotenv import load_dotenv

# 加载 .env 文件中的环境变量
load_dotenv()


def search(query: str) -> str:
    """基于 Kimi（Moonshot）的联网搜索工具。

    Args:
        query: 待检索的关键词或问题。

    Returns:
        若干条搜索结果拼接成的文本；出错时返回以 ``错误:`` 开头的说明。
    """
    print(f"🔍 正在执行 [Kimi WebSearch] 网页搜索：{query}")
    try:
        api_key = os.getenv("MOONSHOT_API_KEY")
        base_url = os.getenv("MOONSHOT_BASE_URL")

        if not api_key or not base_url:
            return "错误：MOONSHOT_API_KEY、MOONSHOT_BASE_URL 未在 .env 文件中配置。"

        payload = {
            "text_query": query,
            "limit": 5,
            "timeout_seconds": 10,
        }
        headers = {
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json",
        }
        resp = requests.post(base_url, json=payload, headers=headers, timeout=12)
        resp.raise_for_status()
        results = resp.json()

        # 返回结构中外层 key 为 search_results
        if results.get("search_results"):
            snippets = []
            for idx, item in enumerate(results["search_results"][:3]):
                title = item.get("title", "")
                snippet = item.get("snippet", "")
                url = item.get("url", "")
                date = item.get("date", "")
                site_name = item.get("site_name", "")
                snippets.append(
                    f"[{idx + 1}] {title}\n"
                    f"站点：{site_name} | 发布时间：{date}\n"
                    f"来源：{url}\n"
                    f"摘要：{snippet}"
                )
            return "\n\n".join(snippets)

        return f"对不起，没有找到关于 '{query}' 的信息。"

    except Exception as e:  # noqa: BLE001 - 工具层统一兜底，把错误交还给模型
        return f"搜索时发生错误：{e}"
