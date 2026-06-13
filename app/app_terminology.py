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
    jerga: List[str]  # Common phrases/expressions
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
                    "agile": "Metodología ágil para gestión de proyectos iterativa",
                    "scrum": "Framework ágil con sprints, roles y ceremonias definidas",
                    "kanban": "Sistema visual de gestión del flujo de trabajo",
                    "user_story": "Descripción de una funcionalidad desde perspectiva del usuario",
                    "velocity": "Métrica de cantidad de trabajo completado por sprint",
                    "burndown": "Gráfico que muestra trabajo restante vs tiempo",
                    "definition_of_done": "Criterios que debe cumplir una tarea para estar completa",
                    "points": "Estimación de esfuerzo relativo (story points)"
                },
                documentation_urls=[
                    "https://docs.taiga.io/",
                    "https://taiga.io/features/",
                    "https://github.com/taigaio/taiga-doc"
                ],
                jerga=[
                    "Vamos a crear una user story para esto",
                    "Necesitamos puntos para esta tarea",
                    "¿Cuál es la velocity del equipo?",
                    "Esto va en el backlog del producto",
                    "Hagamos un planning poker",
                    "El burndown muestra que vamos bien",
                    "Cumple con la Definition of Done",
                    "Movamos esto al siguiente sprint",
                    "Esto es un bloqueo, necesitamos desbloquear",
                    "El workflow está optimizado"
                ],
                features={
                    "kanban_boards": "Tableros Kanban con gestión visual del flujo",
                    "scrum_boards": "Tableros Scrum con sprints y backlog",
                    "issues": "Gestión de issues y bugs integrada",
                    "wiki": "Documentación integrada en el proyecto",
                    "epics": "Gestión de epics para grandes funcionalidades",
                    "tasks": "Descomposición de user stories en tareas",
                    "time_tracking": "Seguimiento de tiempo por tarea",
                    "integrations": "Integraciones con GitHub, GitLab, Slack"
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
                    "work_package": "Unidad básica de trabajo en OpenProject",
                    "project_hierarchy": "Estructura jerárquica de proyectos y subproyectos",
                    "cost_tracking": "Gestión de costos y presupuesto",
                    "time_tracking": "Registro de horas trabajadas",
                    "gantt": "Diagrama de Gantt para planificación",
                    "wp_types": "Tipos de work packages (Task, Bug, Feature, etc.)",
                    "status_workflow": "Flujo de estados personalizable",
                    "custom_fields": "Campos personalizados adicionales"
                },
                documentation_urls=[
                    "https://www.openproject.org/docs/",
                    "https://www.openproject.org/features/",
                    "https://api.openproject.org/"
                ],
                jerga=[
                    "Creemos un work package para esto",
                    "Esto necesita un tipo específico de WP",
                    "El Gantt muestra la dependencia",
                    "Registremos las horas en el time tracking",
                    "El cost tracking está actualizado",
                    "El workflow del status está bien configurado",
                    "Necesitamos revisar el project hierarchy",
                    "Esto va en la versión 2.0",
                    "El custom field captura esta información",
                    "La assignee ya está asignada"
                ],
                features={
                    "gantt_charts": "Diagramas de Gantt para planificación",
                    "cost_tracking": "Seguimiento de costos y presupuesto",
                    "time_tracking": "Registro de tiempo y horas trabajadas",
                    "project_hierarchy": "Estructura de proyectos y subproyectos",
                    "work_packages": "Gestión de paquetes de trabajo",
                    "team_planner": "Planificación visual de equipo",
                    "boards": "Tableros ágiles con configuración flexible",
                    "wiki": "Documentación colaborativa integrada"
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
                    "pull_request": "Propuesta de cambios al código",
                    "fork": "Copia personal de un repositorio",
                    "branch": "Rama de desarrollo paralela",
                    "merge": "Integración de cambios",
                    "commit": "Punto de guardado en el historial",
                    "repository": "Almacén de código y archivos",
                    "workflow": "Automatización con GitHub Actions",
                    "release": "Versión publicada del software"
                },
                documentation_urls=[
                    "https://docs.github.com/",
                    "https://docs.github.com/en/issues",
                    "https://docs.github.com/en/projects"
                ],
                jerga=[
                    "Abramos un issue para esto",
                    "Hagamos un pull request",
                    "Esto necesita un merge",
                    "Creemos una rama nueva",
                    "El workflow se ejecutará automáticamente",
                    "Hagamos fork del repositorio",
                    "Esto va en el milestone v2.0",
                    "El commit está listo",
                    "La release está publicada",
                    "El project board está actualizado"
                ],
                features={
                    "issues": "Seguimiento de problemas y tareas",
                    "projects": "Tableros de proyecto kanban",
                    "actions": "Automatización de workflows",
                    "pull_requests": "Revisión y fusión de código",
                    "releases": "Gestión de versiones",
                    "pages": "Sitios web estáticos",
                    "packages": "Registro de paquetes",
                    "discussions": "Foros de discusión"
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

    def enhance_description_with_jerga(self, description: str, app_name: str) -> str:
        """Enhance description with app-specific jargon and terminology."""
        terminology = self.get_app_terminology(app_name)
        
        if not terminology:
            return description
        
        enhanced = description
        
        # Add app-specific context
        enhanced += f"\n\n## 🎯 Contexto de {terminology.name}\n\n"
        
        # Add relevant concepts
        enhanced += "**Conceptos Clave:**\n"
        for concept, explanation in list(terminology.concepts.items())[:3]:
            enhanced += f"- **{concept.replace('_', ' ').title()}**: {explanation}\n"
        
        enhanced += "\n**Terminología Específica:**\n"
        for generic, specific in list(terminology.terms.items())[:5]:
            enhanced += f"- **{specific}**: {generic.title()}\n"
        
        enhanced += "\n**Jerga Común del Equipo:**\n"
        for jerga in terminology.jerga[:3]:
            enhanced += f"- \"{jerga}\"\n"
        
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
        enhanced += f"\n\n## 🎯 Contexto de {terminology.name}\n\n"
        
        # Validate mentioned features
        if mentioned_features:
            enhanced += "**Validación de Funcionalidades:**\n"
            for feature in mentioned_features:
                if self.validate_feature_exists(feature, app_name):
                    enhanced += f"- ✅ **{feature}**: Funcionalidad confirmada en {terminology.name}\n"
                else:
                    enhanced += f"- ⚠️ **{feature}**: Esta funcionalidad no existe o no está confirmada en {terminology.name}\n"
            enhanced += "\n"
        
        # Add relevant concepts
        enhanced += "**Conceptos Clave:**\n"
        for concept, explanation in list(terminology.concepts.items())[:3]:
            enhanced += f"- **{concept.replace('_', ' ').title()}**: {explanation}\n"
        
        enhanced += "\n**Terminología Específica:**\n"
        for generic, specific in list(terminology.terms.items())[:5]:
            enhanced += f"- **{specific}**: {generic.title()}\n"
        
        enhanced += "\n**Jerga Común del Equipo:**\n"
        for jerga in terminology.jerga[:3]:
            enhanced += f"- \"{jerga}\"\n"
        
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
        common_features = ["kanban", "scrum", "gantt", "board", "tablero", "sprint", "backlog"]
        for feature in common_features:
            if feature in text_lower:
                mentioned_features.append(feature)
        
        return list(set(mentioned_features))
