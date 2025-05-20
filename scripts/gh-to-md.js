// DOM Element References
const urlInput = document.getElementById("issue-url");
const convertButton = document.getElementById("convert");
const statusAndErrorElement = document.getElementById("error"); // Re-purposing the error element for status too

const MIN_STATUS_DISPLAY_TIME_MS = 200; // Minimum time each status message is visible (1 second)

/**
 * Utility function to create a delay.
 * @param {number} ms The number of milliseconds to delay.
 * @returns {Promise<void>} A promise that resolves after the specified delay.
 */
const delay = (ms) => new Promise(resolve => setTimeout(resolve, ms));

/**
 * Resets the status/error message and enables input/button.
 */
const resetUI = () => {
    statusAndErrorElement.textContent = '';
    statusAndErrorElement.style.color = ''; // Reset color to default
    urlInput.disabled = false;
    convertButton.disabled = false;
};

/**
 * Updates the status/error message for the user, ensuring it's visible for a minimum duration.
 * @param {string} message The message to display.
 * @param {string} type The type of message: 'status' (blue), 'success' (green), or 'error' (red).
 * @returns {Promise<void>} A promise that resolves after the message has been displayed for at least MIN_STATUS_DISPLAY_TIME_MS.
 */
const updateStatus = async (message, type = 'status') => {
    statusAndErrorElement.textContent = message;
    switch (type) {
        case 'status':
            statusAndErrorElement.style.color = 'blue';
            break;
        case 'success':
            statusAndErrorElement.style.color = 'green';
            break;
        case 'error':
            statusAndErrorElement.style.color = 'red';
            break;
        default:
            statusAndErrorElement.style.color = ''; // Default browser color
    }
    await delay(MIN_STATUS_DISPLAY_TIME_MS); // Ensure message is visible for at least this long
};

/**
 * Parses a GitHub issue URL to extract owner, repo, and issue number.
 * @param {string} url The GitHub issue URL.
 * @returns {{owner: string, repo: string, number: string}} The parsed components.
 * @throws {Error} If the URL is invalid or not a GitHub issue URL.
 */
const parseGitHubUrl = (url) => {
    try {
        const urlObj = new URL(url);
        const pathSegments = urlObj.pathname.split("/").filter(s => s !== '');

        if (urlObj.hostname !== 'github.com' || pathSegments.length < 4 || pathSegments[2] !== 'issues') {
            throw new Error("Please enter a valid GitHub issue URL.");
        }

        const [owner, repo, , number] = pathSegments;
        if (!owner || !repo || !number || isNaN(parseInt(number))) {
            throw new Error("Could not parse owner, repository, or issue number from the URL.");
        }

        return { owner, repo, number };
    } catch (e) {
        if (e instanceof TypeError && e.message.includes('Invalid URL')) {
            throw new Error("Invalid URL format. Ensure it's a complete web address.");
        }
        throw new Error(`URL parsing failed: ${e.message}`);
    }
};

/**
 * Converts GitHub issue and comments data into a Markdown string.
 * @param {object} issue The GitHub issue object.
 * @param {Array<object>} comments An array of GitHub comment objects.
 * @returns {string} The formatted Markdown string.
 */
const convertToMarkdown = (issue, comments) => {
    let md = `# ${issue.title}\n\n`;
    md += `*Posted by @${issue.user.login}*\n\n`;
    md += issue.body + "\n\n";

    if (comments.length > 0) {
        md += "---\n\n";
        comments.forEach((comment) => {
            md += `### Comment by @${comment.user.login} on ${new Date(comment.created_at).toLocaleDateString()}\n\n`;
            md += comment.body + "\n\n";
            md += "---\n\n";
        });
    }

    return md;
};

/**
 * Fetches all pages of data from a paginated GitHub API endpoint.
 * @param {string} url The initial URL for the API endpoint.
 * @returns {Promise<Array<object>>} A promise that resolves with an array of all fetched items.
 * @throws {Error} If any fetch request fails.
 */
const getAllPages = async (url) => {
    let allItems = [];
    let nextUrl = url;

    while (nextUrl) {
        const response = await fetch(nextUrl);
        if (!response.ok) {
            throw new Error(`Failed to fetch data from ${nextUrl}. Status: ${response.status} ${response.statusText}`);
        }
        const items = await response.json();
        allItems = allItems.concat(items);

        const linkHeader = response.headers.get("Link");
        nextUrl = null;
        if (linkHeader) {
            const nextLink = linkHeader
                .split(",")
                .find((s) => s.includes('rel="next"'));
            if (nextLink) {
                nextUrl = nextLink.split(";")[0].trim().slice(1, -1);
            }
        }
    }
    return allItems;
};

/**
 * Fetches a GitHub issue and its associated comments.
 * @param {string} owner The repository owner.
 * @param {string} repo The repository name.
 * @param {string} number The issue number.
 * @returns {Promise<{issue: object, comments: Array<object>}>} A promise that resolves with the issue and comments data.
 * @throws {Error} If fetching the issue or comments fails.
 */
const fetchIssueAndComments = async (owner, repo, number) => {
    const issueUrl = `https://api.github.com/repos/${owner}/${repo}/issues/${number}`;
    const commentsUrl = `${issueUrl}/comments`;

    await updateStatus('Fetching issue details...', 'status'); // Staggered update
    const issueResponse = await fetch(issueUrl);
    if (!issueResponse.ok) {
        if (issueResponse.status === 404) {
            throw new Error(`Issue #${number} not found in '${owner}/${repo}'. Please verify the URL.`);
        }
        throw new Error(`Failed to fetch issue. Status: ${issueResponse.status} ${issueResponse.statusText}`);
    }
    const issue = await issueResponse.json();

    await updateStatus('Fetching comments (this might take a moment for many comments)...', 'status'); // Staggered update
    const comments = await getAllPages(commentsUrl);

    return { issue, comments };
};

/**
 * Copies the given text to the user's clipboard.
 * @param {string} text The text to copy.
 * @returns {Promise<void>} A promise that resolves when the text is copied.
 * @throws {Error} If the clipboard API is not available or copying fails.
 */
const copyToClipboard = async (text) => {
    if (!navigator.clipboard || !navigator.clipboard.writeText) {
        throw new Error("Clipboard API not supported by your browser. Please copy the markdown manually.");
    }
    await navigator.clipboard.writeText(text);
};

// Event Listener for the Convert Button
convertButton.addEventListener("click", async () => {
    // 1. Reset UI and disable elements
    resetUI();
    urlInput.disabled = true;
    convertButton.disabled = true;
    await updateStatus('Starting conversion...', 'status'); // Staggered update

    try {
        // 2. Parse URL
        await updateStatus('Parsing GitHub URL...', 'status'); // Staggered update
        const { owner, repo, number } = parseGitHubUrl(urlInput.value);

        // 3. Fetch Issue and Comments (these calls already include staggered updates internally)
        const { issue, comments } = await fetchIssueAndComments(owner, repo, number);

        // 4. Convert to Markdown
        await updateStatus('Converting data to Markdown...', 'status'); // Staggered update
        const markdown = convertToMarkdown(issue, comments);

        // 5. Copy to Clipboard
        await updateStatus('Attempting to copy to clipboard...', 'status'); // Staggered update
        await copyToClipboard(markdown);

        // 6. Success
        await updateStatus('Successfully copied to clipboard!', 'success'); // Staggered update

    } catch (error) {
        // Handle any errors that occurred during the process
        console.error("Conversion Error:", error);
        await updateStatus(`Conversion failed: ${error.message}`, 'error'); // Staggered update for errors
    } finally {
        // 7. Re-enable UI elements regardless of success or failure
        urlInput.disabled = false;
        convertButton.disabled = false;
    }
});

// Initial UI reset when the DOM is fully loaded
document.addEventListener('DOMContentLoaded', resetUI);
