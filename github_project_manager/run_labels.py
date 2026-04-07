#!/usr/bin/env python3
import subprocess
import os
import sys

ORG = "DS-223-2025-Fall"
LABEL_SCRIPT = "create_labels.py"

def write_env(repo_path: str):
    """Write .env for create_labels.py"""
    with open(".env", "w") as f:
        f.write(f"REPO={repo_path}\n")
    print(f"📝 .env updated → REPO={repo_path}")


def run_label_script():
    # TODO : Add error handling
    
    """Run create_labels.py normally"""
    print("▶️ Running create_labels.py ...")
    result = subprocess.run(
        [sys.executable, LABEL_SCRIPT],
        text=True
    )
    if result.returncode != 0:
        print("❌ Error running label script")
    else:
        print("✅ Labels updated\n")


def main():
    print("\n=========================================")
    print("🚀 Starting label creation for ALL GROUPS")
    print("=========================================\n")

    for group_num in range(1, 8):
        repo = f"{ORG}/Group-{group_num}"

        print("-----------------------------------------")
        print(f"🚀 Processing Repository: {repo}")
        print("-----------------------------------------")

        write_env(repo)
        run_label_script()

    print("\n🎉 Completed label creation for all repositories!")


if __name__ == "__main__":
    main()