from __future__ import annotations

import json
from pathlib import Path

import typer
from rich.console import Console

from config import load_config
from graph import build_graph
from state import GraphState
from utils.paths import project_root


app = typer.Typer(add_completion=False)
console = Console()


@app.command()
def run(
    mode: str = typer.Option("offline", help="offline / online"),
    top_k: int = typer.Option(1, help="拉取热门视频条数"),
    video_url: str | None = typer.Option("https://www.youtube.com/watch?v=wWk1kG-8QYY", help="指定 Fox News 视频 URL"),
) -> None:
    cfg = load_config()
    out_dir_cfg = Path(cfg.output_dir)
    out_dir = out_dir_cfg if out_dir_cfg.is_absolute() else (project_root() / out_dir_cfg)
    out_dir.mkdir(parents=True, exist_ok=True)

    graph = build_graph(cfg=cfg, top_k=top_k, video_url=video_url)

    state = GraphState(mode=("online" if mode == "online" else "offline"))
    result = graph.invoke(state)

    # result 可能是 dict 或 GraphState，做兼容
    if isinstance(result, dict):
        final_state = GraphState(**result)
    else:
        final_state = result

    (out_dir / "result.json").write_text(
        json.dumps(final_state.model_dump(), ensure_ascii=False, indent=2),
        encoding="utf-8",
    )
    (out_dir / "script.txt").write_text(final_state.final_script or "", encoding="utf-8")

    console.print(f"[bold green]完成[/bold green] 输出目录：{out_dir.resolve()}")
    if final_state.video:
        console.print(f"[bold]视频[/bold]：{final_state.video.title}")
        console.print(f"[bold]链接[/bold]：{final_state.video.url}")
    if final_state.warnings:
        console.print("[bold yellow]Warnings[/bold yellow]")
        for w in final_state.warnings:
            console.print(f"- {w}")
    console.print("\n[bold]脚本预览[/bold]\n")
    console.print(final_state.final_script[:1200] + ("..." if len(final_state.final_script) > 1200 else ""))


if __name__ == "__main__":
    app()

