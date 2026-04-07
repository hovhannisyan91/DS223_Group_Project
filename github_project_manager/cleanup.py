import requests
from config import TOKEN, ORG  # make sure ORG = "DS-223-2025-Fall"

REPOS = [
    "Group-1",
    "Group-2",
    "Group-3",
    "Group-4",
    "Group-5",
    "Group-6",
    "Group-7",
]

BASE_URL = "https://api.github.com"


def delete_issue(owner: str, repo: str, number: int):
    """Delete an issue using REST API."""
    url = f"{BASE_URL}/repos/{owner}/{repo}/issues/{number}"

    response = requests.delete(
        url,
        headers={
            "Authorization": f"Bearer {TOKEN}",
            "Accept": "application/vnd.github+json"
        }
    )

    if response.status_code in (204, 200):
        print(f"🗑️  Deleted issue #{number}")
    else:
        print(f"⚠️ Could not delete issue #{number}: {response.status_code} {response.text}")


def list_issues(owner: str, repo: str):
    url = f"{BASE_URL}/repos/{owner}/{repo}/issues?state=all&per_page=100"
    response = requests.get(url, headers={"Authorization": f"Bearer {TOKEN}"})
    if response.status_code != 200:
        print(f"❌ Failed to list issues for {repo}: {response.status_code}")
        return []
    return response.json()


def delete_all_issues_for_repo(repo: str):
    print(f"\n==============================")
    print(f"🧹 Cleaning issues for {repo}")
    print("==============================")

    issues = list_issues(ORG, repo)

    if not issues:
        print("✔ No issues found.")
        return

    # Filter out PRs — GitHub API mixes issues & PRs
    issue_list = [i for i in issues if "pull_request" not in i]

    if not issue_list:
        print("✔ No issues (only PRs).")
        return

    for issue in issue_list:
        delete_issue(ORG, repo, issue["number"])

    print(f"🎉 Finished cleaning {repo}")


if __name__ == "__main__":
    for repo in REPOS:
        delete_all_issues_for_repo(repo)