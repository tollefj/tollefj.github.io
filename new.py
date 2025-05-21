import datetime
import os
import re

def slugify(text):
    text = text.lower()
    text = re.sub(r'[^a-z0-9]+', '-', text)
    text = text.strip('-')
    return text

def create_blog_post():
    title = ""
    while not title:
        title = input("enter the blog post title: ").strip()
        if not title:
            print("title cannot be empty. please provide a title.")

    category = input(f"enter the category (default: 'blog'): ").strip()
    if not category:
        category = "blog"

    today = datetime.date.today()
    default_date_str = today.strftime("%Y-%m-%d")
    parsed_date = None
    while parsed_date is None:
        date_input = input(f"enter the date (yyyy-mm-dd, default: {default_date_str}): ").strip()
        if not date_input:
            date_input = default_date_str
        try:
            parsed_date = datetime.datetime.strptime(date_input, "%Y-%m-%d").date()
        except ValueError:
            print("invalid date format. please use yyyy-mm-dd (e.g., 2025-05-21).")

    post_datetime_utc = datetime.datetime.combine(parsed_date, datetime.time(0, 0), tzinfo=datetime.timezone.utc)

    slug = slugify(title)
    post_id = f"{slug}-{int(post_datetime_utc.timestamp())}"
    print(f"generated slug: {slug}")
    print(f"generated post id: {post_id}")

    timestamp_iso = post_datetime_utc.strftime("%Y-%m-%dT%H:%M:%SZ")

    local_timezone = datetime.datetime.now(datetime.timezone.utc).astimezone().tzinfo
    post_datetime_local_display = post_datetime_utc.astimezone(local_timezone)
    timestamp_readable = post_datetime_local_display.strftime("%Y-%m-%d %H:%M")

    year = parsed_date.year
    month = parsed_date.month
    base_dir = os.path.join("posts", str(year), f"{month:02d}") 

    yaml_filename_short = f"{post_id}.yml"
    md_filename_short = f"{post_id}.md"

    yaml_filepath = os.path.join(base_dir, yaml_filename_short)
    md_filepath = os.path.join(base_dir, md_filename_short)

    os.makedirs(base_dir, exist_ok=True)

    yaml_content = f"""title: "{title}"
timestamp_iso: "{timestamp_iso}"
timestamp_readable: "{timestamp_readable}"
category: "{category}"
slug: "{post_id}"
md: "{md_filepath}"
"""
    with open(yaml_filepath, "w", encoding="utf-8") as f:
        f.write(yaml_content)

    md_content = """Some text.
A footnote [^1]
[^1]: some details
"""
    with open(md_filepath, "w", encoding="utf-8") as f:
        f.write(md_content)

    print(f"\nsuccessfully created post '{title}':")
    print(f"  metadata: {yaml_filepath}")
    print(f"  content:  {md_filepath}")

    should_open = input(f"\nedit now? (y/n) [default: yes, ofc]: ").strip().lower()
    if should_open == "n":
        print("cu")
    else:
        os.system(f"vim {md_filepath}")

if __name__ == "__main__":
    create_blog_post()
