from datetime import date, timedelta
from GitHubHandler import GitHubHandler
from config import TOKEN, ORG

# ==========================================================
# CONFIG FLAGS
# ==========================================================
USE_LABELS = True
ASSIGN_PEOPLE = True   # keep False for now to avoid email notifications


# ==========================================================
# GROUP MEMBERS (for future assignee support)
# ==========================================================
GROUP_MEMBERS = {
    # "Group-1": {
    #     "pm": ["shushanmeyroyan"],
    #     "db": ["Arina89086"],
    #     "backend": ["NarekN7"],
    #     "frontend": ["aregkhachatryan6463"],
    #     "ds": ["shhushann"],
    # },
    # "Group-2": {
    #     "pm": ["vikamelkumyan"],
    #     "db": ["LevonHakobyan004"],
    #     "backend": ["grigorhovhannisyan-bit"],
    #     "frontend": ["ani777har"],
    #     "ds": ["ZhoraPoghosyan"],
    # },
    # "Group-3": {
    #     "pm": ["ArmenMkrtumyan"],
    #     "db": ["itsallakh"],
    #     "backend": ["mariekhachatryan"],
    #     "frontend": ["yevastepanyan8"],
    #     "ds": ["levongevorgian"],
    # },
    # "Group-4": {
    #     "pm": ["HamletBrutyan"],
    #     "db": ["tachirion"],
    #     "backend": ["ElenaMelkonyan"],
    #     "frontend": ["manehp"],
    #     "ds": ["serinepoghosyan"],
    # },
    # "Group-5": {
    #     "pm": ["keema383"],
    #     "db": ["lizakhachatryan"],
    #     "backend": ["keema383"],  # same person
    #     "frontend": ["yeghiazariangor"],
    #     "ds": ["norayramirkhanyan23"],
    # },
    "Group-6": {
        "pm": ["AnzhelaDavityan"],
        "db": ["AmalyaTadevosyan245"],
        "backend": ["melkonyanmelanie"],
        "frontend": ["AnnaMikayelyan"],
        "ds": ["arpine2004"],
    },
    "Group-7": {
        "pm": ["aaareeev"],
        "db": ["zhannabalyan"],
        "backend": ["sonabarseghyan04"],
        "frontend": ["EdelweissG"],
        "ds": ["ellghalechyan"],
    },
}


# ==========================================================
# ROLE → LABELS
# (only using labels you’ve already created)
# ==========================================================
ROLE_LABELS = {
    "pm": ["pm"],
    "db": ["db"],
    "ds": ["ds"],
    "backend": ["backend"],
    "frontend": ["frontend"],
    "pm_frontend_backend": ["pm_frontend_backend"],
}


# ==========================================================
# MILESTONE DATES (for Start/Due in project fields)
# ==========================================================
MILESTONE_ORDER = ["Milestone 1", "Milestone 2", "Milestone 3", "Milestone 4"]

# For project DATE fields: just date (YYYY-MM-DD)
MILESTONE_DATES = {
    "Milestone 1": "2025-11-11",
    "Milestone 2": "2025-11-19",
    "Milestone 3": "2025-11-28",
    "Milestone 4": "2025-12-08",
}


def get_start_and_due(ms_name: str) -> tuple[str, str]:
    """
    Start date:
      - M1: due date - 7 days
      - others: previous milestone's due date
    Due date:
      - milestone's due date
    """
    idx = MILESTONE_ORDER.index(ms_name)
    due = date.fromisoformat(MILESTONE_DATES[ms_name])

    if idx == 0:
        start = due - timedelta(days=7)
    else:
        prev = MILESTONE_ORDER[idx - 1]
        start = date.fromisoformat(MILESTONE_DATES[prev])

    return start.isoformat(), due.isoformat()


# ==========================================================
# MILESTONE TASKS — SMALL TASKS PER ROLE
# ==========================================================
MILESTONE_TASKS = {
    "Milestone 1": {
        "pm": [
            "Define the problem statement using the shared Google Doc.",
            "Finalize team roles and responsibilities using the shared spreadsheet.",
            "Schedule a meeting with Karen and Artur.",
            "Locate and join your assigned GitHub repository.",
            "Create product roadmap and prioritized functionality list.",
            "Create Python virtual environment and generate requirements.txt.",
            "Push problem definition, repo confirmation, and requirements.txt.",
            "Prototype the UI using Figma or a similar tool.",
            "Create a private Slack channel for your group.",
            "Install VSCode and the Project Manager extension.",
        ]
    },

    "Milestone 2": {
        "pm": [
            "Install mkdocs and initialize the documentation structure.",
            "Design ERD for the product database.",
            "Transform project structure into service-based layout.",
            "Review and merge PRs from team members.",
            "Delete branches after merging PRs.",
        ],
        "db": [
            "Create branch named 'db'.",
            "Create database service/container.",
            "Create the database and required tables based on ERD.",
            "Connect to SQL from Python.",
            "Load data from flat files into the database.",
            "Implement helper DB methods for later usage.",
            "Push DB work to 'db' branch.",
            "Open pull request for PM review.",
        ],
        "ds": [
            "Create branch named 'ds'.",
            "Create DS service/container.",
            "Simulate data if needed.",
            "Use DB CRUD functionality for data access.",
            "Build simple baseline models.",
            "Push DS work to 'ds' branch.",
            "Open pull request for PM review.",
        ],
        "backend": [
            "Create branch named 'back'.",
            "Create backend service/container.",
            "Design API endpoints together with PM and DB developer.",
            "Implement dummy CRUD endpoints (GET, POST, PUT, DELETE).",
            "Push backend work to 'back' branch.",
            "Open pull request for PM review.",
        ],
        "frontend": [
            "Create branch named 'front'.",
            "Create frontend service/container.",
            "Coordinate with PM on the initial UI skeleton.",
            "Push UI skeleton to 'front' branch.",
            "Open pull request for PM review.",
        ],
    },

    "Milestone 3": {
        "pm": [
            "Design the complete list of required API endpoints.",
            "Share endpoint specifications with backend and frontend developers.",
            "Research appropriate Streamlit components for the UI.",
            "Support frontend engineer with UI and component decisions.",
        ],
        "db": [
            "Update database tables according to the revised ERD.",
            "Finalize database docstrings and internal documentation.",
            "Push updated DB work.",
        ],
        "ds": [
            "Build the final machine learning model.",
            "Prepare final output (predictions, scores, or segments).",
            "Push final DS work to 'ds' branch.",
        ],
        "backend": [
            "Implement all required API endpoints based on PM specification.",
            "Create Pydantic models for requests and responses.",
            "Add docstrings and documentation for all endpoints.",
            "Push backend work to 'back' branch.",
        ],
        "frontend": [
            "Build final app layouts in Streamlit.",
            "Refine UI based on PM requirements.",
            "Use only built-in Streamlit components.",
            "Push final frontend work to 'front' branch.",
        ],
    },

    "Milestone 4": {
        "pm": [
            "Finalize endpoint list including analytics and visualization endpoints.",
            "Provide clear guidance on visual analytics requirements.",
            "Create MkDocs overview page (Problem, Solution, Expected Outcomes).",
            "Create documentation pages for each service (api, app, db, model, etc.).",
            "Deploy the documentation site to GitHub Pages.",
            "Update README with links to MkDocs, pgAdmin, Streamlit, Swagger.",
            "Add run instructions to README.",
            "Add UI and Swagger screenshots to README.",
            "Coordinate cleanup of the repository and removal of unnecessary files.",
        ],
        "db": [
            "Apply any database adjustments needed for analytics features.",
        ],
        "ds": [
            "Finalize the model for production usage.",
            "Prepare visual outputs for frontend integration.",
        ],
        "backend": [
            "Implement additional endpoints needed for analytics visualization.",
            "Ensure all APIs are stable and production-ready.",
        ],
        "frontend": [
            "Integrate all analytics visualizations into the Streamlit app.",
        ],
        # collaboration task across PM + FE + BE
        "pm_frontend_backend": [
            "Coordinate final integration across PM, backend, and frontend services.",
        ],
    },
}


# ==========================================================
# PROJECT BOARDS (per group)
# ==========================================================
PROJECT_BOARDS = {
    f"Group-{i}": {
        "repo": f"Group-{i}",
        "board": f"Group {i} Project Management",
    }
    for i in range(6, 8)
}


# ==========================================================
# Helper functions
# ==========================================================
def build_issue_title(group: str, milestone: str, role: str, task: str) -> str:
    return f"[{milestone}] [{role.upper()}] {task}"


def build_issue_body(group: str, milestone: str, role: str, task: str) -> str:
    return f"""# {milestone}

**Group:** {group}  
**Role:** {role}

## Task
- {task}
"""


def get_labels_for_role(role: str) -> list[str]:
    if not USE_LABELS:
        return []
    return ROLE_LABELS.get(role, [])


def get_assignees_for_role(group: str, role: str) -> list[str]:
    if not ASSIGN_PEOPLE:
        return []

    base = GROUP_MEMBERS[group]

    if role in base:
        return base[role]

    if role == "pm_frontend_backend":
        return base["pm"] + base["frontend"] + base["backend"]

    return []


def generate_issues_for_milestone(gh: GitHubHandler, group: str, milestone: str):
    tasks_by_role = MILESTONE_TASKS[milestone]
    start_date, due_date = get_start_and_due(milestone)

    print(f"\n=== Generating issues for {group} → {milestone} ===")
    print(f"Start Date = {start_date}, Due Date = {due_date}")

    for role, tasks in tasks_by_role.items():
        for task in tasks:
            title = build_issue_title(group, milestone, role, task)
            body = build_issue_body(group, milestone, role, task)
            labels = get_labels_for_role(role)
            assignees = get_assignees_for_role(group, role)

            # Create or update the issue (GitHubHandler handles update_if_exists)
            issue = gh.create_issue(
                title=title,
                body=body,
                labels=labels,
                milestone=milestone,
                assignees=assignees if assignees else None,
            )

            issue_num = issue["number"]

            # Add to project
            gh.add_issue_to_project(issue_num)

            # Set project fields (if fields exist)
            gh.set_project_field_value(issue_num, "Start Date", start_date)
            gh.set_project_field_value(issue_num, "Due Date", due_date)
            gh.set_project_field_value(issue_num, "Status", "Todo")

            print(f"✅ Issue #{issue_num} created/updated: {title}")

    print(f"✔ Completed {group} – {milestone}")


# ==========================================================
# MAIN
# ==========================================================
if __name__ == "__main__":
    # You can restrict which milestones to generate, e.g.:
    # MILESTONES_TO_GENERATE = ["Milestone 1", "Milestone 2"]
    MILESTONES_TO_GENERATE = MILESTONE_ORDER[:]  # all 4

    for group, cfg in PROJECT_BOARDS.items():
        repo_name = cfg["repo"]
        board_name = cfg["board"]

        print("\n========================================")
        print(f"🚀 Setting up issues for {group}")
        print(f"📁 Repo: {ORG}/{repo_name}")
        print(f"📋 Board: {board_name}")
        print("========================================\n")

        gh = GitHubHandler(
            token=TOKEN,
            repo_owner=ORG,
            repo_name=repo_name,
            project_name=board_name,
        )

        for ms in MILESTONES_TO_GENERATE:
            generate_issues_for_milestone(gh, group, ms)

    print("\n🎉 All issues generated for all groups and milestones.")