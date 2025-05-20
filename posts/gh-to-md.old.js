const urlInput = document.getElementById("issue-url");
const convertButton = document.getElementById("convert");
const errorElement = document.getElementById("error");

function parseGitHubUrl(url) {
  try {
    const urlObj = new URL(url);
    const [, owner, repo, , number] = urlObj.pathname.split("/");
    return { owner, repo, number };
  } catch (e) {
    throw new Error("Invalid GitHub URL");
  }
}

function convertToMarkdown(issue, comments) {
  let md = `# ${issue.title}\n\n`;
  md += `*Posted by @${issue.user.login}*\n\n`;
  md += issue.body + "\n\n";

  if (comments.length > 0) {
    md += "---\n\n";
    comments.forEach((comment) => {
      md += `### Comment by @${comment.user.login}\n\n`;
      md += comment.body + "\n\n";
      md += "---\n\n";
    });
  }

  return md;
}

async function getAllPages(url) {
  let allItems = [];
  let nextUrl = url;

  while (nextUrl) {
    const response = await fetch(nextUrl);
    if (!response.ok) throw new Error("Failed to fetch data");
    const items = await response.json();
    allItems = allItems.concat(items);
    const link = response.headers.get("Link");
    nextUrl = null;
    if (link) {
      const nextLink = link
        .split(",")
        .find((s) => s.includes('rel="next"'));
      if (nextLink) nextUrl = nextLink.split(";")[0].trim().slice(1, -1);
    }
  }

  return allItems;
}

async function fetchIssueAndComments(owner, repo, number) {
  const issueUrl =
    `https://api.github.com/repos/${owner}/${repo}/issues/${number}`;
  const commentsUrl = `${issueUrl}/comments`;

  const [issue, comments] = await Promise.all([
    fetch(issueUrl).then((res) => {
      if (!res.ok) throw new Error("Failed to fetch issue");
      return res.json();
    }),
    getAllPages(commentsUrl),
  ]);

  return { issue, comments };
}

async function copyToClipboard(text) {
  await navigator.clipboard.writeText(text);
}

convertButton.addEventListener("click", async () => {
  errorElement.textContent = "";
  convertButton.disabled = true;

  try {
    const { owner, repo, number } = parseGitHubUrl(urlInput.value);
    const { issue, comments } = await fetchIssueAndComments(
      owner,
      repo,
      number,
    );
    const markdown = convertToMarkdown(issue, comments);
    await copyToClipboard(markdown);
  } catch (error) {
    errorElement.textContent = error.message;
  } finally {
    convertButton.disabled = false;
  }
});
