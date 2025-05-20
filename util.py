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

def update_html(html, html_module, backlink="../index.html"):
    html = html.replace("{CONTENT}", html_module)
    html = html.replace("{HREF}", backlink)
    # all other sections need to be replaced if we want to use the same template
    html = html.replace("{TOOLS}", "")
    return html

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
    html = update_html(html, _html)
    with open(post_id, "w") as f:
        f.write(html)


def gh_md_tool(html, location):
    _html = strip_spaces(
        f"""
<div>
  <div class="container centered">
    <div>
      <!-- <label for="issue-url">github issue url</label> -->
      <input type="text" id="issue-url" placeholder="github issue url" />
    </div>
    <div>
      <button id="convert">copy .md</button>
    </div>
  </div>
  <p class="error" id="error"></p>
  <script type="module" src="gh-to-md.js"></script>
  <p class="centered">A reworked implementation of the <a href="https://github.com/simonw/tools/blob/main/github-issue-to-markdown.html">&nbsp;tool by Simon Willison</a></p>
</div>
"""
    )
    html = update_html(html, _html)
    with open(location, "w") as f:
        f.write(html)


def add_tools(html, template):
    _html = ["<h2>Tools</h2>"]
    tools = [
        {
            "title": "github issue to .md",
            "location": "posts/gh-md-tool.html",
            "create_fn": gh_md_tool,
        }
    ]

    for tool in tools:
        # first populate the html under /posts 
        tool["create_fn"](template, tool["location"])
        #  then link to it on the home page
        _html.append(
            strip_spaces(
                f"<h2 class='linkify'><a href='{tool['location']}'>{tool['title']}</a></h2>"
            )
        )

    _html = strip_spaces("\n".join(_html))
    return html.replace("{TOOLS}", _html)


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
