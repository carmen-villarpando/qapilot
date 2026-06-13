"""Enhanced template engine with role-based improvements and external documentation."""

import json
import logging
import re
from typing import Dict, List, Any, Optional
from dataclasses import dataclass

import httpx
from app_terminology import AppTerminologyManager

logger = logging.getLogger(__name__)

@dataclass
class RoleContext:
    """Context for different roles in issue improvement."""
    role: str
    perspective: str
    focus_areas: List[str]
    documentation_urls: List[str]

class EnhancedTemplateEngine:
    """Enhanced template-based engine for issue improvements with role-based perspectives."""
    
    def __init__(self, templates_file: str = "data/enhanced_issue_templates.json"):
        """Initialize the enhanced template engine."""
        self.templates_file = templates_file
        self.templates = self._load_templates()
        self.terminology_manager = AppTerminologyManager()
        
        # Role definitions with their perspectives
        self.roles = {
            "qa_manager": RoleContext(
                role="QA Manager",
                perspective="Calidad y testing exhaustivo",
                focus_areas=["testing", "quality", "edge cases", "user acceptance"],
                documentation_urls=[
                    "https://www.istqb.org/",
                    "https://www.guru99.com/software-testing.html"
                ]
            ),
            "product_owner": RoleContext(
                role="Product Owner",
                perspective="Valor de negocio y experiencia del usuario",
                focus_areas=["business value", "user stories", "acceptance criteria", "stakeholders"],
                documentation_urls=[
                    "https://www.atlassian.com/agile/product-owner",
                    "https://www.scrum.org/resources/what-is-a-product-owner"
                ]
            ),
            "developer": RoleContext(
                role="Developer",
                perspective="Implementación técnica y mejores prácticas",
                focus_areas=["code quality", "architecture", "performance", "maintainability"],
                documentation_urls=[
                    "https://martinfowler.com/",
                    "https://12factor.net/"
                ]
            ),
            "security_engineer": RoleContext(
                role="Security Engineer",
                perspective="Seguridad y cumplimiento normativo",
                focus_areas=["security", "compliance", "vulnerabilities", "best practices"],
                documentation_urls=[
                    "https://owasp.org/",
                    "https://cwe.mitre.org/"
                ]
            ),
            "frontend_engineer": RoleContext(
                role="Frontend Engineer",
                perspective="UX/UI y experiencia del usuario",
                focus_areas=["ui", "ux", "accessibility", "responsive design"],
                documentation_urls=[
                    "https://web.dev/",
                    "https://developer.mozilla.org/en-US/"
                ]
            ),
            "backend_engineer": RoleContext(
                role="Backend Engineer",
                perspective="Arquitectura del servidor y datos",
                focus_areas=["api", "database", "performance", "scalability"],
                documentation_urls=[
                    "https://12factor.net/",
                    "https://microservices.io/"
                ]
            ),
            "performance_engineer": RoleContext(
                role="Performance Engineer",
                perspective="Optimización y métricas",
                focus_areas=["performance", "monitoring", "optimization", "metrics"],
                documentation_urls=[
                    "https://web.dev/vitals/",
                    "https://developer.mozilla.org/en-US/docs/Web/Performance"
                ]
            ),
            "ux_writer": RoleContext(
                role="UX Writer",
                perspective="Contenido y comunicación",
                focus_areas=["content", "localization", "accessibility", "user communication"],
                documentation_urls=[
                    "https://www.nngroup.com/",
                    "https://material.io/design/communication/"
                ]
            )
        }

    def _load_templates(self) -> Dict[str, Any]:
        """Load enhanced issue templates from JSON file."""
        try:
            with open(self.templates_file, 'r', encoding='utf-8') as f:
                return json.load(f)
        except FileNotFoundError:
            logger.error(f"Enhanced templates file not found: {self.templates_file}")
            return {}
        except json.JSONDecodeError as e:
            logger.error(f"Error parsing enhanced templates: {e}")
            return {}

    def _detect_role_from_title(self, title: str) -> str:
        """Detect the appropriate role based on issue title and content."""
        title_lower = title.lower()
        
        # Role detection patterns
        role_patterns = {
            "qa_manager": ["test", "testing", "qa", "calidad", "bug", "error", "issue"],
            "product_owner": ["feature", "requirement", "user story", "funcionalidad", "necesidad"],
            "security_engineer": ["security", "seguridad", "auth", "login", "password", "vulnerability"],
            "frontend_engineer": ["ui", "frontend", "button", "scroll", "interface", "design"],
            "backend_engineer": ["api", "backend", "database", "server", "export", "data"],
            "performance_engineer": ["performance", "slow", "lento", "rápido", "optimization", "carga"],
            "ux_writer": ["message", "text", "content", "copy", "error message", "comunicación"]
        }
        
        # Count matches for each role
        role_scores = {}
        for role, patterns in role_patterns.items():
            score = sum(1 for pattern in patterns if pattern in title_lower)
            if score > 0:
                role_scores[role] = score
        
        # Return role with highest score, default to developer
        if role_scores:
            return max(role_scores, key=role_scores.get)
        
        return "developer"

    def _fetch_external_documentation(self, urls: List[str]) -> str:
        """Fetch content from external documentation URLs."""
        content = []
        
        # Allowed domains for security
        allowed_domains = {
            "developer.mozilla.org",
            "web.dev", 
            "owasp.org",
            "www.istqb.org",
            "www.guru99.com",
            "www.atlassian.com",
            "www.scrum.org",
            "www.nngroup.com",
            "material.io",
            "csv.spec.whatwg.org",
            "www.w3.org"
        }
        
        for url in urls:
            try:
                # Validate URL domain
                from urllib.parse import urlparse
                parsed = urlparse(url)
                if parsed.netloc not in allowed_domains:
                    logger.warning(f"Blocked unauthorized domain: {parsed.netloc}")
                    content.append(f"### 📚 Referencia: {url}\n*Dominio no autorizado para seguridad*\n")
                    continue
                
                # Rate limiting: max 3 requests
                if len(content) >= 3:
                    logger.info("Rate limit reached for external documentation")
                    break
                
                response = httpx.get(url, timeout=5, follow_redirects=True)
                if response.status_code == 200:
                    # Extract basic content (simplified for demo)
                    text = response.text[:500]  # Reduced content size
                    content.append(f"### 📚 Referencia: {url}\n{text}...\n")
                else:
                    logger.warning(f"HTTP {response.status_code} from {url}")
                    content.append(f"### 📚 Referencia: {url}\n*Error al acceder al contenido*\n")
            except Exception as e:
                logger.warning(f"Failed to fetch documentation from {url}: {e}")
                content.append(f"### 📚 Referencia: {url}\n*No se pudo acceder al contenido*\n")
        
        return "\n".join(content)

    def _enhance_description_with_role(self, base_description: str, role_context: RoleContext, external_docs: List[str]) -> str:
        """Enhance the base description with role-specific perspective."""
        enhanced_sections = []
        
        # Add role perspective
        role_section = f"\n### 👤 Perspectiva de {role_context.role}\n\n**Enfoque:** {role_context.perspective}\n\n**Áreas clave:** {', '.join(role_context.focus_areas)}\n"
        enhanced_sections.append(role_section)
        
        # Add external documentation if available
        if external_docs:
            doc_content = self._fetch_external_documentation(external_docs)
            if doc_content:
                enhanced_sections.append(doc_content)
        
        # Combine with base description
        return base_description + "\n".join(enhanced_sections)

    def _iterate_poor_description(self, title: str, current_description: str) -> str:
        """Iterate on a poor description to make it more detailed and actionable."""
        if len(current_description.strip()) < 100:  # Consider it poor if too short
            # Generate a more detailed description based on title
            enhanced_description = f"""## 📝 Descripción del Problema

El miembro del equipo reporta: "{title}"

### 🎯 Análisis del Problema

Esta situación requiere atención inmediata ya que afecta directamente la experiencia del miembro y el funcionamiento esperado del sistema.

### 🔍 Contexto Adicional

 basado en el título proporcionado, este issue parece relacionado con funcionalidades críticas que necesitan ser abordadas para mantener la calidad y el rendimiento del sistema.

### 📋 Siguientes Pasos

1. Investigar el problema reportado
2. Reproducir el escenario descrito
3. Identificar la causa raíz
4. Implementar una solución adecuada
5. Verificar la corrección
6. Documentar los cambios realizados

### 🎪 Impacto

- **Miembros afectados:** Todos los usuarios de la plataforma
- **Urgencia:** Requiere atención prioritaria
- **Complejidad:** Por determinar tras análisis inicial"""
            
            return enhanced_description
        
        return current_description

    def improve_issue(self, title: str, repo_context: str = "", repo_name: str = "") -> Dict[str, Any]:
        """Improve an issue using enhanced templates with role-based perspectives and app terminology."""
        title_lower = title.lower()
        
        # Detect app from context
        detected_app = self.terminology_manager.detect_app_from_context(title, repo_name)
        logger.info(f"Detected app: {detected_app}")
        
        # Find matching template
        matched_template = None
        matched_category = None
        
        for category, template in self.templates.items():
            keywords = [kw.lower() for kw in template["keywords"]]
            if any(keyword in title_lower for keyword in keywords):
                matched_template = template
                matched_category = category
                break
        
        if not matched_template:
            logger.info(f"No enhanced template found for: {title}, using generic")
            return self._generate_generic_improvement(title, repo_context, detected_app)
        
        logger.info(f"Using enhanced template for: {title}")
        
        # Detect role
        detected_role = self._detect_role_from_title(title)
        role_context = self.roles.get(detected_role, self.roles["developer"])
        
        # Get base improvements
        improvements = matched_template["improvements"].copy()
        
        # Enhance description with role perspective
        base_description = improvements.get("description", "")
        external_docs = matched_template.get("external_docs", [])
        
        # Iterate on poor descriptions
        improved_description = self._iterate_poor_description(title, base_description)
        
        # Extract features mentioned in the title
        mentioned_features = self.terminology_manager.extract_features_from_text(title, detected_app)
        
        # Add app-specific terminology and feature validation
        enhanced_with_app = self.terminology_manager.enhance_description_with_validation(
            improved_description, detected_app, mentioned_features
        )
        
        # Add role-specific enhancements
        if detected_role != matched_template.get("role", "developer"):
            # Add additional role perspective if different from template role
            enhanced_description = self._enhance_description_with_role(
                enhanced_with_app, 
                role_context, 
                external_docs
            )
            improvements["description"] = enhanced_description
        else:
            improvements["description"] = enhanced_with_app
        
        # Add app documentation to external docs
        app_docs = self.terminology_manager.get_documentation_content(detected_app)
        all_external_docs = list(set(external_docs + app_docs))
        
        # Add role metadata
        improvements["detected_role"] = detected_role
        improvements["role_perspective"] = role_context.perspective
        improvements["detected_app"] = detected_app
        improvements["app_terminology"] = detected_app
        
        # Add enhanced labels based on role and app
        role_labels = {
            "qa_manager": ["quality", "testing"],
            "product_owner": ["product", "business-value"],
            "security_engineer": ["security", "compliance"],
            "frontend_engineer": ["frontend", "ui"],
            "backend_engineer": ["backend", "api"],
            "performance_engineer": ["performance", "optimization"],
            "ux_writer": ["content", "ux-writing"]
        }
        
        base_labels = improvements.get("labels", [])
        role_additional_labels = role_labels.get(detected_role, [])
        app_suggested_labels = self.terminology_manager.suggest_labels(title, detected_app)
        
        improvements["labels"] = list(set(base_labels + role_additional_labels + app_suggested_labels))
        
        # Add complexity and estimation if not present
        if "estimated_hours" not in improvements:
            improvements["estimated_hours"] = self._estimate_complexity(title, detected_role)
        
        if "complexity" not in improvements:
            improvements["complexity"] = self._determine_complexity(title, detected_role)
        
        return improvements

    def _generate_generic_improvement(self, title: str, repo_context: str = "", detected_app: str = "github") -> Dict[str, Any]:
        """Generate generic improvements when no template matches."""
        detected_role = self._detect_role_from_title(title)
        role_context = self.roles[detected_role]
        
        # Extract features mentioned in the title
        mentioned_features = self.terminology_manager.extract_features_from_text(title, detected_app)
        
        # Add app-specific terminology and feature validation
        app_enhanced_description = self.terminology_manager.enhance_description_with_validation(
            f"El miembro del equipo reporta: \"{title}\"", detected_app, mentioned_features
        )
        
        description = f"""## 📝 Descripción del Problema

{app_enhanced_description}

### 👤 Perspectiva de {role_context.role}

**Enfoque:** {role_context.perspective}

**Áreas clave:** {', '.join(role_context.focus_areas)}

### 🔧 Pasos para Reproducir

1. Acceder a la funcionalidad afectada
2. Identificar el escenario específico del problema
3. Reproducir el comportamiento no deseado
4. Documentar los resultados observados

### ✅ Comportamiento Esperado

El sistema debería funcionar de manera eficiente y predecible, proporcionando una experiencia positiva para el miembro del equipo.

### 📊 Criterios de Aceptación

- [ ] El problema está claramente identificado
- [ ] Se puede reproducir consistentemente
- [ ] Se implementa una solución efectiva
- [ ] La solución es verificada y probada
- [ ] No se introducen nuevos problemas
"""
        
        # Get app-specific labels
        app_labels = self.terminology_manager.suggest_labels(title, detected_app)
        
        return {
            "description": description,
            "labels": list(set(["bug", "needs-investigation", detected_role] + app_labels)),
            "priority": "medium",
            "assignee": "team-lead",
            "detected_role": detected_role,
            "role_perspective": role_context.perspective,
            "detected_app": detected_app,
            "app_terminology": detected_app,
            "estimated_hours": self._estimate_complexity(title, detected_role),
            "complexity": self._determine_complexity(title, detected_role)
        }

    def _estimate_complexity(self, title: str, role: str) -> int:
        """Estimate complexity based on title and role."""
        complexity_keywords = {
            "low": ["simple", "easy", "quick", "minor", "small"],
            "medium": ["medium", "moderate", "normal", "standard"],
            "high": ["complex", "difficult", "major", "critical", "urgent"]
        }
        
        title_lower = title.lower()
        
        for complexity, keywords in complexity_keywords.items():
            if any(keyword in title_lower for keyword in keywords):
                return {"low": 4, "medium": 8, "high": 16}[complexity]
        
        # Role-based default complexity
        role_complexity = {
            "qa_manager": 8,
            "product_owner": 6,
            "security_engineer": 12,
            "frontend_engineer": 6,
            "backend_engineer": 10,
            "performance_engineer": 12,
            "ux_writer": 4,
            "developer": 8
        }
        
        return role_complexity.get(role, 8)

    def _determine_complexity(self, title: str, role: str) -> str:
        """Determine complexity level as string."""
        hours = self._estimate_complexity(title, role)
        
        if hours <= 6:
            return "low"
        elif hours <= 12:
            return "medium"
        else:
            return "high"
