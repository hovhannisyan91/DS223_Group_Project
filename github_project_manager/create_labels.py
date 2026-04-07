#!/usr/bin/env python3
import os
import subprocess

# =========================================
# Load .env
# =========================================
if not os.path.exists(".env"):
    print("⚠️  .env not found. Create one with REPO=ORG/REPO")
    exit(1)

env_vars = {}
with open(".env") as f:
    for line in f:
        if "=" in line:
            key, value = line.strip().split("=", 1)
            env_vars[key] = value

if "REPO" not in env_vars:
    print("❌ .env missing REPO variable")
    exit(1)

REPO = env_vars["REPO"]
print(f"📁 Target Repository: {REPO}")

# =========================================
# LABEL DEFINITIONS
# =========================================
LABELS = {
    # Core labels
    "pm": ("FFD700", "Product/Project Manager tasks"),
    "db": ("1E90FF", "Database Developer tasks"),
    "ds": ("00C853", "Data Scientist tasks"),
    "backend": ("FF7043", "Backend Developer tasks"),
    "frontend": ("42A5F5", "Frontend Developer tasks"),

    # Cross-collaboration
    "pm_backend": ("BFD4F2", "Tasks for PM and Backend collaboration"),
    "pm_frontend": ("D4E157", "Tasks for PM and Frontend collaboration"),
    "pm_db": ("81C784", "Tasks for PM and Database collaboration"),
    "pm_frontend_backend": ("4DB6AC", "Tasks for PM, Frontend, and Backend collaboration"),
}


# =========================================
# CREATE LABELS
# =========================================
for label_name, (color, description) in LABELS.items():
    print(f"🏷️ Creating label: {label_name}")

    cmd = [
        "gh", "label", "create",
        label_name,
        "--repo", REPO,
        "--color", color,
        "--description", description
    ]

    res = subprocess.run(cmd, capture_output=True, text=True)

    if res.returncode != 0:
        # Label probably exists, skip silently
        print(f"⚠️  Could not create '{label_name}', skipping...")
    else:
        print(f"✅  Label '{label_name}' created successfully!")

print("\n🎉 All labels processed for:", REPO)