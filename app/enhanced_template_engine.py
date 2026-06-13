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
        
        # Generate contextual description based on title analysis
        contextual_description = self._generate_contextual_description(title, detected_app, detected_role, mentioned_features)
        
        # Add app-specific terminology and feature validation
        app_enhanced_description = self.terminology_manager.enhance_description_with_validation(
            contextual_description, detected_app, mentioned_features
        )
        
        description = f"""## 📝 Description

{app_enhanced_description}

### 👤 {role_context.role} Perspective

**Focus:** {role_context.perspective}

**Key Areas:** {', '.join(role_context.focus_areas)}

### 🔧 Steps to Reproduce

{self._generate_contextual_steps(title, detected_app, detected_role)}

### ✅ Expected Behavior

{self._generate_contextual_expected_behavior(title, detected_app, detected_role)}

### 📊 Acceptance Criteria

{self._generate_contextual_acceptance_criteria(title, detected_app, detected_role)}
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

    def _generate_contextual_description(self, title: str, detected_app: str, detected_role: str, mentioned_features: List[str]) -> str:
        """Generate contextual description based on title analysis."""
        title_lower = title.lower()
        
        # Analyze title for specific patterns and generate rich description
        if "kanban" in title_lower and "taiga" in title_lower:
            return """Team member reports that when attempting to access an active kanban board in the Taiga project, the board fails to load properly. This critical issue prevents team members from viewing the current workflow status, tracking progress on user stories, and managing task assignments across different swimlanes. The loading failure appears to affect the main kanban view, potentially impacting sprint planning and daily standup activities."""
        
        elif "login" in title_lower or "authentication" in title_lower:
            return """Team member experiences authentication issues when attempting to access the system. This problem prevents users from logging in securely, potentially blocking access to critical project functionality and compromising the user experience. The authentication failure may be related to credential validation, session management, or connectivity with the authentication service."""
        
        elif "scroll" in title_lower or "scrolling" in title_lower:
            return """Team member reports scrolling functionality is not working correctly in the interface. This issue affects user navigation and content accessibility, particularly when trying to view content that extends beyond the visible viewport. The scrolling problem impacts user experience and may prevent users from accessing important information or completing essential tasks."""
        
        elif "button" in title_lower or "click" in title_lower:
            return """Team member reports that interactive buttons are not responding to user clicks or are not performing their intended actions. This issue prevents users from completing critical workflows, submitting forms, or navigating through the application interface. The button malfunction may be related to event handling, JavaScript execution, or CSS styling problems."""
        
        elif "performance" in title_lower or "slow" in title_lower or "lag" in title_lower:
            return """Team member reports significant performance issues affecting system responsiveness. The application is experiencing slow load times, delayed responses to user actions, or general performance degradation that impacts productivity. These performance bottlenecks may be related to database queries, API calls, frontend rendering, or resource optimization."""
        
        else:
            # Generic but contextual description
            return f"""Team member reports an issue with {detected_app} that requires immediate attention. This problem affects the normal operation of the system and may impact team productivity and project deliverables. The issue needs to be investigated and resolved to ensure smooth workflow continuation and maintain system reliability."""

    def _generate_contextual_steps(self, title: str, detected_app: str, detected_role: str) -> str:
        """Generate contextual reproduction steps based on title analysis."""
        title_lower = title.lower()
        
        if "kanban" in title_lower and "taiga" in title_lower:
            return """1. Log in to the Taiga application
2. Navigate to the affected project
3. Click on the "Kanban" tab or board view
4. Observe that the board fails to load or displays loading spinner indefinitely
5. Try refreshing the page to verify if the issue persists
6. Check browser console for any JavaScript errors
7. Test with different browsers to isolate the problem"""
        
        elif "login" in title_lower or "authentication" in title_lower:
            return """1. Navigate to the application login page
2. Enter valid credentials (username/email and password)
3. Click the login button or press Enter
4. Observe the authentication process and any error messages
5. Check if the page redirects correctly after successful login
6. Verify network connectivity and browser console for errors
7. Test with different user accounts if available"""
        
        elif "scroll" in title_lower or "scrolling" in title_lower:
            return """1. Navigate to the page or section with scrolling issues
2. Attempt to scroll using mouse wheel, trackpad, or keyboard arrows
3. Observe if the content moves or remains static
4. Test horizontal and vertical scrolling separately
5. Check if scrollbars appear when content overflows
6. Test on different screen sizes and devices
7. Verify browser developer tools for CSS issues"""
        
        elif "button" in title_lower or "click" in title_lower:
            return """1. Navigate to the page containing the affected button
2. Attempt to click the button using mouse or touch
3. Observe if any visual feedback occurs (hover, active states)
4. Check browser console for JavaScript errors
5. Verify if the button is properly enabled and not disabled
6. Test keyboard navigation (Tab to button, Enter/Space to activate)
7. Check if button event listeners are properly attached"""
        
        elif "performance" in title_lower or "slow" in title_lower or "lag" in title_lower:
            return """1. Navigate to the affected page or feature
2. Measure initial load time using browser dev tools
3. Monitor network requests and their response times
4. Check CPU and memory usage during operation
5. Test with different amounts of data or content
6. Profile JavaScript execution time if applicable
7. Compare performance across different browsers and devices"""
        
        else:
            return """1. Navigate to the affected area of the application
2. Identify the specific functionality that is not working
3. Attempt to reproduce the issue with different inputs
4. Document the exact steps that trigger the problem
5. Check for any error messages or unusual behavior
6. Verify the issue occurs consistently
7. Gather relevant logs or debugging information"""

    def _generate_contextual_expected_behavior(self, title: str, detected_app: str, detected_role: str) -> str:
        """Generate contextual expected behavior based on title analysis."""
        title_lower = title.lower()
        
        if "kanban" in title_lower and "taiga" in title_lower:
            return """The kanban board should load quickly and display all project columns (swimlanes) with their respective user stories and tasks. Users should be able to:
- View all columns and their cards clearly
- Drag and drop cards between columns
- Filter and search for specific items
- Access card details by clicking on them
- See real-time updates when team members make changes
- Experience smooth scrolling and responsive interactions"""
        
        elif "login" in title_lower or "authentication" in title_lower:
            return """The authentication system should work seamlessly and securely:
- Users should be able to log in with valid credentials
- The login process should complete within 2-3 seconds
- Invalid credentials should show clear, helpful error messages
- Successful login should redirect to the appropriate dashboard
- Session should persist appropriately without requiring frequent re-login
- Two-factor authentication should work if enabled
- Password reset functionality should be accessible and functional"""
        
        elif "scroll" in title_lower or "scrolling" in title_lower:
            return """Scrolling should work smoothly and intuitively across all content areas:
- Mouse wheel scrolling should work at appropriate speed
- Touchpad scrolling should support natural gestures
- Keyboard navigation (arrow keys, space, page up/down) should function
- Scrollbars should appear when content overflows viewport
- Momentum scrolling should work on touch devices
- Scroll performance should maintain 60fps during movement
- Content should snap appropriately to sections or items when designed"""
        
        elif "button" in title_lower or "click" in title_lower:
            return """Buttons should respond immediately and reliably to user interactions:
- Visual feedback should appear on hover (color change, underline, etc.)
- Active state should show when button is pressed
- Click should trigger the intended action without delay
- Buttons should be accessible via keyboard navigation
- Loading states should show for async operations
- Disabled buttons should be clearly visually indicated
- Touch targets should be at least 44x44px for mobile accessibility"""
        
        elif "performance" in title_lower or "slow" in title_lower or "lag" in title_lower:
            return """The application should perform optimally with responsive interactions:
- Page loads should complete within 2-3 seconds
- User interactions should respond within 100ms
- Animations should maintain 60fps performance
- Memory usage should remain stable without leaks
- Network requests should be optimized and cached appropriately
- Database queries should execute efficiently
- The application should handle concurrent users without degradation"""
        
        else:
            return f"""The {detected_app} system should function reliably and efficiently:
- All features should work as designed and documented
- User interactions should be responsive and intuitive
- Error handling should be graceful and informative
- The system should maintain data integrity and consistency
- Performance should meet acceptable standards for the user base
- Security measures should protect user data and system access
- The user interface should be accessible and user-friendly"""

    def _generate_contextual_acceptance_criteria(self, title: str, detected_app: str, detected_role: str) -> str:
        """Generate contextual acceptance criteria based on title analysis."""
        title_lower = title.lower()
        
        if "kanban" in title_lower and "taiga" in title_lower:
            return """- [ ] Kanban board loads completely within 3 seconds
- [ ] All project columns and swimlanes are displayed correctly
- [ ] User stories and tasks appear in their appropriate columns
- [ ] Drag and drop functionality works between columns
- [ ] Card details can be accessed by clicking on items
- [ ] Real-time updates reflect changes from other team members
- [ ] Board works correctly on desktop and mobile devices
- [ ] No JavaScript errors appear in browser console
- [ ] Scrolling is smooth and responsive throughout the board"""
        
        elif "login" in title_lower or "authentication" in title_lower:
            return """- [ ] Users can successfully log in with valid credentials
- [ ] Login process completes within 3 seconds
- [ ] Clear error messages appear for invalid credentials
- [ ] Successful login redirects to appropriate dashboard
- [ ] Session persists for expected duration without issues
- [ ] Password reset functionality works end-to-end
- [ ] Two-factor authentication works if enabled
- [ ] Login works across different browsers and devices
- [ ] Security measures prevent unauthorized access"""
        
        elif "scroll" in title_lower or "scrolling" in title_lower:
            return """- [ ] Mouse wheel scrolling works smoothly and responsively
- [ ] Touchpad gestures work with natural scrolling behavior
- [ ] Keyboard navigation (arrows, space, page up/down) functions properly
- [ ] Scrollbars appear when content exceeds viewport dimensions
- [ ] Momentum scrolling works on touch devices
- [ ] Scroll performance maintains 60fps during movement
- [ ] Content snap points work as designed
- [ ] Scrolling works consistently across different browsers
- [ ] No layout shifts occur during scrolling"""
        
        elif "button" in title_lower or "click" in title_lower:
            return """- [ ] Buttons respond immediately to user clicks
- [ ] Visual feedback appears on hover and active states
- [ ] Intended actions trigger correctly without errors
- [ ] Buttons are accessible via keyboard navigation
- [ ] Loading states show for async operations
- [ ] Disabled buttons are clearly visually indicated
- [ ] Touch targets meet minimum 44x44px requirement
- [ ] Buttons work consistently across different browsers
- [ ] No JavaScript errors occur on button interactions"""
        
        elif "performance" in title_lower or "slow" in title_lower or "lag" in title_lower:
            return """- [ ] Page loads complete within 3 seconds on standard connection
- [ ] User interactions respond within 100ms
- [ ] Animations maintain 60fps performance consistently
- [ ] Memory usage remains stable during extended use
- [ ] Network requests are optimized and properly cached
- [ ] Database queries execute efficiently with proper indexing
- [ ] System handles concurrent users without performance degradation
- [ ] Core Web Vitals meet recommended thresholds
- [ ] No memory leaks detected during testing"""
        
        else:
            return f"""- [ ] The reported issue is clearly identified and understood
- [ ] The problem can be reproduced consistently
- [ ] Root cause analysis identifies the underlying issue
- [ ] Solution addresses the problem without introducing new issues
- [ ] Fix is tested thoroughly across different scenarios
- [ ] Performance impact is acceptable and within standards
- [ ] Documentation is updated to reflect changes made
- [ ] Team members are trained on any new processes or features
- [ ] Monitoring is in place to prevent future occurrences"""
