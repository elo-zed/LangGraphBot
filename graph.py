from __future__ import annotations

from langgraph.graph import END, StateGraph

from agents.context_aggregation_agent import context_aggregation_agent
from agents.keyword_extraction_agent import keyword_extraction_agent
from agents.script_generation_agent import script_generation_agent
from agents.subtitle_agent import subtitle_agent
from agents.trending_video_agent import trending_video_agent
from agents.zhihu_search_agent import zhihu_search_agent
from config import AppConfig
from state import GraphState
from utils.http import HttpClient
from utils.llm import LLMClient


def build_graph(
    *,
    cfg: AppConfig,
    top_k: int = 10,
    video_url: str | None = None,
):
    http = HttpClient(
        timeout_seconds=cfg.http_timeout_seconds,
        retries=cfg.http_retries,
        user_agent=cfg.http_user_agent,
    )
    llm = LLMClient(
        api_key=cfg.openai_api_key,
        base_url=cfg.openai_base_url,
        model=cfg.openai_model,
        timeout_seconds=cfg.http_timeout_seconds,
    )

    graph = StateGraph(GraphState)

    # graph.add_node(
    #     "trending_video",
    #     lambda s: trending_video_agent(s, http=http, top_k=top_k, video_url=video_url),
    # )
    graph.add_node("subtitle", lambda s: subtitle_agent(s))
    graph.add_node("keyword_extraction", lambda s: keyword_extraction_agent(s, llm=llm))
    graph.add_node("zhihu_search", lambda s: zhihu_search_agent(s, http=http, top_k=5))
    graph.add_node("context_aggregation", lambda s: context_aggregation_agent(s, llm=llm))
    graph.add_node("script_generation", lambda s: script_generation_agent(s, llm=llm))

    graph.set_entry_point("subtitle") # 开始节点
    #graph.add_edge("trending_video", "subtitle")
    graph.add_edge("subtitle", "keyword_extraction")
    graph.add_edge("keyword_extraction", "zhihu_search")
    graph.add_edge("zhihu_search", "context_aggregation")
    graph.add_edge("context_aggregation", "script_generation")
    graph.add_edge("script_generation", END) # 结束节点

    return graph.compile()

