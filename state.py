from __future__ import annotations

from typing import Any, Literal, Optional

from pydantic import BaseModel, Field


class VideoInfo(BaseModel):
    title: str
    description: str = ""
    published_at: str = ""
    url: str
    source: str = "foxnews"


class KeywordInfo(BaseModel):
    who: list[str] = Field(default_factory=list)
    where: list[str] = Field(default_factory=list)
    when: list[str] = Field(default_factory=list)
    event: str = ""
    key_phrases: list[str] = Field(default_factory=list)
    entities: list[str] = Field(default_factory=list)


class ZhihuEvidence(BaseModel):
    title: str
    url: str
    snippet: str = ""
    highlights: list[str] = Field(default_factory=list)


class GraphState(BaseModel):
    mode: Literal["offline", "online"] = "offline"

    # Step 1
    trending_videos: list[VideoInfo] = Field(default_factory=list)
    video: Optional[VideoInfo] = None

    URL: str = "https://www.youtube.com/watch?v=wWk1kG-8QYY"
    # Step 2
    transcript_raw: str = ""
    transcript_clean: str = ""

    # Step 3
    transcript_summary: str = ""
    keywords: KeywordInfo = Field(default_factory=KeywordInfo)

    # Step 4
    zhihu_results: list[ZhihuEvidence] = Field(default_factory=list)

    # Step 5
    background_context: dict[str, Any] = Field(default_factory=dict)

    # Step 6
    final_script: str = ""

    # Debug
    warnings: list[str] = Field(default_factory=list)
    traces: list[str] = Field(default_factory=list)

