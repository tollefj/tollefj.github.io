import re
import datetime
import os
from markdown_it import MarkdownIt
from mdit_py_plugins.front_matter import front_matter_plugin
from mdit_py_plugins.footnote import footnote_plugin
import shutil


def snapshot():
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    snapshot_path = f"old/posts/{timestamp}"
    print(f"Snapshotting posts to {snapshot_path}")
    os.makedirs(snapshot_path, exist_ok=True)
    for file in os.listdir("posts"):
        print(f"Checking {file}")
        if file.endswith(".html"):
            src = os.path.join("posts", file)
            dst = os.path.join(snapshot_path, file)
            print(f"Moving {src} to {dst}")
            shutil.move(src, dst)


def update_html(html, html_module, root="../"):
    return (
        html.replace("{CONTENT}", html_module)
        .replace("{ROOT}", root)
        .replace("{TOOLS}", "")
    )


def strip_spaces(html):
    # html = re.sub(r"\s+", " ", html)
    html = html.strip()
    return html


def get_readable_time(timestamp):
    return datetime.datetime.fromisoformat(timestamp).strftime("%B %d %Y @ %H:%M")


def article_html(html, _yml, _md, post_id):
    md = (
        MarkdownIt("commonmark", {"breaks": True, "html": True})
        .use(front_matter_plugin)
        .use(footnote_plugin)
        .enable("table")
    )

    with open("templates/article.html", "r") as f:
        html = update_html(
            html,
            f.read().format(
                title=_yml["title"],
                date=get_readable_time(_yml["timestamp_iso"]),
                content=md.render(_md),
            ),
        )
        with open(post_id, "w") as f:
            f.write(html)


def gh_md_tool(html, location):
    with open("modules/gh-to-md.html", "r") as f:
        html = update_html(html, f.read())
        with open(location, "w") as f:
            f.write(html)


def add_tools(html, template):
    _html = ["<h2>Tools</h2>"]
    tools = [
        {
            "title": "github issue to .md",
            "location": "posts/gh-md-tool.html",
            "build": gh_md_tool,
        }
    ]

    for tool in tools:
        # first build the html under /posts
        tool["build"](template, tool["location"])
        #  then link to it on the home page
        _html.append(
            strip_spaces(
                f"<h2 class='linkify'><a href='{tool['location']}'>{tool['title']}</a></h2>"
            )
        )

    _html = strip_spaces("\n".join(_html))
    return html.replace("{TOOLS}", _html)


def meta_html(_yml, post_id):
    title = _yml["title"]
    date = get_readable_time(_yml["timestamp_iso"])
    with open("templates/meta.html", "r") as f:
        html = f.read().format(
            title=title,
            href=post_id,
            date=date,
        )
        return html
