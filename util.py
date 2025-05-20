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


def strip_spaces(html):
    # html = re.sub(r"\s+", " ", html)
    html = html.strip()
    return html


def get_readable_time(timestamp):
    return datetime.datetime.fromisoformat(timestamp).strftime("%B %d %Y @ %H:%M")


md = (
    MarkdownIt("commonmark", {"breaks": True, "html": True})
    .use(front_matter_plugin)
    .use(footnote_plugin)
    .enable("table")
)


def article_html(html, _yml, _md, post_id):
    _html = strip_spaces(
        f"""
<article>
    <h2>{_yml['title']}</h2>
    <div class="meta">
        <p id="date">{get_readable_time(_yml["timestamp_iso"])}</p>
    </div>
    <div class="content">{md.render(_md)}</div>
</article>
"""
    )
    html = html.replace("{CONTENT}", _html)
    html = html.replace("{HREF}", "../index.html")

    with open(post_id, "w") as f:
        f.write(html)


def meta_html(_yml, post_id):
    html = strip_spaces(
        f"""
<h2 class="linkify"><a href="{post_id}">{_yml['title']}</a></h2>
<div class="meta">
    <p id="date">{get_readable_time(_yml["timestamp_iso"])}</p>
</div>
"""
    )
    return html
