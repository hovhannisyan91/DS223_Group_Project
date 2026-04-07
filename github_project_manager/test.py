PROJECT_BOARDS = {
    f"Group-{i}": {
        "repo": f"Group-{i}",
        "board": f"Group {i} Project Management",
    }
    for i in range(5,6)
}

print(PROJECT_BOARDS)

# for repo in $(gh repo list DS-223-2025-Fall --private --json name -q '.[].name'); do
#   gh repo edit DS-223-2025-Fall/$repo --visibility public
# done