#!/usr/bin/env python3
"""从 routes.json 生成 README.md 的项目表与 index.html 的卡片。

用法:
    python scripts/build_route.py            # 重新生成两个文件
    python scripts/build_route.py --check    # 只校验, 不一致时退出码 1

约定: 两个目标文件中被 <!-- xxx:begin --> ... <!-- xxx:end --> 包裹的区块
属于生成区, 不要手改; 区块外的内容原样保留。
"""

from __future__ import annotations

import html
import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
DATA_FILE = ROOT / "routes.json"
README_FILE = ROOT / "README.md"
HTML_FILE = ROOT / "index.html"

# kind → 显示名。新增类型时还要同步 index.html 里的颜色变量与 legend。
KIND_CN = {
    "hw": "电路",      # 电路板设计
    "fw": "固件",      # 烧录到单片机的程序
    "ui": "UI",        # 串口屏工程等界面工程
    "client": "上位机",  # PC / 手机端软件
    "docs": "文档",
}

EXT_ICON = (
    '<span class="ext"><svg viewBox="0 0 24 24">'
    '<path d="M18 13v6a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2V8a2 2 0 0 1 2-2h6"/>'
    '<polyline points="15 3 21 3 21 9"/>'
    '<line x1="10" y1="14" x2="21" y2="3"/>'
    "</svg></span>"
)

STAT_RE = re.compile(r"(<!-- stat:begin -->).*?(<!-- stat:end -->)")


# ---------------------------------------------------------------- 数据

def load_projects() -> tuple[str, list[dict]]:
    data = json.loads(DATA_FILE.read_text(encoding="utf-8"))
    org = data.get("org", "").strip()
    if not org:
        sys.exit("routes.json: 缺少 org 字段")

    projects = data.get("projects") or []
    if not projects:
        sys.exit("routes.json: projects 为空")

    seen: dict[str, str] = {}
    for i, project in enumerate(projects, 1):
        name = (project.get("name") or "").strip()
        if not name:
            sys.exit(f"routes.json: 第 {i} 个项目缺少 name")
        project["name"] = name
        items = project.get("items") or []
        if not items:
            sys.exit(f"routes.json: 「{name}」没有任何仓库条目")
        for item in items:
            kind = item.get("kind")
            if kind not in KIND_CN:
                allowed = " / ".join(KIND_CN)
                sys.exit(f"routes.json: 「{name}」中 kind={kind!r} 非法, 只能是 {allowed}")
            repo = (item.get("repo") or "").strip()
            if not repo:
                sys.exit(f"routes.json: 「{name}」中有一条 repo 为空")
            item["repo"] = repo
            role = (item.get("role") or "").strip()
            if role:
                item["role"] = role
            else:
                item.pop("role", None)
            if repo in seen:
                print(f"  警告: 仓库 {repo} 同时出现在「{seen[repo]}」和「{name}」")
            else:
                seen[repo] = name
    return org, projects


def repo_url(org: str, repo: str) -> str:
    return f"https://github.com/{org}/{repo}"


def type_label(item: dict) -> str:
    """README 表格里的「类型」列: 电路 / 电路 · 主控板"""
    base = KIND_CN[item["kind"]]
    return f"{base} · {item['role']}" if item.get("role") else base


def badge_label(item: dict) -> str:
    """index.html 徽章文字, 有 role 时只显示 role, 否则显示大类"""
    return item.get("role") or KIND_CN[item["kind"]]


# ---------------------------------------------------------------- 渲染

def render_readme(org: str, projects: list[dict]) -> str:
    blocks = []
    for i, project in enumerate(projects, 1):
        rows = [
            f"## {i}. {project['name']}",
            "",
            "| 类型 | 仓库 |",
            "| --- | --- |",
        ]
        for item in project["items"]:
            url = repo_url(org, item["repo"])
            rows.append(f"| {type_label(item)} | [{item['repo']}]({url}) |")
        blocks.append("\n".join(rows))
    return "\n\n".join(blocks)


def render_cards(org: str, projects: list[dict]) -> str:
    cards = []
    for i, project in enumerate(projects):
        delay = 0.04 + i * 0.04
        lines = [
            f'<div class="card" data-idx="{i + 1:02d}" '
            f'style="animation-delay:{delay:.2f}s">',
            f'  <div class="card-head"><h2>{html.escape(project["name"])}</h2></div>',
            '  <div class="card-body">',
        ]
        for item in project["items"]:
            kind = item["kind"]
            name = html.escape(item["repo"])
            url = html.escape(repo_url(org, item["repo"]), quote=True)
            lines += [
                '    <div class="repo">',
                f'      <span class="repo-dot {kind}"></span>',
                f'      <span class="repo-label {kind}">{html.escape(badge_label(item))}</span>',
                f'      <span class="repo-name"><a href="{url}" target="_blank" '
                f'rel="noopener">{name}</a></span>',
                f"      {EXT_ICON}",
                "    </div>",
            ]
        lines += ["  </div>", "</div>"]
        cards.append("\n".join(lines))
    return "\n\n".join(cards)


# ---------------------------------------------------------------- 替换

def splice_block(text: str, tag: str, body: str) -> str:
    """把 <!-- tag:begin --> 与 <!-- tag:end --> 之间的行换成 body"""
    lines = text.split("\n")
    begin = next(
        (i for i, line in enumerate(lines) if line.strip().startswith(f"<!-- {tag}:begin")),
        None,
    )
    end = next(
        (i for i, line in enumerate(lines) if line.strip().startswith(f"<!-- {tag}:end")),
        None,
    )
    if begin is None or end is None or end <= begin:
        sys.exit(f'缺少标记: <!-- {tag}:begin --> / <!-- {tag}:end -->')
    indent = lines[begin][: len(lines[begin]) - len(lines[begin].lstrip())]
    block = [(indent + line if line.strip() else line) for line in body.split("\n")]
    return "\n".join(lines[: begin + 1] + block + lines[end:])


def splice_stat(text: str, label: str) -> str:
    if not STAT_RE.search(text):
        sys.exit("缺少标记: <!-- stat:begin --> ... <!-- stat:end -->")
    return STAT_RE.sub(lambda m: f"{m.group(1)}{label}{m.group(2)}", text)


def read_text(path: Path) -> tuple[str, str]:
    raw = path.read_bytes()
    newline = "\r\n" if b"\r\n" in raw else "\n"
    return raw.decode("utf-8").replace("\r\n", "\n"), newline


def write_text(path: Path, text: str, newline: str) -> None:
    path.write_bytes(text.replace("\n", newline).encode("utf-8"))


def build() -> list[tuple[Path, str]]:
    org, projects = load_projects()
    total = sum(len(p["items"]) for p in projects)
    stat = f"{len(projects)} projects · {total} repos indexed"

    readme, readme_nl = read_text(README_FILE)
    readme = splice_block(readme, "routes", "\n" + render_readme(org, projects) + "\n")

    page, page_nl = read_text(HTML_FILE)
    page = splice_block(page, "routes", "\n" + render_cards(org, projects) + "\n")
    page = splice_stat(page, stat)

    return [(README_FILE, readme, readme_nl), (HTML_FILE, page, page_nl)]


def main() -> int:
    check = "--check" in sys.argv[1:]
    results = build()
    org, projects = load_projects()
    total = sum(len(p["items"]) for p in projects)

    changed = [path for path, text, newline in results
               if path.read_bytes() != text.replace("\n", newline).encode("utf-8")]

    if check:
        if changed:
            print("生成结果与源文件不一致, 请运行 python scripts/build_route.py")
            for path in changed:
                print(f"  - {path.name}")
            return 1
        print(f"OK: {len(projects)} 个项目 / {total} 个仓库, 与 routes.json 一致")
        return 0

    for path, text, newline in results:
        write_text(path, text, newline)

    print(f"已生成: {len(projects)} 个项目 / {total} 个仓库 (org={org})")
    for path in changed or []:
        print(f"  更新 {path.name}")
    if not changed:
        print("  两个文件无变化")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
