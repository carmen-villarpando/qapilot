"""Template-based issue improvement engine."""

import json
import logging
import re
from typing import Any, Dict

logger = logging.getLogger(__name__)


class TemplateEngine:
    """Template-based engine for issue improvements."""

    def __init__(self, templates_file: str = "app/data/issue_templates.json"):
        """Initialize template engine."""
        self.templates_file = templates_file
        self.templates = self._load_templates()

    def _load_templates(self) -> Dict[str, Any]:
        """Load issue templates from JSON file."""
        try:
            with open(self.templates_file, "r", encoding="utf-8") as f:
                return json.load(f)
        except FileNotFoundError:
            logger.error(f"Templates file not found: {self.templates_file}")
            return {}
        except json.JSONDecodeError as e:
            logger.error(f"Error parsing templates file: {e}")
            return {}

    def _match_keywords(self, title: str, keywords: list[str]) -> bool:
        """Check if title contains any of the keywords."""
        title_lower = title.lower()
        return any(keyword.lower() in title_lower for keyword in keywords)

    def _find_matching_template(self, title: str) -> Dict[str, Any] | None:
        """Find the best matching template for the given title."""
        best_match = None
        max_matches = 0

        for template_name, template_data in self.templates.items():
            keywords = template_data.get("keywords", [])
            matches = sum(1 for keyword in keywords if keyword.lower() in title.lower())
            
            if matches > max_matches:
                max_matches = matches
                best_match = template_data

        return best_match

    def improve_issue(self, title: str, repository_context: str = "") -> Dict[str, Any]:
        """Generate issue improvements based on templates."""
        # Find matching template
        template = self._find_matching_template(title)
        
        if template:
            improvements = template["improvements"].copy()
            
            # Personalize the description with the actual title
            improvements["description"] = self._personalize_description(
                improvements["description"], title, repository_context
            )
            
            logger.info(f"Used template for: {title}")
            return improvements
        else:
            # Fallback to generic improvement
            logger.info(f"No template found for: {title}, using generic")
            return self._generate_generic_improvement(title, repository_context)

    def _personalize_description(self, description: str, title: str, repository_context: str) -> str:
        """Personalize the description with specific details."""
        # Extract key information from the title
        title_parts = title.lower().split()
        
        # Add specific context based on title
        personalized = description
        
        # Add repository context if available
        if repository_context:
            personalized += f"\n\n## 🏢 Contexto del Repositorio\n\n{repository_context}"
        
        # Add specific issue details
        personalized += f"\n\n## 🎯 Issue Específico\n\n**Título Original:** {title}\n"
        
        # Extract and highlight the main problem
        if "scroll" in title.lower():
            personalized += "**Tipo de Problema:** Problema de scroll/desplazamiento\n"
        elif "login" in title.lower() or "signin" in title.lower():
            personalized += "**Tipo de Problema:** Problema de autenticación\n"
        elif "botón" in title.lower() or "button" in title.lower():
            personalized += "**Tipo de Problema:** Problema de interacción con botones\n"
        elif "lento" in title.lower() or "performance" in title.lower():
            personalized += "**Tipo de Problema:** Problema de rendimiento\n"
        
        return personalized

    def _generate_generic_improvement(self, title: str, repository_context: str) -> Dict[str, Any]:
        """Generate a generic improvement when no template matches."""
        return {
            "description": f"""## 📝 Descripción del Problema

El usuario ha reportado un issue con el título: "{title}". Este problema necesita ser investigado y resuelto para mejorar la experiencia del usuario.

## 🔧 Pasos para Reproducir

1. Analizar el título del issue para entender el problema
2. Investigar el área afectada del código
3. Intentar reproducir el problema descrito
4. Documentar los hallazgos

## ✅ Comportamiento Esperado

El sistema debería funcionar correctamente sin el problema reportado. El usuario debería poder completar las tareas afectadas sin encontrar errores o comportamientos inesperados.

## 🏢 Contexto del Repositorio

{repository_context or "Contexto del repositorio no disponible."}

## 🎯 Próximos Pasos

1. Asignar este issue al equipo correspondiente
2. Investigar la causa raíz del problema
3. Implementar una solución
4. Probar la solución antes del despliegue
5. Documentar los cambios realizados""",
            "labels": ["bug", "needs-investigation"],
            "priority": "medium",
            "assignee": "triage-team"
        }

    def get_available_keywords(self) -> list[str]:
        """Get all available keywords from templates."""
        keywords = []
        for template_data in self.templates.values():
            keywords.extend(template_data.get("keywords", []))
        return list(set(keywords))
