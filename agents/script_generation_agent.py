from __future__ import annotations

import json

from state import GraphState
from utils.llm import DeepSeekClient


def script_generation_agent(state: GraphState, llm: DeepSeekClient) -> dict:

    with open("agents/transcript.txt","r") as f:
        transcript_str = f.readlines()

    prompt = f"""
        根据下面的视频字幕，总结30s-90s 时长的口播内容，内容只包含一个主题事件，尽量说清楚时间、地点、哪些人物、事件的目的，如果没有时间就用当天的时间，不要有任何评论

        字幕：
        {transcript_str}
        """.strip()


    content = llm.chat_completion(prompt,content="你是短视频口播脚本写手，输出适合口播的中文脚本。"    
    )
    return content



if __name__=="__main__":
    s = GraphState()
    llm = DeepSeekClient()
    content = script_generation_agent(s,llm)
    print(content)


