import requests
import re
import subprocess
import json


class GitHubHandler:
    def __init__(self, token: str, repo_owner: str, repo_name: str, project_name: str):
        self.token = token
        self.repo_owner = repo_owner
        self.repo_name = repo_name
        self.project_name = project_name

        self.rest_base = "https://api.github.com"
        self.graphql_url = f"{self.rest_base}/graphql"
        self.headers = {
            "Authorization": f"Bearer {token}",
            "Accept": "application/vnd.github+json"
        }

        # Initialize project ID when creating instance
        self.project_id = self.get_or_create_project()

    # ----------------------------------
    # Base GraphQL request
    # ----------------------------------
    def graphql(self, query: str, variables: dict | None = None):
        response = requests.post(
            self.graphql_url,
            headers=self.headers,
            json={"query": query, "variables": variables or {}}
        )

        if response.status_code != 200:
            raise Exception(f"GraphQL error: {response.status_code}\n{response.text}")

        data = response.json()
        if "errors" in data:
            raise Exception(f"GraphQL query errors: {json.dumps(data['errors'], indent=2)}")
        return data

    # ----------------------------------
    # Safely detect if owner is User or Org
    # ----------------------------------
    def get_owner_node_id(self):
      print("DEBUG >>> get_owner_node_id() called")
      print("DEBUG >>> repo_owner =", self.repo_owner)

      # 1) Try USER lookup
      user_query = """
      query($login: String!) {
        user(login: $login) {
          id
        }
      }
      """

      try:
          user_result = self.graphql(user_query, {"login": self.repo_owner})
          print("DEBUG >>> user_result =", user_result)
      except Exception as e:
          print("DEBUG >>> User lookup failed:", e)
          user_result = {"data": {"user": None}}

      if user_result["data"].get("user"):
          print(f"👤 '{self.repo_owner}' is a USER")
          return user_result["data"]["user"]["id"]

      # 2) Try ORGANIZATION lookup
      print("DEBUG >>> Trying organization lookup")

      org_query = """
      query($login: String!) {
        organization(login: $login) {
          id
        }
      }
      """

      try:
          org_result = self.graphql(org_query, {"login": self.repo_owner})
          print("DEBUG >>> org_result =", org_result)
      except Exception as e:
          print("DEBUG >>> Org lookup failed:", e)
          org_result = {"data": {"organization": None}}

      if org_result["data"].get("organization"):
          print(f"🏢 '{self.repo_owner}' is an ORGANIZATION")
          return org_result["data"]["organization"]["id"]

      raise Exception(f"❌ '{self.repo_owner}' is not a GitHub user or org")

    # ----------------------------------
    # Get or create ProjectV2
    # ----------------------------------
    def get_or_create_project(self) -> str:
        """Get the ID of an existing project by name, or create it if missing."""
        owner_id = self.get_owner_node_id()

        # 1️⃣ Check existing projects through GraphQL (fresh)
        query = """
        query($ownerId: ID!) {
          node(id: $ownerId) {
            ... on User {
              projectsV2(first: 50) {
                nodes { id title url }
              }
            }
            ... on Organization {
              projectsV2(first: 50) {
                nodes { id title url }
              }
            }
          }
        }
        """
        result = self.graphql(query, {"ownerId": owner_id})
        projects = result["data"]["node"]["projectsV2"]["nodes"]

        existing = next((p for p in projects if p["title"] == self.project_name), None)

        # 2️⃣ If not found → create new
        if not existing:
            print(f"🚀 Creating new Project Board: {self.project_name}")
            mutation = """
            mutation($ownerId: ID!, $title: String!) {
              createProjectV2(input: {ownerId: $ownerId, title: $title}) {
                projectV2 { id title url }
              }
            }
            """
            result = self.graphql(mutation, {"ownerId": owner_id, "title": self.project_name})
            project_data = result.get("data", {}).get("createProjectV2", {}).get("projectV2")
            if not project_data:
                raise Exception(f"❌ Failed to create project. Response:\n{result}")
            self.project_url = project_data["url"]
            print(f"✅ Created new project: {project_data['title']} ({self.project_url})")
            return project_data["id"]

        # 3️⃣ Found existing → confirm it still exists via CLI
        print(f"✅ Found existing project: {existing['title']}")
        cli_check = subprocess.run(
            ["gh", "project", "list", "--owner", self.repo_owner, "--limit", "50"],
            capture_output=True,
            text=True
        )
        if self.project_name not in cli_check.stdout:
            print(f"⚠️ CLI did not find project '{self.project_name}'. Re-creating...")
            mutation = """
            mutation($ownerId: ID!, $title: String!) {
              createProjectV2(input: {ownerId: $ownerId, title: $title}) {
                projectV2 { id title url }
              }
            }
            """
            result = self.graphql(mutation, {"ownerId": owner_id, "title": self.project_name})
            project_data = result.get("data", {}).get("createProjectV2", {}).get("projectV2")
            self.project_url = project_data["url"]
            print(f"✅ Re-created project: {project_data['title']} ({self.project_url})")
            return project_data["id"]

        # 4️⃣ If confirmed, return its ID
        self.project_url = existing["url"]
        return existing["id"]

    # ----------------------------------
    # Add custom field to project
    # ----------------------------------
    def add_field(self, name: str, field_type: str = "TEXT"):
        """Add a custom field to a GitHub ProjectV2 using the CLI."""
        valid_types = {"TEXT", "NUMBER", "DATE", "SINGLE_SELECT", "ITERATION"}
        field_type = field_type.upper()
        if field_type not in valid_types:
            raise ValueError(f"Invalid field type '{field_type}'. Must be one of: {valid_types}")

        # Get the project number (CLI works with numbers, not IDs)
        print(f"🔍 Getting project number for '{self.project_name}'...")
        list_cmd = [
            "gh", "project", "list",
            "--owner", self.repo_owner,
            "--limit", "50"
        ]
        res = subprocess.run(list_cmd, capture_output=True, text=True)
        if res.returncode != 0:
            raise Exception(f"Failed to list projects:\n{res.stderr}")

        # Extract the project number by matching project name
        pattern = rf"^\s*(\d+)\s+{re.escape(self.project_name)}"
        match = re.search(pattern, res.stdout, re.MULTILINE)
        if not match:
            raise Exception(f"Could not find project '{self.project_name}' in CLI output:\n{res.stdout}")

        project_number = match.group(1)
        print(f"📋 Found project number: {project_number}")

        # Add the field
        print(f"➕ Adding field '{name}' ({field_type}) via CLI...")
        cmd = [
            "gh", "project", "field-create",
            project_number,
            "--owner", self.repo_owner,
            "--name", name,
            "--data-type", field_type
        ]
        res = subprocess.run(cmd, capture_output=True, text=True)
        if res.returncode != 0:
            raise Exception(f"❌ Field creation failed:\n{res.stderr}")

        print(f"✅ Field created successfully: {name}")
        return res.stdout
    # ----------------------------------
    # Internal: Fetch project views & fields
    # ----------------------------------
    def _get_views_and_fields(self):
        """Return all views and fields for this project."""
        query = """
        query($projectId: ID!) {
          node(id: $projectId) {
            ... on ProjectV2 {
              title
              views(first: 10) {
                nodes {
                  id
                  name
                  visibleFields {
                    nodes { id name }
                  }
                }
              }
              fields(first: 50) {
                nodes { id name dataType }
              }
            }
          }
        }
        """
        data = self.graphql(query, {"projectId": self.project_id})
        return data["data"]["node"]

    # ----------------------------------
    # Internal: Toggle field visibility for one view
    # ----------------------------------
  
    # ----------------------------------
    # List all project fields
    # ----------------------------------
    def list_project_fields(self):
        """List all existing project fields."""
        query = """
        query($projectId: ID!) {
          node(id: $projectId) {
            ... on ProjectV2 {
              fields(first: 50) {
                nodes { id name dataType }
              }
            }
          }
        }
        """
        result = self.graphql(query, {"projectId": self.project_id})
        fields = result["data"]["node"]["fields"]["nodes"]
        print("📋 Project fields:")
        for f in fields:
            print(f"  - {f['name']} ({f['dataType']})")
        return fields
    # ----------------------------------
    # Update existing milestone (replace)
    # ----------------------------------
    def update_milestone(self, title: str, description: str = "", due_on: str | None = None, state: str = "open"):
        """Find an existing milestone by title and update its properties."""
        list_url = f"{self.rest_base}/repos/{self.repo_owner}/{self.repo_name}/milestones"
        res = requests.get(list_url, headers=self.headers)
        if res.status_code != 200:
            raise Exception(f"❌ Could not list milestones: {res.text}")

        milestones = res.json()
        match = next((m for m in milestones if m["title"] == title), None)
        if not match:
            raise Exception(f"❌ Milestone '{title}' not found to update.")

        milestone_number = match["number"]
        patch_url = f"{self.rest_base}/repos/{self.repo_owner}/{self.repo_name}/milestones/{milestone_number}"

        payload = {"title": title, "state": state}
        if description:
            payload["description"] = description
        if due_on:
            payload["due_on"] = due_on

        response = requests.patch(patch_url, headers=self.headers, json=payload)
        if response.status_code != 200:
            raise Exception(f"❌ Milestone update failed: {response.status_code}\n{response.text}")

        print(f"✅ Milestone '{title}' updated successfully.")
        return response.json()
    # ----------------------------------
    # Create milestone (REST API)
    # ----------------------------------
    def create_milestone(self, title: str, description: str = "", due_on: str | None = None):
        """Create milestone; if it already exists, update it instead."""
        url = f"{self.rest_base}/repos/{self.repo_owner}/{self.repo_name}/milestones"
        data = {"title": title, "description": description}
        if due_on:
            data["due_on"] = due_on

        response = requests.post(url, headers=self.headers, json=data)
        if response.status_code == 201:
            milestone = response.json()
            print(f"✅ Milestone created: {milestone['title']} (#{milestone['number']})")
            return milestone

        # If milestone already exists → update instead
        if response.status_code == 422 and "already_exists" in response.text:
            print(f"⚙️ Milestone '{title}' already exists — updating it instead.")
            return self.update_milestone(title, description=description, due_on=due_on)

        raise Exception(f"❌ Milestone creation failed: {response.status_code}\n{response.text}")
        # ----------------------------------
    # List all views and their visible fields
    # ----------------------------------
    # ----------------------------------
    # Internal: Fetch project views & fields (fully schema-safe)
    # ----------------------------------
    def _get_views_and_fields(self):
        """Return all views and available field configurations for this project (with proper pagination)."""
        query = """
        query($projectId: ID!) {
          node(id: $projectId) {
            ... on ProjectV2 {
              title
              views(first: 10) {
                nodes {
                  id
                  name
                  visibleFields(first: 50) {
                    nodes {
                      id
                      name
                    }
                  }
                }
              }
              fields(first: 50) {
                nodes {
                  __typename
                  ... on ProjectV2FieldCommon {
                    id
                    name
                    dataType
                  }
                  ... on ProjectV2IterationField {
                    id
                    name
                    dataType
                  }
                  ... on ProjectV2SingleSelectField {
                    id
                    name
                    dataType
                  }
                }
              }
            }
          }
        }
        """
        data = self.graphql(query, {"projectId": self.project_id})
        return data["data"]["node"]

    # ----------------------------------
    # Hide / Unhide fields by name
    # ----------------------------------
    def _set_field_visibility(self, view_id: str, field_ids: list[str], visible: bool):
        """Update visibility of one or more fields in a specific view."""
        mutation = """
        mutation($input: UpdateProjectV2ViewVisibilityInput!) {
          updateProjectV2ViewVisibility(input: $input) {
            projectV2View { id name }
          }
        }
        """
        variables = {
            "input": {
                "viewId": view_id,
                "fieldIds": field_ids,
                "isVisible": visible
            }
        }
        result = self.graphql(mutation, variables)
        action = "✅ Unhidden" if visible else "🙈 Hidden"
        print(f"{action} fields: {field_ids} in view {view_id}")
        return result

    def unhide_fields_by_name(self, field_names: list[str]):
        """Unhide given fields in all views where they exist."""
        node = self._get_views_and_fields()
        all_fields = {f["name"]: f["id"] for f in node["fields"]["nodes"]}
        views = node["views"]["nodes"]

        for view in views:
            view_id = view["id"]
            ids_to_unhide = [all_fields[name] for name in field_names if name in all_fields]
            if ids_to_unhide:
                self._set_field_visibility(view_id, ids_to_unhide, visible=True)

    def hide_fields_by_name(self, field_names: list[str]):
        """Hide given fields in all views where they exist."""
        node = self._get_views_and_fields()
        all_fields = {f["name"]: f["id"] for f in node["fields"]["nodes"]}
        views = node["views"]["nodes"]

        for view in views:
            view_id = view["id"]
            ids_to_hide = [all_fields[name] for name in field_names if name in all_fields]
            if ids_to_hide:
                self._set_field_visibility(view_id, ids_to_hide, visible=False)

    # ----------------------------------
    # Create Issue (with labels, milestone, assignee)
    # ----------------------------------
    # ----------------------------------
    # Create or update a GitHub Issue (returns issue number)
    # ----------------------------------
    def create_issue(self, title: str, body: str = "", labels: list[str] | None = None,
                     milestone: str | None = None, assignees: list[str] | None = None,
                     update_if_exists: bool = True):
        """Create an issue, optionally update existing one if same title exists."""
        url = f"{self.rest_base}/repos/{self.repo_owner}/{self.repo_name}/issues"
        existing_issues = requests.get(
            f"{url}?state=all&per_page=100",
            headers=self.headers
        ).json()

        # 1️⃣ Check for existing issue by title
        for issue in existing_issues:
            if issue["title"].strip().lower() == title.strip().lower():
                if update_if_exists:
                    print(f"⚙️ Issue '{title}' already exists — updating it instead.")
                    issue_number = issue["number"]
                    update_data = {
                        "body": body,
                        "labels": labels or issue.get("labels", []),
                        "assignees": assignees or issue.get("assignees", [])
                    }
                    response = requests.patch(
                        f"{url}/{issue_number}",
                        json=update_data,
                        headers=self.headers
                    )
                    if response.status_code not in [200, 201]:
                        raise Exception(f"❌ Failed to update issue #{issue_number}: {response.text}")
                    print(f"✅ Updated issue #{issue_number}: {title}")
                    return {
                        "number": issue_number,
                        "url": issue["html_url"]
                    }
                else:
                    print(f"⚠️ Issue '{title}' already exists. Skipping creation.")
                    return {
                        "number": issue["number"],
                        "url": issue["html_url"]
                    }

        # 2️⃣ Create a new issue
        issue_data = {
            "title": title,
            "body": body,
        }
        if labels:
            issue_data["labels"] = labels
        if assignees:
            issue_data["assignees"] = assignees
        if milestone:
            # Look up milestone number by title
            milestones = requests.get(f"{url[:-7]}/milestones", headers=self.headers).json()
            milestone_id = next((m["number"] for m in milestones if m["title"] == milestone), None)
            if milestone_id:
                issue_data["milestone"] = milestone_id

        response = requests.post(url, json=issue_data, headers=self.headers)
        if response.status_code not in [200, 201]:
            raise Exception(f"❌ Issue creation failed: {response.status_code}\n{response.text}")

        issue_info = response.json()
        issue_number = issue_info["number"]
        print(f"✅ Created issue #{issue_number}: {title}")
        return {
            "number": issue_number,
            "url": issue_info["html_url"]
        }
    # ----------------------------------
    # Internal: get Issue node ID by number
    # ----------------------------------
    def _get_issue_node_id(self, issue_number: int) -> str:
        query = """
        query($owner:String!, $name:String!, $number:Int!) {
          repository(owner:$owner, name:$name) {
            issue(number:$number) { id url }
          }
        }
        """
        vars_ = {"owner": self.repo_owner, "name": self.repo_name, "number": issue_number}
        data = self.graphql(query, vars_)
        issue = data["data"]["repository"]["issue"]
        if not issue:
            raise Exception(f"Issue #{issue_number} not found in {self.repo_owner}/{self.repo_name}.")
        return issue["id"]

    # ----------------------------------
    # Internal: find existing ProjectV2 item for an issue URL (handles pagination)
    # ----------------------------------
    def _find_project_item_id_by_issue_url(self, issue_url: str) -> str | None:
        query = """
        query($projectId: ID!, $after: String) {
          node(id: $projectId) {
            ... on ProjectV2 {
              items(first: 100, after: $after) {
                nodes {
                  id
                  content { ... on Issue { url } }
                }
                pageInfo { hasNextPage endCursor }
              }
            }
          }
        }
        """
        after = None
        while True:
            vars_ = {"projectId": self.project_id, "after": after}
            data = self.graphql(query, vars_)["data"]["node"]["items"]
            for n in data["nodes"]:
                if n["content"] and n["content"].get("url") == issue_url:
                    return n["id"]
            if not data["pageInfo"]["hasNextPage"]:
                return None
            after = data["pageInfo"]["endCursor"]

    # ----------------------------------
    # Add ONE issue to the ProjectV2 board (idempotent)
    # ----------------------------------
    def add_issue_to_project(self, issue_number: int) -> str:
        issue_url = f"https://github.com/{self.repo_owner}/{self.repo_name}/issues/{issue_number}"

        # 1) If it's already in the project, return existing item id
        existing_item_id = self._find_project_item_id_by_issue_url(issue_url)
        if existing_item_id:
            print(f"📎 Issue #{issue_number} already on project (item {existing_item_id}).")
            return existing_item_id

        # 2) Get issue node id
        issue_node_id = self._get_issue_node_id(issue_number)

        # 3) Add to project
        mutation = """
        mutation($projectId: ID!, $contentId: ID!) {
          addProjectV2ItemById(input:{ projectId:$projectId, contentId:$contentId }) {
            item { id }
          }
        }
        """
        vars_ = {"projectId": self.project_id, "contentId": issue_node_id}
        try:
            res = self.graphql(mutation, vars_)
            item_id = res["data"]["addProjectV2ItemById"]["item"]["id"]
            print(f"🧩 Added Issue #{issue_number} to project (item {item_id}).")
            return item_id
        except Exception as e:
            # If GitHub ever returns a “content already exists” style error, fall back to lookup
            print(f"⚠️ addProjectV2ItemById threw: {e}. Checking if item now exists…")
            existing_item_id = self._find_project_item_id_by_issue_url(issue_url)
            if existing_item_id:
                print(f"📎 Issue #{issue_number} is on project (item {existing_item_id}).")
                return existing_item_id
            raise

    # ----------------------------------
    # Add MANY issues to the ProjectV2 board (idempotent)
    # ----------------------------------
    def add_issues_to_project(self, issue_numbers: list[int]) -> list[tuple[int, str | None]]:
        results: list[tuple[int, str | None]] = []
        for num in issue_numbers:
            try:
                item_id = self.add_issue_to_project(num)
                results.append((num, item_id))
            except Exception as e:
                print(f"❌ Failed to add Issue #{num}: {e}")
                results.append((num, None))
        return results

    # ----------------------------------
    # Update a project field value for a specific issue (e.g., Due Date)
    # ----------------------------------
    def set_project_field_value(self, issue_number: int, field_name: str, value: str):
        """Set a project field value (like Status or Due Date) for a given issue on the board."""
        # 1️⃣ Ensure issue is already on project board
        issue_url = f"https://github.com/{self.repo_owner}/{self.repo_name}/issues/{issue_number}"
        item_id = self._find_project_item_id_by_issue_url(issue_url)
        if not item_id:
            print(f"⚠️ Issue #{issue_number} not yet in project. Adding it first...")
            item_id = self.add_issue_to_project(issue_number)

        # 2️⃣ Fetch all field definitions
        fields_query = """
        query($projectId: ID!) {
          node(id: $projectId) {
            ... on ProjectV2 {
              fields(first: 100) {
                nodes {
                  __typename
                  ... on ProjectV2FieldCommon {
                    id
                    name
                    dataType
                  }
                  ... on ProjectV2SingleSelectField {
                    id
                    name
                    dataType
                    options { id name }
                  }
                }
              }
            }
          }
        }
        """
        data = self.graphql(fields_query, {"projectId": self.project_id})
        all_fields = data["data"]["node"]["fields"]["nodes"]

        field = next((f for f in all_fields if f["name"].lower() == field_name.lower()), None)
        if not field:
            raise Exception(f"❌ Field '{field_name}' not found in project.")

        # 3️⃣ Build correct input value depending on data type
        if field["dataType"] == "DATE":
            field_value = {"date": value}
        elif field["dataType"] == "TEXT":
            field_value = {"text": value}
        elif field["dataType"] == "SINGLE_SELECT":
            option = next((o for o in field["options"] if o["name"].lower() == value.lower()), None)
            if not option:
                raise Exception(f"❌ Option '{value}' not found for field '{field_name}'.")
            field_value = {"singleSelectOptionId": option["id"]}
        else:
            raise Exception(f"⚠️ Unsupported field type: {field['dataType']} for '{field_name}'")

        # 4️⃣ Mutation to update the field
        mutation = """
        mutation($projectId: ID!, $itemId: ID!, $fieldId: ID!, $value: ProjectV2FieldValue!) {
          updateProjectV2ItemFieldValue(
            input: {
              projectId: $projectId
              itemId: $itemId
              fieldId: $fieldId
              value: $value
            }
          ) {
            projectV2Item { id }
          }
        }
        """
        variables = {
            "projectId": self.project_id,
            "itemId": item_id,
            "fieldId": field["id"],
            "value": field_value,
        }

        res = self.graphql(mutation, variables)
        print(f"✅ Set field '{field_name}' → {value} for Issue #{issue_number}")
        return res