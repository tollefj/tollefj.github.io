wanting to move to pure html, embarrassingly from the website [justfuckingusehtml](https://justfuckingusehtml.com/), I ended up moving from the typical jekyll gh-pages setup, to my own local md files with metadata through a ./new.sh script, and then a python pipeline building and injecting the resulting html files into a single `index.html`.

the workflow (new blog):

```txt
./new.sh "some title" --> md + yml meta file.
python new.py --> interactively asks you for content/date/...
edit `posts/<year>/<month>/some-title.md`
python build.py --> index.html
push changes
```
___

### project structure
```bash
.
├── modules
│   └── gh-to-md.html
├── posts
│   ├── 2023
│   │   ...
│   ├── 2024
│   ├── 2025
│   │   └── 05
│   │       ├── LLM.md
│   │       └── LLM.yml
│   ├── gh-md-tool.html
│   └── LLM-workflows.html
├── scripts
│   └── gh-to-md.js
├── styles
│   ├── gh-to-md.css
│   └── style.css
├── templates
│   ├── article.html
│   ├── index.html
│   └── meta.html
├── index.html
├── new.sh
├── reqs.txt
├── build.py
└── util.py
```

### `new.sh`
```bash
#!/bin/bash

if [ "$#" -ne 1 ]; then
  echo "Something went wrong. Example: ./new.sh \"some title\""
  exit 1
fi

TITLE="$1"
CATEGORY="blog"

SLUG=$(echo "$TITLE" | iconv -t ascii//TRANSLIT | sed -E 's/[^a-zA-Z0-9]+/-/g' | sed -E 's/^-+|-+$//g' | tr '[:upper:]' '[:lower:]')
POST_ID="${SLUG}-$(date -u +"%s")"

TIMESTAMP_ISO=$(date -u +"%Y-%m-%dT%H:%M:%SZ")
TIMESTAMP_READABLE=$(date +"%Y-%m-%d %H:%M")

YAML_FILENAME="posts/${POST_ID}.yml"
MD_FILENAME="posts/${POST_ID}.md"

mkdir -p posts
mkdir -p posts/$(date +%Y)/$(date +%m)

cat > "$YAML_FILENAME" <<EOF
title: "$TITLE"
timestamp_iso: "$TIMESTAMP_ISO"
timestamp_readable: "$TIMESTAMP_READABLE"
category: "$CATEGORY"
slug: "$POST_ID"
md: "$MD_FILENAME"
EOF

# this is just a placeholder md file
cat > "$MD_FILENAME" <<EOF
Some text.
A footnote [^1]
[^1]: some details
EOF

mv "$YAML_FILENAME" "posts/$(date +%Y)/$(date +%m)/$POST_ID.yml"
mv "$MD_FILENAME" "posts/$(date +%Y)/$(date +%m)/$POST_ID.md"

echo "Successfully created post '$TITLE':"
echo "  Metadata: $YAML_FILENAME"
echo "  Content:  $MD_FILENAME"
```

all pages here are sourced from the template `templates/index.html`, where various content is replaced in a naive but efficient way for a simple site like this. it's all string manipulation, without relying on external libraries outside of [markdown-it](https://github.com/markdown-it/markdown-it) for parsing md into html.

### tools
the `gh-to-md`-tool is an example of how additional sections can be added, where the html is iframe-like, containing an incomplete module to be injected into the homepage. this is done through a `add_tools()`-step, as follows:

```python

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
    # inject:
    return html.replace("{TOOLS}", _html)
```
