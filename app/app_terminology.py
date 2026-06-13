"""App-specific terminology and jargon for different products."""

from typing import Dict, List, Any
from dataclasses import dataclass
import re

@dataclass
class AppTerminology:
    """Terminology and jargon for a specific app."""
    name: str
    terms: Dict[str, str]  # Generic term -> App-specific term
    concepts: Dict[str, str]  # Concept -> App-specific description
    documentation_urls: List[str]
    slang: List[str]  # Common phrases/expressions
    features: Dict[str, str]  # Feature -> Description

class AppTerminologyManager:
    """Manager for app-specific terminology and jargon."""

    def __init__(self):
        """Initialize the terminology manager."""
        self.apps = {
            "taiga": AppTerminology(
                name="Taiga",
                terms={
                    "issue": "User Story",
                    "task": "Task",
                    "bug": "Issue",
                    "epic": "Epic",
                    "sprint": "Sprint",
                    "backlog": "Product Backlog",
                    "board": "Project Board",
                    "column": "Swimlane",
                    "label": "Tag",
                    "assignee": "Assigned to",
                    "priority": "Priority",
                    "status": "Status",
                    "description": "Description",
                    "title": "Subject",
                    "comment": "Note",
                    "attachment": "Attachment",
                    "milestone": "Milestone"
                },
                concepts={
                    "agile": "Iterative project management methodology",
                    "scrum": "Agile framework with sprints, roles and defined ceremonies",
                    "kanban": "Visual workflow management system",
                    "user_story": "Functionality description from user perspective",
                    "velocity": "Metric of work completed per sprint",
                    "burndown": "Chart showing remaining work vs time",
                    "definition_of_done": "Criteria a task must meet to be complete",
                    "points": "Relative effort estimation (story points)"
                },
                documentation_urls=[
                    "https://docs.taiga.io/",
                    "https://taiga.io/features/",
                    "https://github.com/taigaio/taiga-doc"
                ],
                jerga=[
                    "Let's create a user story for this",
                    "We need points for this task",
                    "What's the team velocity?",
                    "This goes in the product backlog",
                    "Let's do planning poker",
                    "The burndown shows we're on track",
                    "It meets the Definition of Done",
                    "Let's move this to the next sprint",
                    "This is a blocker, we need to unblock",
                    "The workflow is optimized"
                ],
                features={
                    "kanban_boards": "Kanban boards with visual flow management",
                    "scrum_boards": "Scrum boards with sprints and backlog",
                    "issues": "Integrated issue and bug management",
                    "wiki": "Integrated project documentation",
                    "epics": "Epic management for large functionalities",
                    "tasks": "User story decomposition into tasks",
                    "time_tracking": "Time tracking per task",
                    "integrations": "Integrations with GitHub, GitLab, Slack"
                }
            ),
            "openproject": AppTerminology(
                name="OpenProject",
                terms={
                    "issue": "Work Package",
                    "task": "Task",
                    "bug": "Bug",
                    "epic": "Epic",
                    "sprint": "Sprint",
                    "backlog": "Backlog",
                    "board": "Board",
                    "column": "Status",
                    "label": "Category",
                    "assignee": "Assignee",
                    "priority": "Priority",
                    "status": "Status",
                    "description": "Description",
                    "title": "Subject",
                    "comment": "Comment",
                    "attachment": "Attachment",
                    "milestone": "Version"
                },
                concepts={
                    "work_package": "Basic work unit in OpenProject",
                    "project_hierarchy": "Hierarchical structure of projects and subprojects",
                    "cost_tracking": "Cost and budget management",
                    "time_tracking": "Work hours registration",
                    "gantt": "Gantt chart for planning",
                    "wp_types": "Work package types (Task, Bug, Feature, etc.)",
                    "status_workflow": "Customizable status flow",
                    "custom_fields": "Additional custom fields"
                },
                documentation_urls=[
                    "https://www.openproject.org/docs/",
                    "https://www.openproject.org/features/",
                    "https://api.openproject.org/"
                ],
                jerga=[
                    "Let's create a work package for this",
                    "This needs a specific WP type",
                    "The Gantt shows the dependency",
                    "Let's log the hours in time tracking",
                    "Cost tracking is up to date",
                    "The status workflow is well configured",
                    "We need to review the project hierarchy",
                    "This goes in version 2.0",
                    "The custom field captures this information",
                    "The assignee is already assigned"
                ],
                features={
                    "gantt_charts": "Gantt charts for planning",
                    "cost_tracking": "Cost and budget tracking",
                    "time_tracking": "Time and work hours tracking",
                    "project_hierarchy": "Project and subproject structure",
                    "work_packages": "Work package management",
                    "team_planner": "Visual team planning",
                    "boards": "Agile boards with flexible configuration",
                    "wiki": "Integrated collaborative documentation"
                }
            ),
            "github": AppTerminology(
                name="GitHub",
                terms={
                    "issue": "Issue",
                    "task": "Task",
                    "bug": "Bug",
                    "epic": "Epic",
                    "sprint": "Milestone",
                    "backlog": "Backlog",
                    "board": "Project Board",
                    "column": "Column",
                    "label": "Label",
                    "assignee": "Assignee",
                    "priority": "Priority",
                    "status": "Status",
                    "description": "Description",
                    "title": "Title",
                    "comment": "Comment",
                    "attachment": "Attachment",
                    "milestone": "Milestone"
                },
                concepts={
                    "pull_request": "Code change proposal",
                    "fork": "Personal copy of a repository",
                    "branch": "Parallel development branch",
                    "merge": "Integration of changes",
                    "commit": "Save point in history",
                    "repository": "Code and files storage",
                    "workflow": "Automation with GitHub Actions",
                    "release": "Published software version"
                },
                documentation_urls=[
                    "https://docs.github.com/",
                    "https://docs.github.com/en/issues",
                    "https://docs.github.com/en/projects"
                ],
                jerga=[
                    "Let's open an issue for this",
                    "Let's make a pull request",
                    "This needs a merge",
                    "Let's create a new branch",
                    "The workflow will run automatically",
                    "Let's fork the repository",
                    "This goes in milestone v2.0",
                    "The commit is ready",
                    "The release is published",
                    "The project board is updated"
                ],
                features={
                    "issues": "Problem and task tracking",
                    "projects": "Kanban project boards",
                    "actions": "Workflow automation",
                    "pull_requests": "Code review and merging",
                    "releases": "Version management",
                    "pages": "Static websites",
                    "packages": "Package registry",
                    "discussions": "Discussion forums"
                }
            )
        }

    def get_app_terminology(self, app_name: str) -> AppTerminology | None:
        """Get terminology for a specific app."""
        return self.apps.get(app_name.lower())

    def translate_text(self, text: str, from_app: str, to_app: str) -> str:
        """Translate text from one app terminology to another."""
        from_terminology = self.get_app_terminology(from_app)
        to_terminology = self.get_app_terminology(to_app)
        
        if not from_terminology or not to_terminology:
            return text
        
        translated = text
        
        # Translate terms
        for generic_term, from_term in from_terminology.terms.items():
            if generic_term in to_terminology.terms:
                to_term = to_terminology.terms[generic_term]
                # Case-insensitive replacement
                pattern = re.compile(re.escape(from_term), re.IGNORECASE)
                translated = pattern.sub(to_term, translated)
        
        return translated

    def enhance_description_with_slang(self, description: str, app_name: str) -> str:
        """Enhance description with app-specific slang and terminology."""
        terminology = self.get_app_terminology(app_name)
        
        if not terminology:
            return description
        
        enhanced = description
        
        # Add app-specific context
        enhanced += f"\n\n## 🎯 {terminology.name} Context\n\n"
        
        # Add relevant concepts
        enhanced += "**Key Concepts:**\n"
        for concept, explanation in list(terminology.concepts.items())[:3]:
            enhanced += f"- **{concept.replace('_', ' ').title()}**: {explanation}\n"
        
        enhanced += "\n**Specific Terminology:**\n"
        for generic, specific in list(terminology.terms.items())[:5]:
            enhanced += f"- **{specific}**: {generic.title()}\n"
        
        enhanced += "\n**Common Team Slang:**\n"
        for slang in terminology.slang[:3]:
            enhanced += f"- \"{slang}\"\n"
        
        return enhanced

    def get_documentation_content(self, app_name: str) -> List[str]:
        """Get documentation URLs for an app."""
        terminology = self.get_app_terminology(app_name)
        return terminology.documentation_urls if terminology else []

    def suggest_labels(self, title: str, app_name: str) -> List[str]:
        """Suggest appropriate labels based on app and title."""
        terminology = self.get_app_terminology(app_name)
        
        if not terminology:
            return ["bug", "enhancement"]
        
        labels = []
        title_lower = title.lower()
        
        # App-specific label suggestions
        if app_name == "taiga":
            if "user story" in title_lower or "story" in title_lower:
                labels.append("user-story")
            if "bug" in title_lower or "issue" in title_lower:
                labels.append("bug")
            if "epic" in title_lower:
                labels.append("epic")
            if "task" in title_lower:
                labels.append("task")
            labels.extend(["agile", "taiga"])
                
        elif app_name == "openproject":
            if "work package" in title_lower or "wp" in title_lower:
                labels.append("work-package")
            if "bug" in title_lower:
                labels.append("bug")
            if "feature" in title_lower:
                labels.append("feature")
            if "task" in title_lower:
                labels.append("task")
            labels.extend(["openproject", "enterprise"])
            
        elif app_name == "github":
            if "pull request" in title_lower or "pr" in title_lower:
                labels.append("pull-request")
            if "bug" in title_lower:
                labels.append("bug")
            if "enhancement" in title_lower:
                labels.append("enhancement")
            if "documentation" in title_lower:
                labels.append("documentation")
            labels.extend(["github", "oss"])
        
        return list(set(labels))

    def detect_app_from_context(self, text: str, repo_name: str = "") -> str:
        """Detect which app the context is referring to."""
        text_lower = text.lower()
        repo_lower = repo_name.lower()
        
        # Check for explicit mentions
        app_keywords = {
            "taiga": ["taiga", "user story", "sprint planning", "backlog", "velocity", "kanban", "tablero kanban", "project board"],
            "openproject": ["openproject", "work package", "cost tracking", "gantt", "board"],
            "github": ["github", "pull request", "commit", "repository", "fork", "issue"]
        }
        
        for app, keywords in app_keywords.items():
            if any(keyword in text_lower for keyword in keywords):
                return app
            if any(keyword in repo_lower for keyword in keywords):
                return app
        
        return "github"  # Default to GitHub

    def validate_feature_exists(self, feature_name: str, app_name: str) -> bool:
        """Validate if a feature exists in the specific app."""
        terminology = self.get_app_terminology(app_name)
        
        if not terminology:
            return False
        
        # Check if feature exists in the app's features
        if feature_name.lower() in terminology.features:
            return True
        
        # Check common feature mappings
        feature_mappings = {
            "taiga": {
                "kanban": "kanban_boards",
                "kanban board": "kanban_boards", 
                "tablero kanban": "kanban_boards",
                "scrum": "scrum_boards",
                "tablero scrum": "scrum_boards"
            },
            "openproject": {
                "gantt": "gantt_charts",
                "cost tracking": "cost_tracking",
                "time tracking": "time_tracking",
                "work package": "work_packages"
            },
            "github": {
                "pull request": "pull_requests",
                "pr": "pull_requests",
                "actions": "actions",
                "releases": "releases"
            }
        }
        
        app_features = feature_mappings.get(app_name, {})
        return feature_name.lower() in app_features

    def enhance_description_with_validation(self, description: str, app_name: str, mentioned_features: List[str]) -> str:
        """Enhance description with app-specific terminology and feature validation."""
        terminology = self.get_app_terminology(app_name)
        
        if not terminology:
            return description
        
        enhanced = description
        
        # Add app-specific context
        enhanced += f"\n\n## 🎯 {terminology.name} Context\n\n"
        
        # Validate mentioned features
        if mentioned_features:
            enhanced += "**Feature Validation:**\n"
            for feature in mentioned_features:
                if self.validate_feature_exists(feature, app_name):
                    enhanced += f"- ✅ **{feature}**: Confirmed functionality in {terminology.name}\n"
                else:
                    enhanced += f"- ⚠️ **{feature}**: This functionality does not exist or is not confirmed in {terminology.name}\n"
            enhanced += "\n"
        
        # Add relevant concepts
        enhanced += "**Key Concepts:**\n"
        for concept, explanation in list(terminology.concepts.items())[:3]:
            enhanced += f"- **{concept.replace('_', ' ').title()}**: {explanation}\n"
        
        enhanced += "\n**Specific Terminology:**\n"
        for generic, specific in list(terminology.terms.items())[:5]:
            enhanced += f"- **{specific}**: {generic.title()}\n"
        
        enhanced += "\n**Common Team Slang:**\n"
        for slang in terminology.slang[:3]:
            enhanced += f"- \"{slang}\"\n"
        
        return enhanced

    def extract_features_from_text(self, text: str, app_name: str) -> List[str]:
        """Extract potential features mentioned in text."""
        terminology = self.get_app_terminology(app_name)
        
        if not terminology:
            return []
        
        text_lower = text.lower()
        mentioned_features = []
        
        # Check for feature mentions
        for feature_name in terminology.features:
            if feature_name.replace("_", " ").lower() in text_lower:
                mentioned_features.append(feature_name.replace("_", " "))
        
        # Check common feature names
        common_features = ["kanban", "scrum", "gantt", "board", "sprint", "backlog"]
        for feature in common_features:
            if feature in text_lower:
                mentioned_features.append(feature)
        
        return list(set(mentioned_features))
