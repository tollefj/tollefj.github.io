#!/bin/bash
if [ "$#" -ne 1 ]; then
  echo "Something went wrong. Example: ./new.sh \"some title\""
  exit 1
fi

TITLE="$1"
CATEGORY="blog"

SLUG=$(echo "$TITLE" | iconv -t ascii//TRANSLIT | sed -E 's/[^a-zA-Z0-9]+/-/g' | sed -E 's/^-+|-+$//g' | tr '[:upper:]' '[:lower:]')
echo "Slug: $SLUG"

POST_ID="${SLUG}-$(date -u +"%s")"

TIMESTAMP_ISO=$(date -u +"%Y-%m-%dT%H:%M:%SZ")
TIMESTAMP_READABLE=$(date +"%Y-%m-%d %H:%M")

YAML_FILENAME="posts/${POST_ID}.yml"
MD_FILENAME="posts/${POST_ID}.md"

mkdir -p posts
mkdir -p posts/$(date +%Y)/$(date +%m)

# metadata file
cat > "$YAML_FILENAME" <<EOF
title: "$TITLE"
timestamp_iso: "$TIMESTAMP_ISO"
timestamp_readable: "$TIMESTAMP_READABLE"
category: "$CATEGORY"
slug: "$POST_ID"
md: "$MD_FILENAME"
EOF

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
