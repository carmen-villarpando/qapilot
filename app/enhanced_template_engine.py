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
                perspective="Quality and comprehensive testing",
                focus_areas=["testing", "quality", "edge cases", "user acceptance"],
                documentation_urls=[
                    "https://www.istqb.org/",
                    "https://www.guru99.com/software-testing.html"
                ]
            ),
            "product_owner": RoleContext(
                role="Product Owner",
                perspective="Business value and user experience",
                focus_areas=["business value", "user stories", "acceptance criteria", "stakeholders"],
                documentation_urls=[
                    "https://www.atlassian.com/agile/product-owner",
                    "https://www.scrum.org/resources/what-is-a-product-owner"
                ]
            ),
            "developer": RoleContext(
                role="Developer",
                perspective="Technical implementation and best practices",
                focus_areas=["code quality", "architecture", "performance", "maintainability"],
                documentation_urls=[
                    "https://martinfowler.com/",
                    "https://12factor.net/"
                ]
            ),
            "security_engineer": RoleContext(
                role="Security Engineer",
                perspective="Security and compliance",
                focus_areas=["security", "compliance", "vulnerabilities", "best practices"],
                documentation_urls=[
                    "https://owasp.org/",
                    "https://cwe.mitre.org/"
                ]
            ),
            "frontend_engineer": RoleContext(
                role="Frontend Engineer",
                perspective="UX/UI and user experience",
                focus_areas=["ui", "ux", "accessibility", "responsive design"],
                documentation_urls=[
                    "https://web.dev/",
                    "https://developer.mozilla.org/en-US/"
                ]
            ),
            "backend_engineer": RoleContext(
                role="Backend Engineer",
                perspective="Server architecture and data",
                focus_areas=["api", "database", "performance", "scalability"],
                documentation_urls=[
                    "https://12factor.net/",
                    "https://microservices.io/"
                ]
            ),
            "performance_engineer": RoleContext(
                role="Performance Engineer",
                perspective="Optimization and metrics",
                focus_areas=["performance", "monitoring", "optimization", "metrics"],
                documentation_urls=[
                    "https://web.dev/vitals/",
                    "https://developer.mozilla.org/en-US/docs/Web/Performance"
                ]
            ),
            "ux_writer": RoleContext(
                role="UX Writer",
                perspective="Content and communication",
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
            "qa_manager": ["test", "testing", "qa", "quality", "bug", "error", "issue"],
            "product_owner": ["feature", "requirement", "user story", "functionality", "need"],
            "security_engineer": ["security", "auth", "login", "password", "vulnerability"],
            "frontend_engineer": ["ui", "frontend", "button", "scroll", "interface", "design"],
            "backend_engineer": ["api", "backend", "database", "server", "export", "data"],
            "performance_engineer": ["performance", "slow", "fast", "optimization", "load"],
            "ux_writer": ["message", "text", "content", "copy", "error message", "communication"]
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
                    content.append(f"### 📚 Reference: {url}\n*Unauthorized domain blocked for security*\n")
                    continue
                
                # Rate limiting: max 3 requests
                if len(content) >= 3:
                    logger.info("Rate limit reached for external documentation")
                    break
                
                response = httpx.get(url, timeout=5, follow_redirects=True)
                if response.status_code == 200:
                    # Extract basic content (simplified for demo)
                    text = response.text[:500]  # Reduced content size
                    content.append(f"### 📚 Reference: {url}\n{text}...\n")
                else:
                    logger.warning(f"HTTP {response.status_code} from {url}")
                    content.append(f"### 📚 Reference: {url}\n*Error accessing content*\n")
            except Exception as e:
                logger.warning(f"Failed to fetch documentation from {url}: {e}")
                content.append(f"### 📚 Reference: {url}\n*Could not access content*\n")
        
        return "\n".join(content)

    def _enhance_description_with_role(self, base_description: str, role_context: RoleContext, external_docs: List[str]) -> str:
        """Enhance the base description with role-specific perspective."""
        enhanced_sections = []
        
        # Add role perspective
        role_section = f"\n### 👤 {role_context.role} Perspective\n\n**Focus:** {role_context.perspective}\n\n**Key Areas:** {', '.join(role_context.focus_areas)}\n"
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
            enhanced_description = f"""## 📝 Problem Description

Team member reports: "{title}"

### 🎯 Problem Analysis

This situation requires immediate attention as it directly affects the member experience and expected system functionality.

### 🔍 Additional Context

Based on the provided title, this issue appears related to critical functionalities that need to be addressed to maintain system quality and performance.

### 📋 Next Steps

1. Investigate the reported problem
2. Reproduce the described scenario
3. Identify the root cause
4. Implement an appropriate solution
5. Verify the correction
6. Document the changes made

### 🎪 Impact

- **Affected members:** All platform users
- **Urgency:** Requires priority attention
- **Complexity:** To be determined after initial analysis"""
            
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
            f"Team member reports: \"{title}\"", detected_app, mentioned_features
        )
        
        description = f"""## 📝 Problem Description

{app_enhanced_description}

### 👤 {role_context.role} Perspective

**Focus:** {role_context.perspective}

**Key Areas:** {', '.join(role_context.focus_areas)}

### 🔧 Steps to Reproduce

1. Access the affected functionality
2. Identify the specific problem scenario
3. Reproduce the undesired behavior
4. Document the observed results

### ✅ Expected Behavior

The system should function efficiently and predictably, providing a positive experience for team members.

### 📊 Acceptance Criteria

- [ ] The problem is clearly identified
- [ ] It can be reproduced consistently
- [ ] An effective solution is implemented
- [ ] The solution is verified and tested
- [ ] No new problems are introduced
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
