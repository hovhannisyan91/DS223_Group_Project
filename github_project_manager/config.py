# config/config.py
import os
import ast
from dotenv import load_dotenv

load_dotenv('tasks.env')

ORG = os.getenv("ORG")
OWNER = os.getenv("OWNER")
TOKEN = os.getenv("TOKEN")

GITHUB_API = os.getenv("GITHUB_API")
REST_API  = os.getenv("REST_API")

PROJECT_TITLE = os.getenv("PROJECT_TITLE")


ROLE_LABELS = {
    "pm": "pm",
    "db": "db",
    "ds": "ds",
    "backend": "backend",
    "frontend": "frontend",

    # Dual Labels
    "pm_backend": "pm_backend",
    "pm_frontend": "pm_frontend",
    "pm_db": "pm_db",
    "pm_frontend_backend": "pm_frontend_backend"
}


GROUP_MEMBERS = {
    "Group-1": {
        "pm": "shushanmeyroyan",
        "db": "Arina89086",
        "backend": "NarekN7",
        "frontend": "aregkhachatryan6463",
        "ds": "shhushann"
    },
    "Group-2": {
        "pm": "vikamelkumyan",
        "db": "LevonHakobyan004",
        "backend": "grigorhovhannisyan-bit",
        "frontend": "ani777har",
        "ds": "ZhoraPoghosyan"
    },
    "Group-3": {
        "pm": "codecaine",
        "db": "itsallakh",
        "backend": "mariekhachatryan",
        "frontend": "yevastepanyan8",
        "ds": "levongevorgian"
    },
    "Group-4": {
        "pm": "HamletBrutyan",
        "db": "tachirion",
        "backend": "ElenaMelkonyan",
        "frontend": "manehp",
        "ds": "serinepoghosyan"
    },
    "Group-5": {
        "pm": "keema383",
        "db": "lizakhachatryan",
        "backend": "keema383",  # Same person
        "frontend": "yeghiazariangor",
        "ds": "norayramirkhanyan23"
    },
    "Group-6": {
        "pm": "AnzhelaDavityan",
        "db": "AmalyaTadevosyan245",
        "backend": "melkonyanmelanie",
        "frontend": "AnnaMikayelyan",
        "ds": "arpine2004"
    },
    "Group-7": {
        "pm": "aaareeev",
        "db": "zhannabalyan",
        "backend": "sonabarseghyan04",
        "frontend": "EdelweissG",
        "ds": "ellghalechyan"
    }
}


def compute_role_to_assignees(group_members):
    result = {}

    for group, roles in group_members.items():
        g = {}

        # Single roles
        g["pm"] = [roles["pm"]]
        g["db"] = [roles["db"]]
        g["backend"] = [roles["backend"]]
        g["frontend"] = [roles["frontend"]]
        g["ds"] = [roles["ds"]]

        # Dual roles
        g["pm_backend"] = [roles["pm"], roles["backend"]]
        g["pm_frontend"] = [roles["pm"], roles["frontend"]]
        g["pm_db"] = [roles["pm"], roles["db"]]
        g["pm_frontend_backend"] = [roles["pm"], roles["frontend"], roles["backend"]]

        result[group] = g

    return result


ROLE_TO_ASSIGNEES = compute_role_to_assignees(GROUP_MEMBERS)



# TASKS = {
#     "Task 1": {"title": "Setup project repository", "body": "Initialize the repository with README and .gitignore", "labels": ["setup"], "assignees": role_to_assignees["pm"]},
#     "Task 2": {"title": "Design database schema", "body": "Create an initial design for the database schema", "labels": ["database"], "assignees": role_to_assignees["db"]},
#     "Task 3": {"title": "Implement authentication", "body": "Set up user authentication and authorization", "labels": ["backend"], "assignees": role_to_assignees["pm_db"]},
# }



# TARGET_ISSUE_NUMBERS = ast.literal_eval(os.getenv("TARGET_ISSUE_NUMBERS"))







if __name__ == "__main__": 

    print(ROLE_TO_ASSIGNEES)
