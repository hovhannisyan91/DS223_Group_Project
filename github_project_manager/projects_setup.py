from config import TOKEN, OWNER, ORG
from GitHubHandler import GitHubHandler


NUMBER_OF_GROUPS = 7
import os

PROJECT_BOARDS = {
    'Group-1': {
        "repo": "Group-1",
        "board": "Group 1 Project Management"
    },
    'Group-2': {
        "repo":"Group-2",
        "board": "Group 2 Project Management"
    },
    'Group-3': {
        "repo":"Group-3",
        "board": "Group 3 Project Management"
    },
    'Group-4': {
        "repo":"Group-4",
        "board": "Group 4 Project Management"
    },
    'Group-5': {
        "repo":"Group-5",
        "board": "Group 5 Project Management"
    },
    'Group-6': {
        "repo":"Group-6",
        "board": "Group 6 Project Management"
    },
    'Group-7': {
        "repo":"Group-7",
        "board": "Group 7 Project Management"
    },
}


MILESTONES = {
    "Milestone 1": {"due_on": "2025-11-11T23:59:59Z", "description": "milestones/m1.md"},
    "Milestone 2": {"due_on": "2025-11-19T23:59:59Z", "description": "milestones/m2.md"},
    "Milestone 3": {"due_on": "2025-11-28T23:59:59Z", "description": "milestones/m3.md"},
    "Milestone 4": {"due_on": "2025-12-08T23:59:59Z", "description": "milestones/m4.md"},
}


       
def load_markdown(path: str) -> str:
    """Load a markdown file safely and return its content."""
    if not os.path.exists(path):
        raise FileNotFoundError(f"Markdown file not found: {path}")

    with open(path, "r", encoding="utf-8") as f:
        return f.read()
    


for title, cfg in MILESTONES.items():
    md_path = cfg["description"]
    description_text = load_markdown(md_path)

    print(f"📌 Processing {title}...")
    print(f"Due on: {cfg['due_on']}")
    print(f"Description loaded from: {description_text}")

    # gh.create_milestone(
    #     title=title,
    #     description=description_text,
    #     due_on=cfg["due_on"]
    # )



if __name__ == "__main__":
    for group, cfg in PROJECT_BOARDS.items():

        repo = cfg["repo"]
        board = cfg["board"]

        print(f"\n==============================")
        print(f"🚀 Setting up project for {group}")
        print(f"📁 Repo:  {repo}")
        print(f"📋 Board: {board}")
        print("==============================\n")

        # Create GitHub handler for this repo + board
        gh = GitHubHandler(
            token=TOKEN,
            repo_owner=ORG,
            repo_name=repo,
            project_name=board
        )

        fields_to_add = [
            {"name": "Due Date", "field_type": "DATE"},
            {"name": "Start Date", "field_type": "DATE"}
            ]
            

        for field in fields_to_add:
            gh.add_field(name=field["name"], field_type=field["field_type"])


        # Create all milestones for this repo
        print(f"📌 Creating milestones for {group}...")
        for ms_title, ms_cfg in MILESTONES.items():
            description_md = load_markdown(ms_cfg["description"])
            gh.create_milestone(
                title=ms_title,
                description=description_md,
                due_on=ms_cfg["due_on"]
            )

        print(f"🎉 Finished setting up {group}\n")


