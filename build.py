import yaml
import re
from datetime import datetime
import os
from util import article_html, meta_html, snapshot

POSTS_DIR = "posts"
TEMPLATE = "templates/index.html"
OUTPUT = "index.html"

if __name__ == "__main__":
    snapshot()

    with open(TEMPLATE, "r") as f:
        HTML = f.read()

    post_links = []
    for root, dirs, files in os.walk(POSTS_DIR):
        for file in files:
            if "yml" in file:
                if not os.path.exists(os.path.join(root, file.replace("yml", "md"))):
                    print(f"Missing md file for {file}")
                    continue
                _path = os.path.join(root, file)
                _path_md = os.path.join(root, file.replace("yml", "md"))

                _yml = yaml.safe_load(open(_path, "r"))
                _md = open(_path_md).read()
                post_id = _yml["title"].replace(" ", "-")
                post_id = re.sub(r"[^a-zA-Z0-9-]", "", post_id)
                post_id = f"posts/{post_id}.html"
                # create the standalone article
                article_html(HTML, _yml, _md, post_id)
                # add the post to the list for sorting links
                post_links.append(
                    {
                        "timestamp": _yml["timestamp_iso"],
                        "html": meta_html(_yml, post_id),
                    }
                )

    posts_sorted = sorted(
        post_links,
        key=lambda x: datetime.fromisoformat(x["timestamp"]),
        reverse=True,
    )
    posts_html = [p["html"] for p in posts_sorted]
    posts_html = "\n".join(posts_html)

    html = HTML.replace("{CONTENT}", posts_html)
    html = html.replace("{HREF}", OUTPUT)
    with open(OUTPUT, "w") as f:
        f.write(html)
