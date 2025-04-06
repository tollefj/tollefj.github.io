"""
---
layout: post
title:  "title here"
date:   2025-04-04 18:03:00 +0100
categories: blog
tags: [tags separated by space]
description:  "desc"
---

# title here
_description_
"""

import os
import sys
import argparse
import typing
import datetime

"""
usage:
python create.py "title" "description" "tags separated by space"
"""

out_dir = "_posts"

def format_time():
    now = datetime.datetime.now()
    return now.strftime("%Y-%m-%d %H:%M:%S +0100")

def create(title: str, description: str, tags: typing.List[str], cat: str = "blog") -> None:
    current_time = format_time()
    
    post = f"""---
layout: post
title:  "{title}"
date:   {current_time}
categories: {cat}
tags: [{', '.join(f'{tag}' for tag in tags)}]
description:  "{description}"
---
_{description}_

*content goes here*

"""

    filename = f"{datetime.datetime.now().strftime('%Y-%m-%d')}-{title.replace(' ', '-')}.md"
    filepath = os.path.join(out_dir, filename)

    with open(filepath, "w") as file:
        file.write(post)
    
    print(f"Post created: {filepath}")


def main():
    parser = argparse.ArgumentParser(description="Create a new blog post.")
    parser.add_argument("title", type=str, help="Title of the post")
    parser.add_argument("description", type=str, help="Description of the post")
    parser.add_argument("tags", type=str, nargs='+', help="Tags for the post")
    parser.add_argument("--cat", type=str, default="blog", help="Category of the post (default: blog)")

    args = parser.parse_args()

    if not os.path.exists(out_dir):
        os.makedirs(out_dir)

    create(args.title, args.description, args.tags, args.cat)


if __name__ == "__main__":
    main()

