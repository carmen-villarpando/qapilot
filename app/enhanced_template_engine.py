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
        
        # Generate professional QA-style description for bugs
        if self._is_bug_issue(title):
            description = self._generate_qa_lead_description(title, detected_app, detected_role, mentioned_features, app_enhanced_description)
        elif self._is_story_issue(title):
            description = self._generate_po_pm_description(title, detected_app, detected_role, mentioned_features, app_enhanced_description)
        else:
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

    def _is_bug_issue(self, title: str) -> bool:
        """Detect if the issue is a bug based on title analysis."""
        title_lower = title.lower()
        bug_keywords = [
            "bug", "error", "issue", "problem", "broken", "crash", "fail", "not working",
            "doesn't work", "incorrect", "wrong", "missing", "corrupt", "invalid",
            "exception", "timeout", "freeze", "hang", "stuck", "blocked", "blocked",
            "not loading", "loading", "crash", "freeze", "hang", "stuck", "blocked"
        ]
        return any(keyword in title_lower for keyword in bug_keywords)

    def _is_story_issue(self, title: str) -> bool:
        """Detect if the issue is a user story/feature based on title analysis."""
        title_lower = title.lower()
        # First check if it's a bug - bugs take precedence
        if self._is_bug_issue(title):
            return False
        
        story_keywords = [
            "story", "feature", "requirement", "enhancement", "improvement", "add", "create",
            "implement", "build", "develop", "design", "new", "support", "integrate",
            "user story", "epic", "task", "functionality", "capability", "ability"
        ]
        return any(keyword in title_lower for keyword in story_keywords)

    def _generate_qa_lead_description(self, title: str, detected_app: str, detected_role: str, mentioned_features: List[str], app_enhanced_description: str) -> str:
        """Generate professional QA Lead style description for bugs."""
        
        # Generate improved title
        improved_title = self._generate_improved_title(title)
        
        # Generate structured description
        structured_description = self._generate_structured_description(title, detected_app, detected_role)
        
        # Generate summary
        summary = self._generate_summary(title, detected_app)
        
        # Generate expected behavior
        expected_behavior = self._generate_qa_expected_behavior(title, detected_app, detected_role)
        
        # Generate reproduction steps
        reproduction_steps = self._generate_qa_reproduction_steps(title, detected_app, detected_role)
        
        # Generate open questions
        open_questions = self._generate_open_questions(title, detected_app, detected_role)
        
        return f"""## 📝 {improved_title}

### 📋 Description

{self._generate_bug_description(title, detected_app, detected_role)}

### ✅ Expected Behavior

{self._generate_bug_expected_behavior(title, detected_app, detected_role)}

### 🔴 Actual Behavior

{self._generate_bug_actual_behavior(title, detected_app, detected_role)}

### 🔧 Steps to Reproduce

{self._generate_bug_reproduction_steps(title, detected_app, detected_role)}

### 🌍 Environment

{self._generate_bug_environment(title, detected_app, detected_role)}

### 📊 Impact & Priority

**Priority:** {self._assess_bug_priority(title)}
**Impact:** {self._assess_bug_impact(title)}

---

*This issue has been analyzed by QAPilot's QA Lead perspective.*"""

    def _generate_improved_title(self, title: str) -> str:
        """Generate an improved, more descriptive title with typo correction."""
        # First correct typos and improve the title
        corrected_title = self._correct_title_typos(title)
        title_lower = corrected_title.lower()
        
        if "kanban" in title_lower and "not loading" in title_lower:
            return "Bug: Kanban board fails to load in Taiga project"
        elif "login" in title_lower and ("fail" in title_lower or "not working" in title_lower):
            return "Bug: Authentication failure prevents user login"
        elif "scroll" in title_lower and ("not working" in title_lower or "broken" in title_lower):
            return "Bug: Scrolling functionality is not working in interface"
        elif "button" in title_lower and ("not working" in title_lower or "click" in title_lower):
            return "Bug: Interactive buttons are not responding to user clicks"
        elif "performance" in title_lower or "slow" in title_lower:
            return "Bug: Performance degradation affecting system responsiveness"
        else:
            # Generic bug title improvement with typo correction
            if "bug" not in title_lower:
                return f"Bug: {corrected_title}"
            return corrected_title.title()

    def _correct_title_typos(self, title: str) -> str:
        """Correct common typos and improve title formatting."""
        import re
        
        # Common typo corrections
        typo_corrections = {
            # Project/app name typos
            'taiga projet': 'Taiga project',
            'taiga proyect': 'Taiga project',
            'taiga projetc': 'Taiga project',
            'taiga projet': 'Taiga project',
            'taiga proj': 'Taiga project',
            'taiga': 'Taiga',
            
            # Common word typos
            'kanban bord': 'Kanban board',
            'kanban bord': 'Kanban board',
            'kanban bord': 'Kanban board',
            'kanban bard': 'Kanban board',
            'kanban': 'Kanban',
            
            'loding': 'loading',
            'loadin': 'loading',
            'laoding': 'loading',
            'loaing': 'loading',
            
            'faild': 'failed',
            'faild': 'failed',
            'faile': 'failed',
            'fail': 'failed',
            
            'brocken': 'broken',
            'brocken': 'broken',
            'broke': 'broken',
            
            'not woking': 'not working',
            'not wroking': 'not working',
            'not workin': 'not working',
            'not wokring': 'not working',
            
            'perfomance': 'performance',
            'perfromance': 'performance',
            'preformance': 'performance',
            'performace': 'performance',
            
            'authentiction': 'authentication',
            'authenticaion': 'authentication',
            'authentacation': 'authentication',
            
            'scroling': 'scrolling',
            'scroling': 'scrolling',
            'scroling': 'scrolling',
            'scrooling': 'scrolling',
            
            'buton': 'button',
            'buton': 'button',
            'buton': 'button',
            
            'responce': 'response',
            'respose': 'response',
            'responce': 'response',
            
            'erorr': 'error',
            'eror': 'error',
            'erorr': 'error',
            
            'issu': 'issue',
            'isue': 'issue',
            'issu': 'issue',
            
            'problm': 'problem',
            'problm': 'problem',
            'proble': 'problem',
            'problm': 'problem',
            
            'functonality': 'functionality',
            'functinality': 'functionality',
            'functonality': 'functionality',
            'funcionality': 'functionality',
            
            'acces': 'access',
            'acess': 'access',
            'acces': 'access',
            
            'user': 'user',
            'usr': 'user',
            'useer': 'user',
            
            'systm': 'system',
            'systm': 'system',
            'systme': 'system',
            'systm': 'system',
            
            'interfac': 'interface',
            'interfce': 'interface',
            'interfac': 'interface',
            
            'naviagation': 'navigation',
            'naviagtion': 'navigation',
            'naviagation': 'navigation',
            
            'behavoir': 'behavior',
            'behavoir': 'behavior',
            'behavour': 'behavior',
            
            'expcted': 'expected',
            'expeted': 'expected',
            'expcted': 'expected',
            
            'reproduc': 'reproduce',
            'reproduc': 'reproduce',
            'reproduc': 'reproduce',
            
            'environmnt': 'environment',
            'environmnt': 'environment',
            'environmet': 'environment',
            
            'prority': 'priority',
            'prority': 'priority',
            'priorty': 'priority',
            
            'impact': 'impact',
            'impct': 'impact',
            'imact': 'impact',
            
            'step': 'step',
            'stp': 'step',
            'ste': 'step',
            
            'descripion': 'description',
            'descripion': 'description',
            'descripton': 'description',
            
            'actual': 'actual',
            'actul': 'actual',
            'actal': 'actual',
            
            'behvior': 'behavior',
            'behvior': 'behavior',
            'behavour': 'behavior',
        }
        
        # Apply typo corrections
        corrected = title
        for typo, correction in typo_corrections.items():
            corrected = re.sub(rf'\b{re.escape(typo)}\b', correction, corrected, flags=re.IGNORECASE)
        
        # Fix spacing and capitalization
        corrected = self._fix_title_formatting(corrected)
        
        return corrected

    def _fix_title_formatting(self, title: str) -> str:
        """Fix spacing, capitalization, and general formatting."""
        import re
        
        # Remove extra spaces
        title = re.sub(r'\s+', ' ', title.strip())
        
        # Capitalize first letter of each word (but keep technical terms consistent)
        words = title.split()
        formatted_words = []
        
        for word in words:
            word_lower = word.lower()
            
            # Keep technical terms in consistent case
            if word_lower in ['taiga', 'kanban', 'github', 'api', 'ui', 'ux']:
                formatted_words.append(word.title())
            elif word_lower in ['qa', 'pm', 'po']:
                formatted_words.append(word.upper())
            else:
                # Capitalize first letter
                formatted_words.append(word.capitalize())
        
        return ' '.join(formatted_words)

    def _generate_structured_description(self, title: str, detected_app: str, detected_role: str) -> str:
        """Generate structured description with assumptions clearly stated."""
        title_lower = title.lower()
        
        if "kanban" in title_lower and "taiga" in title_lower:
            return """**Assumption:** This issue affects the main kanban board view in a Taiga project management interface.

**Observed Behavior:** When users attempt to access the kanban board, the board either fails to load completely or displays an indefinite loading state.

**Impact Assessment:** This issue blocks team members from:
- Viewing current work in progress
- Managing task assignments across swimlanes
- Tracking sprint progress
- Conducting daily standup activities

**Environment Context:** (Suggested)
- Browser: [To be confirmed]
- Taiga Version: [To be confirmed]
- Project Type: [To be confirmed - Agile/Scrum/Kanban]
- User Role: [To be confirmed - Team Member/Scrum Master/Developer]"""
        
        elif "login" in title_lower or "authentication" in title_lower:
            return """**Assumption:** This issue affects the primary authentication flow of the application.

**Observed Behavior:** Users are unable to successfully authenticate and access the system.

**Impact Assessment:** This issue completely blocks:
- User access to all application features
- Team productivity and workflow continuity
- Customer-facing operations
- Internal system administration

**Environment Context:** (Suggested)
- Browser: [To be confirmed]
- Authentication Method: [To be confirmed - Email/Password, SSO, 2FA]
- User Account Type: [To be confirmed]
- Network Environment: [To be confirmed]"""
        
        else:
            return f"""**Assumption:** This issue affects core functionality in {detected_app}.

**Observed Behavior:** The system is not performing as expected based on the reported issue.

**Impact Assessment:** This issue may affect:
- User experience and productivity
- System reliability and stability
- Business operations continuity
- Team workflow efficiency

**Environment Context:** (Suggested)
- Browser/Platform: [To be confirmed]
- Application Version: [To be confirmed]
- User Context: [To be confirmed]
- Network Conditions: [To be confirmed]"""

    def _generate_summary(self, title: str, detected_app: str) -> str:
        """Generate concise summary of the issue."""
        title_lower = title.lower()
        
        if "kanban" in title_lower and "taiga" in title_lower:
            return "Team members cannot access the kanban board in Taiga, blocking workflow management and sprint tracking activities."
        elif "login" in title_lower or "authentication" in title_lower:
            return "Users are unable to authenticate and access the system, completely blocking application usage."
        elif "scroll" in title_lower or "scrolling" in title_lower:
            return "Scrolling functionality is broken, preventing users from accessing content beyond the visible viewport."
        elif "button" in title_lower or "click" in title_lower:
            return "Interactive buttons are not responding to user clicks, preventing completion of critical workflows."
        elif "performance" in title_lower or "slow" in title_lower:
            return "System performance is degraded, causing slow response times and poor user experience."
        else:
            return f"A critical issue in {detected_app} is preventing normal system operation and needs immediate investigation."

    def _generate_qa_expected_behavior(self, title: str, detected_app: str, detected_role: str) -> str:
        """Generate expected behavior from QA perspective."""
        title_lower = title.lower()
        
        if "kanban" in title_lower and "taiga" in title_lower:
            return """**Expected System Behavior:**
- Kanban board loads completely within 3 seconds
- All project columns and swimlanes display correctly
- User stories and tasks appear in appropriate columns
- Drag-and-drop functionality works between columns
- Real-time updates reflect team member changes
- Board works on desktop and mobile devices
- No JavaScript errors in browser console

**Performance Criteria:**
- Load time: <3 seconds
- Interaction response: <100ms
- Memory usage: Stable during extended use
- Network requests: Optimized and cached"""
        
        elif "login" in title_lower or "authentication" in title_lower:
            return """**Expected System Behavior:**
- Login page loads and renders correctly
- Valid credentials authenticate successfully
- Invalid credentials show clear error messages
- Successful login redirects to appropriate dashboard
- Session persists without frequent re-login
- Two-factor authentication works when enabled
- Password reset functionality is accessible

**Security Criteria:**
- Authentication completes within 2-3 seconds
- Passwords are handled securely (not logged or exposed)
- Session tokens are properly managed
- Rate limiting prevents brute force attacks
- HTTPS is enforced for all auth requests"""
        
        else:
            return f"""**Expected System Behavior:**
- The {detected_app} system functions as designed and documented
- User interactions are responsive and intuitive
- Error handling is graceful and informative
- Data integrity and consistency are maintained
- Performance meets acceptable standards
- Security measures protect user data

**Quality Criteria:**
- Response time: <2 seconds for standard operations
- Error rate: <1% for normal usage patterns
- Uptime: >99.9% availability
- User satisfaction: High usability score"""

    def _generate_qa_reproduction_steps(self, title: str, detected_app: str, detected_role: str) -> str:
        """Generate detailed reproduction steps for QA testing."""
        title_lower = title.lower()
        
        if "kanban" in title_lower and "taiga" in title_lower:
            return """**Pre-conditions:**
- User has valid Taiga account
- User is member of at least one project
- Project has kanban board configured

**Test Steps:**
1. Open web browser and navigate to Taiga instance
2. Login with valid credentials
3. Select affected project from project list
4. Click on "Kanban" tab or board view
5. Observe board loading behavior
6. Wait up to 30 seconds for full load
7. Check browser developer console for errors
8. Test with different browsers (Chrome, Firefox, Safari)
9. Test on mobile device if possible
10. Try refreshing the page to reproduce consistently

**Expected Results:** Board loads completely with all columns and tasks visible

**Actual Results:** [To be documented during testing]"""
        
        elif "login" in title_lower or "authentication" in title_lower:
            return """**Pre-conditions:**
- User has valid account credentials
- Authentication service is running
- Network connectivity is available

**Test Steps:**
1. Open web browser and navigate to application login page
2. Verify login page loads correctly
3. Enter valid username/email in username field
4. Enter valid password in password field
5. Click "Login" button or press Enter
6. Observe authentication process and any redirects
7. Note any error messages or unusual behavior
8. Test with invalid credentials to verify error handling
9. Test with different browsers if possible
10. Check network requests in browser dev tools

**Expected Results:** Successful authentication and redirect to dashboard

**Actual Results:** [To be documented during testing]"""
        
        else:
            return f"""**Pre-conditions:**
- User has appropriate permissions for {detected_app}
- System is running and accessible
- Required test data is available

**Test Steps:**
1. Navigate to the affected area of {detected_app}
2. Identify the specific functionality mentioned in the issue
3. Attempt to reproduce the reported problem
4. Document the exact sequence of actions
5. Note any error messages or unusual behavior
6. Test with different inputs or parameters
7. Verify the issue occurs consistently
8. Check system logs for relevant information
9. Test on different browsers/devices if applicable
10. Record performance metrics if relevant

**Expected Results:** Function works as designed without errors

**Actual Results:** [To be documented during testing]"""

    def _generate_open_questions(self, title: str, detected_app: str, detected_role: str) -> str:
        """Generate open questions for investigation."""
        title_lower = title.lower()
        
        if "kanban" in title_lower and "taiga" in title_lower:
            return """**Environment Questions:**
- What browser and version are being used?
- What Taiga version is installed?
- Is this affecting all projects or specific ones?
- Does the issue occur for all user roles?

**Technical Questions:**
- Are there JavaScript errors in browser console?
- What do the network requests show (status codes, timing)?
- Is the backend API responding correctly?
- Are there any recent changes to the kanban board configuration?

**Impact Questions:**
- How many team members are affected?
- What is the business impact of this issue?
- Are there workarounds available?
- Has this issue occurred before?"""
        
        elif "login" in title_lower or "authentication" in title_lower:
            return """**Environment Questions:**
- What browser and version are being used?
- Is this affecting all users or specific accounts?
- Are there any recent changes to authentication system?
- Is two-factor authentication involved?

**Technical Questions:**
- What do the authentication logs show?
- Are there network connectivity issues?
- Is the authentication service running correctly?
- Are credentials being transmitted securely?

**Security Questions:**
- Could this be related to a security breach?
- Are there failed login attempts in logs?
- Is rate limiting working correctly?
- Are session tokens being generated properly?"""
        
        else:
            return f"""**Environment Questions:**
- What browser/platform is being used?
- Is this affecting all users or specific ones?
- Are there any recent system changes or deployments?
- What is the user's role and permissions?

**Technical Questions:**
- What do the system logs show?
- Are there any error messages or stack traces?
- Is the database responding correctly?
- Are network requests completing successfully?

**Impact Questions:**
- How many users are affected?
- What is the business impact?
- Are there workarounds available?
- Has this issue occurred before?"""

    def _assess_bug_priority(self, title: str) -> str:
        """Assess bug priority based on impact."""
        title_lower = title.lower()
        
        if "login" in title_lower or "authentication" in title_lower:
            return "HIGH - Blocks all user access"
        elif "critical" in title_lower or "crash" in title_lower:
            return "HIGH - System failure or data loss risk"
        elif "performance" in title_lower or "slow" in title_lower:
            return "MEDIUM - Affects user experience but system functional"
        elif "button" in title_lower or "scroll" in title_lower:
            return "MEDIUM - Partial functionality affected"
        else:
            return "MEDIUM - Needs investigation for full impact assessment"

    def _assess_test_coverage(self, title: str) -> str:
        """Assess test coverage impact."""
        title_lower = title.lower()
        
        if "login" in title_lower or "authentication" in title_lower:
            return "HIGH - Affects authentication test suites"
        elif "kanban" in title_lower or "board" in title_lower:
            return "MEDIUM - May affect workflow management tests"
        elif "performance" in title_lower:
            return "HIGH - Requires performance regression testing"
        else:
            return "MEDIUM - Requires functional test updates"

    def _assess_regression_risk(self, title: str) -> str:
        """Assess regression risk."""
        title_lower = title.lower()
        
        if "authentication" in title_lower or "login" in title_lower:
            return "HIGH - Core system functionality"
        elif "database" in title_lower or "data" in title_lower:
            return "HIGH - Potential data integrity impact"
        elif "performance" in title_lower:
            return "MEDIUM - May affect system performance"
        else:
            return "LOW - Isolated functionality issue"

    def _generate_bug_description(self, title: str, detected_app: str, detected_role: str) -> str:
        """Generate bug description focusing on what's currently happening."""
        title_lower = title.lower()
        
        if "kanban" in title_lower and "not loading" in title_lower:
            return """Team members are unable to access the kanban board in their Taiga project. When attempting to navigate to the kanban view, the board either fails to load completely or displays an indefinite loading state, preventing users from viewing their tasks and managing workflow."""
        
        elif "login" in title_lower and ("fail" in title_lower or "not working" in title_lower):
            return """Users are experiencing authentication failures when attempting to log in to the system. The login process is not completing successfully, preventing users from accessing their accounts and using the application."""
        
        elif "scroll" in title_lower and ("not working" in title_lower or "broken" in title_lower):
            return """Users are unable to scroll through content in the interface. The scrolling functionality is not responding to mouse wheel, trackpad, or keyboard input, preventing users from accessing content that extends beyond the visible viewport."""
        
        elif "button" in title_lower and ("not working" in title_lower or "click" in title_lower):
            return """Interactive buttons are not responding to user clicks. When users attempt to click buttons in the interface, nothing happens or the expected actions are not triggered, preventing users from completing their workflows."""
        
        elif "performance" in title_lower or "slow" in title_lower:
            return """The application is experiencing significant performance degradation. Users are experiencing slow response times, delayed reactions to their actions, and overall poor system performance that impacts productivity."""
        
        else:
            return f"""The system is experiencing a malfunction that affects normal operation in {detected_app}. Users are encountering issues that prevent them from using the application as intended, impacting their ability to complete their work efficiently."""

    def _generate_bug_expected_behavior(self, title: str, detected_app: str, detected_role: str) -> str:
        """Generate expected behavior for the bug."""
        title_lower = title.lower()
        
        if "kanban" in title_lower and "not loading" in title_lower:
            return """The kanban board should load completely within 3 seconds, displaying all project columns and tasks. Users should be able to view, interact with, and manage their tasks through the kanban interface without any loading issues."""
        
        elif "login" in title_lower and ("fail" in title_lower or "not working" in title_lower):
            return """Users should be able to log in successfully with valid credentials within 2-3 seconds. The authentication process should complete smoothly and redirect users to their dashboard or intended destination."""
        
        elif "scroll" in title_lower and ("not working" in title_lower or "broken" in title_lower):
            return """Scrolling should work smoothly and responsively using mouse wheel, trackpad, or keyboard navigation. Users should be able to access all content that extends beyond the visible viewport without any issues."""
        
        elif "button" in title_lower and ("not working" in title_lower or "click" in title_lower):
            return """Buttons should respond immediately to user clicks with appropriate visual feedback. The intended actions should trigger correctly, allowing users to complete their workflows without interruption."""
        
        elif "performance" in title_lower or "slow" in title_lower:
            return """The application should respond quickly to user actions (<100ms), load pages efficiently (<3 seconds), and maintain smooth performance during normal usage without delays or lag."""
        
        else:
            return f"""The {detected_app} system should function normally without errors, allowing users to complete their tasks efficiently and without encountering any technical issues or malfunctions."""

    def _generate_bug_actual_behavior(self, title: str, detected_app: str, detected_role: str) -> str:
        """Generate actual behavior description in direct terms."""
        title_lower = title.lower()
        
        if "kanban" in title_lower and "not loading" in title_lower:
            return """The kanban board does not load when accessed. Users see either a blank screen, loading spinner that never resolves, or error messages preventing them from viewing their tasks."""
        
        elif "login" in title_lower and ("fail" in title_lower or "not working" in title_lower):
            return """The login process fails to authenticate users. Either the login button doesn't work, credentials are not accepted, or users receive error messages preventing access."""
        
        elif "scroll" in title_lower and ("not working" in title_lower or "broken" in title_lower):
            return """Scrolling is completely non-functional. Mouse wheel, trackpad gestures, and keyboard arrow keys do not move the content, leaving users unable to access information beyond the initial viewport."""
        
        elif "button" in title_lower and ("not working" in title_lower or "click" in title_lower):
            return """Buttons are unresponsive to clicks. Users can click on buttons but nothing happens - no visual feedback, no action execution, and no error messages."""
        
        elif "performance" in title_lower or "slow" in title_lower:
            return """The application is slow and unresponsive. Actions take several seconds to complete, pages load slowly, and users experience lag during normal interactions."""
        
        else:
            return f"""The {detected_app} system is malfunctioning. Users are experiencing errors, crashes, or incorrect behavior that prevents them from using the application properly."""

    def _generate_bug_reproduction_steps(self, title: str, detected_app: str, detected_role: str) -> str:
        """Generate clear reproduction steps."""
        title_lower = title.lower()
        
        if "kanban" in title_lower and "not loading" in title_lower:
            return """1. Log in to Taiga with valid credentials
2. Navigate to the affected project
3. Click on the "Kanban" tab or board view
4. Observe that the board fails to load properly
5. Wait for 30 seconds to confirm it's not a delay
6. Check browser console for any JavaScript errors"""
        
        elif "login" in title_lower and ("fail" in title_lower or "not working" in title_lower):
            return """1. Open the application login page
2. Enter valid username and password
3. Click the login button or press Enter
4. Observe that authentication fails
5. Check for any error messages displayed
6. Verify network connectivity"""
        
        elif "scroll" in title_lower and ("not working" in title_lower or "broken" in title_lower):
            return """1. Navigate to a page with scrollable content
2. Attempt to scroll using mouse wheel
3. Try scrolling with trackpad gestures
4. Test keyboard arrow keys and spacebar
5. Observe that none of the scroll methods work"""
        
        elif "button" in title_lower and ("not working" in title_lower or "click" in title_lower):
            return """1. Navigate to the page with the affected button
2. Click on the button with mouse
3. Observe that nothing happens
4. Try keyboard navigation (Tab + Enter)
5. Check if button appears disabled or has any visual state"""
        
        elif "performance" in title_lower or "slow" in title_lower:
            return """1. Navigate to any page in the application
2. Perform any action (click, type, navigate)
3. Measure response time with a stopwatch
4. Observe significant delays (>2 seconds)
5. Test multiple different actions to confirm widespread slowness"""
        
        else:
            return f"""1. Navigate to the affected area of {detected_app}
2. Attempt to perform the normal workflow
3. Observe the malfunction or error
4. Document the specific steps that trigger the issue
5. Try to reproduce the issue consistently"""

    def _generate_bug_environment(self, title: str, detected_app: str, detected_role: str) -> str:
        """Generate environment information."""
        return """**Browser:** [To be confirmed - Chrome, Firefox, Safari, Edge]
**Operating System:** [To be confirmed - Windows, macOS, Linux]
**Application Version:** [To be confirmed]
**User Role:** [To be confirmed]
**Network:** [To be confirmed - Corporate, Home, Mobile]
**Device:** [To be confirmed - Desktop, Mobile, Tablet]"""

    def _assess_bug_impact(self, title: str) -> str:
        """Assess bug impact."""
        title_lower = title.lower()
        
        if "login" in title_lower or "authentication" in title_lower:
            return "HIGH - Complete system access blocked"
        elif "kanban" in title_lower or "board" in title_lower:
            return "HIGH - Core workflow functionality blocked"
        elif "performance" in title_lower or "slow" in title_lower:
            return "MEDIUM - Significant user experience degradation"
        elif "scroll" in title_lower or "navigation" in title_lower:
            return "MEDIUM - Content accessibility affected"
        elif "button" in title_lower or "click" in title_lower:
            return "MEDIUM - Workflow completion blocked"
        else:
            return "MEDIUM - Partial functionality affected"

    def _generate_po_pm_description(self, title: str, detected_app: str, detected_role: str, mentioned_features: List[str], app_enhanced_description: str) -> str:
        """Generate Product Owner/Project Manager style description for user stories and features."""
        
        # Generate improved title
        improved_title = self._generate_story_title(title)
        
        # Generate user story format
        user_story = self._generate_user_story(title, detected_app, detected_role)
        
        # Generate business context
        business_context = self._generate_business_context(title, detected_app, detected_role)
        
        # Generate acceptance criteria
        acceptance_criteria = self._generate_story_acceptance_criteria(title, detected_app, detected_role)
        
        # Generate technical requirements
        technical_requirements = self._generate_technical_requirements(title, detected_app, detected_role)
        
        # Generate success metrics
        success_metrics = self._generate_success_metrics(title, detected_app, detected_role)
        
        # Generate dependencies and risks
        dependencies_risks = self._generate_dependencies_risks(title, detected_app, detected_role)
        
        return f"""## 📋 {improved_title}

### 🎯 User Story

{user_story}

### 💼 Business Context

{business_context}

{app_enhanced_description}

### ✅ Acceptance Criteria

{acceptance_criteria}

### 🔧 Technical Requirements

{technical_requirements}

### 📊 Success Metrics

{success_metrics}

### ⚠️ Dependencies & Risks

{dependencies_risks}

### 🏷️ Suggested Labels

feature, user-story, {detected_app.lower()}, product-backlog, ready-for-development

### 📈 Product Assessment

**Business Value:** {self._assess_business_value(title)}
**Development Effort:** {self._assess_development_effort(title)}
**Priority:** {self._assess_story_priority(title)}

---

*This requirement has been analyzed by QAPilot's Product Owner perspective. All assumptions should be validated with stakeholders before development begins.*"""

    def _generate_story_title(self, title: str) -> str:
        """Generate improved title for user stories with typo correction."""
        # First correct typos and improve the title
        corrected_title = self._correct_title_typos(title)
        title_lower = corrected_title.lower()
        
        if "kanban" in title_lower and ("add" in title_lower or "create" in title_lower or "implement" in title_lower):
            return "Feature: Add kanban board functionality to Taiga project"
        elif "login" in title_lower and ("improve" in title_lower or "enhance" in title_lower or "add" in title_lower):
            return "Feature: Enhanced login experience with improved authentication"
        elif "scroll" in title_lower and ("improve" in title_lower or "enhance" in title_lower):
            return "Feature: Enhanced scrolling experience for better user navigation"
        elif "button" in title_lower and ("add" in title_lower or "create" in title_lower or "implement" in title_lower):
            return "Feature: Add interactive button with enhanced user feedback"
        elif "performance" in title_lower and ("improve" in title_lower or "optimize" in title_lower):
            return "Feature: Performance optimization for enhanced user experience"
        else:
            # Generic feature title improvement with typo correction
            if "feature" not in title_lower and "story" not in title_lower:
                return f"Feature: {corrected_title}"
            return corrected_title.title()

    def _generate_user_story(self, title: str, detected_app: str, detected_role: str) -> str:
        """Generate user story in standard format."""
        title_lower = title.lower()
        
        if "kanban" in title_lower and "taiga" in title_lower:
            return """**As a** team member working on an agile project,
**I want to** access and interact with a kanban board in Taiga,
**So that** I can visualize workflow, track progress, and manage tasks effectively across different swimlanes."""
        
        elif "login" in title_lower or "authentication" in title_lower:
            return """**As a** user of the system,
**I want to** log in securely and quickly,
**So that** I can access my work and contribute to the team's goals without authentication barriers."""
        
        elif "scroll" in title_lower or "scrolling" in title_lower:
            return """**As a** user navigating through content,
**I want to** scroll smoothly and intuitively through all available content,
**So that** I can access information efficiently and have a pleasant user experience."""
        
        elif "button" in title_lower or "click" in title_lower:
            return """**As a** user interacting with the interface,
**I want to** click buttons that respond immediately and clearly,
**So that** I can complete my tasks efficiently and understand the system's responses."""
        
        elif "performance" in title_lower or "slow" in title_lower:
            return """**As a** user of the application,
**I want to** experience fast and responsive performance,
**So that** I can work efficiently without waiting or frustration."""
        
        else:
            return f"""**As a** user of {detected_app},
**I want to** {self._extract_user_action(title)},
**So that** I can achieve my goals more effectively and efficiently."""

    def _extract_user_action(self, title: str) -> str:
        """Extract user action from title."""
        title_lower = title.lower()
        
        if "add" in title_lower:
            return "add new functionality"
        elif "improve" in title_lower or "enhance" in title_lower:
            return "improve the existing experience"
        elif "create" in title_lower:
            return "create new content or features"
        elif "implement" in title_lower:
            return "implement new capabilities"
        elif "support" in title_lower:
            return "get support for new functionality"
        else:
            return "access improved features"

    def _generate_business_context(self, title: str, detected_app: str, detected_role: str) -> str:
        """Generate business context and rationale."""
        title_lower = title.lower()
        
        if "kanban" in title_lower and "taiga" in title_lower:
            return """**Business Problem:** Current project management lacks visual workflow tracking, making it difficult for teams to monitor progress and manage tasks effectively.

**Business Value:** Implementing kanban board functionality will:
- Improve team visibility into work progress
- Enable better task management and assignment
- Support agile methodologies and sprint planning
- Increase team productivity and collaboration
- Provide data-driven insights for process improvement

**Stakeholders:** Development team, Scrum Master, Product Owner, Project Managers, Team Members"""
        
        elif "login" in title_lower or "authentication" in title_lower:
            return """**Business Problem:** Current authentication process may be cumbersome or insecure, creating barriers to user adoption and potential security risks.

**Business Value:** Enhanced login experience will:
- Improve user satisfaction and adoption rates
- Reduce support tickets related to login issues
- Strengthen security posture and compliance
- Enable seamless access to critical business functions
- Support mobile and remote work scenarios

**Stakeholders:** End users, Security team, IT administrators, Customer support, Compliance officers"""
        
        elif "scroll" in title_lower or "scrolling" in title_lower:
            return """**Business Problem:** Poor scrolling experience frustrates users and may prevent them from accessing important content, reducing engagement and completion rates.

**Business Value:** Enhanced scrolling will:
- Improve user experience and satisfaction
- Increase content accessibility and consumption
- Support mobile and touch device usage
- Reduce user frustration and support requests
- Enable better content presentation and discovery

**Stakeholders:** End users, UX team, Mobile users, Content creators, Product managers"""
        
        else:
            return f"""**Business Problem:** Current limitations in {detected_app} prevent users from achieving their goals efficiently, impacting productivity and satisfaction.

**Business Value:** This enhancement will:
- Improve user experience and satisfaction
- Increase productivity and efficiency
- Support business objectives and KPIs
- Enable better user adoption and retention
- Provide competitive advantages in the market

**Stakeholders:** End users, Product team, Business stakeholders, Support team, Management"""

    def _generate_story_acceptance_criteria(self, title: str, detected_app: str, detected_role: str) -> str:
        """Generate detailed acceptance criteria for user stories."""
        title_lower = title.lower()
        
        if "kanban" in title_lower and "taiga" in title_lower:
            return """**Given** I am logged into Taiga as a team member
**When** I navigate to a project with kanban functionality
**Then** I should see a kanban board with all project columns

**Given** I am viewing the kanban board
**When** I drag a task card between columns
**Then** the card should move smoothly and update its status in real-time

**Given** I am using the kanban board
**When** I filter or search for specific tasks
**Then** only matching tasks should be displayed

**Given** I am on a mobile device
**When** I access the kanban board
**Then** the board should be responsive and touch-friendly

**Given** I am a team member
**When** another team member updates a task
**Then** I should see the change reflected immediately"""
        
        elif "login" in title_lower or "authentication" in title_lower:
            return """**Given** I am a registered user
**When** I enter valid credentials on the login page
**Then** I should be authenticated and redirected to my dashboard

**Given** I have entered invalid credentials
**When** I attempt to log in
**Then** I should see clear error messages without revealing sensitive information

**Given** I have successfully logged in
**When** I close and reopen the browser
**Then** I should remain logged in for the appropriate session duration

**Given** I am using a mobile device
**When** I attempt to log in
**Then** the login interface should be optimized for touch and mobile screens

**Given** Two-factor authentication is enabled
**When** I log in with valid credentials
**Then** I should be prompted for the second factor before gaining access"""
        
        elif "scroll" in title_lower or "scrolling" in title_lower:
            return """**Given** I am viewing content that exceeds the viewport
**When** I use the mouse wheel to scroll
**Then** the content should scroll smoothly at an appropriate speed

**Given** I am using a touch device
**When** I swipe to scroll
**Then** the content should respond naturally with momentum scrolling

**Given** I am navigating with keyboard
**When** I use arrow keys or spacebar
**Then** the content should scroll in the expected direction

**Given** Content is loading dynamically
**When** I scroll to the bottom of the page
**Then** additional content should load without interrupting the scroll position"""
        
        else:
            return f"""**Given** I am a user of {detected_app}
**When** I interact with the enhanced functionality
**Then** I should experience improved performance and usability

**Given** The feature is implemented
**When** I use it in my daily workflow
**Then** it should integrate seamlessly with existing functionality

**Given** I am on different devices
**When** I access the feature
**Then** it should work consistently across all platforms

**Given** I encounter errors or issues
**When** I use the feature
**Then** I should receive clear, helpful error messages"""

    def _generate_technical_requirements(self, title: str, detected_app: str, detected_role: str) -> str:
        """Generate technical requirements for development team."""
        title_lower = title.lower()
        
        if "kanban" in title_lower and "taiga" in title_lower:
            return """**Frontend Requirements:**
- Responsive kanban board component using modern framework
- Drag-and-drop functionality with visual feedback
- Real-time updates using WebSockets or polling
- Mobile-responsive design with touch support
- Smooth animations and transitions

**Backend Requirements:**
- RESTful API endpoints for kanban operations
- Real-time event broadcasting for updates
- Database schema for kanban data structure
- Authentication and authorization checks
- Performance optimization for large datasets

**Integration Requirements:**
- Integration with existing Taiga project structure
- Compatibility with current user management system
- API versioning for backward compatibility
- Support for existing project templates and workflows"""
        
        elif "login" in title_lower or "authentication" in title_lower:
            return """**Frontend Requirements:**
- Accessible login form with proper labels and ARIA support
- Client-side validation for immediate feedback
- Responsive design for all device sizes
- Loading states and error handling
- Password strength indicator

**Backend Requirements:**
- Secure authentication endpoints with rate limiting
- JWT or session-based authentication
- Password hashing using industry-standard algorithms
- Two-factor authentication support
- Audit logging for security events

**Security Requirements:**
- HTTPS enforcement for all authentication requests
- CSRF protection for form submissions
- Secure session management with proper expiration
- Protection against common authentication attacks
- Compliance with data protection regulations"""
        
        elif "scroll" in title_lower or "scrolling" in title_lower:
            return """**Frontend Requirements:**
- Smooth scrolling implementation using CSS and JavaScript
- Touch gesture support for mobile devices
- Keyboard navigation compatibility
- Performance optimization for large content areas
- Cross-browser compatibility

**Performance Requirements:**
- 60fps scrolling performance
- Efficient DOM manipulation during scroll
- Memory management for large content sets
- Lazy loading for off-screen content
- Optimized event handling

**Accessibility Requirements:**
- Keyboard scroll support
- Screen reader compatibility
- Focus management during scroll
- High contrast mode support
- Reduced motion support for accessibility preferences"""
        
        else:
            return f"""**Frontend Requirements:**
- Modern, responsive user interface
- Cross-browser compatibility
- Mobile-first design approach
- Accessibility compliance (WCAG 2.1)
- Performance optimization

**Backend Requirements:**
- Scalable API architecture
- Database optimization
- Security best practices
- Error handling and logging
- Performance monitoring

**Integration Requirements:**
- Compatibility with existing {detected_app} systems
- API versioning and documentation
- Testing framework integration
- Deployment automation support
- Monitoring and alerting setup"""

    def _generate_success_metrics(self, title: str, detected_app: str, detected_role: str) -> str:
        """Generate success metrics and KPIs."""
        title_lower = title.lower()
        
        if "kanban" in title_lower and "taiga" in title_lower:
            return """**User Adoption Metrics:**
- 80% of active projects using kanban within 3 months
- Average daily active users on kanban boards
- User satisfaction score >4.5/5.0

**Productivity Metrics:**
- 25% reduction in task completion time
- 30% improvement in team velocity
- 20% increase in on-time delivery rate

**Technical Metrics:**
- <2 seconds load time for kanban boards
- <100ms response time for drag-and-drop operations
- 99.9% uptime for kanban functionality
- <1% error rate for kanban operations"""
        
        elif "login" in title_lower or "authentication" in title_lower:
            return """**Security Metrics:**
- 0 successful unauthorized access attempts
- 100% enforcement of strong password policies
- <2 seconds average login time
- <0.1% false positive lockout rate

**User Experience Metrics:**
- <5% login failure rate for valid credentials
- 95% user satisfaction with login experience
- <1% support tickets related to login issues
- 90% successful first-time login completion

**Performance Metrics:**
- <3 seconds page load time for login page
- <1 second authentication processing time
- 99.9% authentication service availability
- <100ms API response time for auth endpoints"""
        
        elif "scroll" in title_lower or "scrolling" in title_lower:
            return """**User Experience Metrics:**
- 95% user satisfaction with scrolling experience
- <5% user complaints about navigation issues
- 90% successful content discovery rate
- <2 seconds average time to find target content

**Performance Metrics:**
- 60fps scrolling performance maintained
- <100ms scroll response time
- <50ms touch gesture response time
- 99% smooth scrolling success rate

**Engagement Metrics:**
- 25% increase in content consumption
- 20% reduction in bounce rate
- 15% increase in time spent on page
- 30% improvement in task completion rates"""
        
        else:
            return f"""**User Adoption Metrics:**
- 70% feature adoption within 2 months
- 4.0+ average user satisfaction score
- <10% feature abandonment rate

**Productivity Metrics:**
- 20% improvement in task efficiency
- 15% reduction in time to completion
- 25% increase in user engagement
- 10% reduction in support requests

**Technical Metrics:**
- <2 seconds average response time
- 99.5% feature availability
- <1% error rate for core functionality
- 90% cross-platform compatibility"""

    def _generate_dependencies_risks(self, title: str, detected_app: str, detected_role: str) -> str:
        """Generate dependencies and risks assessment."""
        title_lower = title.lower()
        
        if "kanban" in title_lower and "taiga" in title_lower:
            return """**Dependencies:**
- Existing Taiga project management system
- User authentication and authorization service
- Database schema for kanban data storage
- Real-time communication infrastructure
- Frontend framework compatibility

**Risks:**
- Performance degradation with large datasets
- Browser compatibility issues with drag-and-drop
- Real-time synchronization conflicts
- User resistance to new workflow changes
- Integration complexity with existing features

**Mitigation Strategies:**
- Implement pagination and virtualization for large datasets
- Comprehensive cross-browser testing
- Conflict resolution mechanisms for concurrent updates
- User training and change management
- Phased rollout with rollback capability"""
        
        elif "login" in title_lower or "authentication" in title_lower:
            return """**Dependencies:**
- User database and authentication service
- Email service for password reset
- Two-factor authentication provider
- SSL/TLS certificate management
- Session storage infrastructure

**Risks:**
- Security vulnerabilities in authentication flow
- User data exposure or breach
- Service availability and single points of failure
- Compliance with data protection regulations
- User resistance to security measures

**Mitigation Strategies:**
- Regular security audits and penetration testing
- Implementation of defense-in-depth security measures
- Redundant infrastructure and disaster recovery
- Privacy by design and compliance frameworks
- User education and security awareness programs"""
        
        elif "scroll" in title_lower or "scrolling" in title_lower:
            return """**Dependencies:**
- Frontend framework and browser APIs
- Content management and delivery system
- Device and browser compatibility layers
- Performance monitoring tools
- Accessibility testing frameworks

**Risks:**
- Performance degradation on low-end devices
- Browser compatibility issues
- Accessibility compliance gaps
- User experience inconsistencies
- Impact on existing functionality

**Mitigation Strategies:**
- Progressive enhancement and graceful degradation
- Comprehensive cross-browser testing program
- Accessibility testing and compliance verification
- Performance monitoring and optimization
- Careful integration testing with existing features"""
        
        else:
            return f"""**Dependencies:**
- Existing {detected_app} infrastructure
- Third-party APIs and services
- Database systems and data storage
- Authentication and authorization services
- Monitoring and logging infrastructure

**Risks:**
- Integration complexity with existing systems
- Performance impact on current functionality
- User adoption and change management
- Technical debt and maintenance burden
- Resource allocation and timeline constraints

**Mitigation Strategies:**
- Phased implementation with thorough testing
- Performance monitoring and optimization
- User training and documentation
- Regular code reviews and quality assurance
- Contingency planning and risk monitoring"""

    def _assess_business_value(self, title: str) -> str:
        """Assess business value of the feature."""
        title_lower = title.lower()
        
        if "kanban" in title_lower or "board" in title_lower:
            return "HIGH - Essential for agile project management and team productivity"
        elif "login" in title_lower or "authentication" in title_lower:
            return "HIGH - Critical for user access and security compliance"
        elif "performance" in title_lower or "slow" in title_lower:
            return "HIGH - Direct impact on user experience and retention"
        elif "scroll" in title_lower or "navigation" in title_lower:
            return "MEDIUM - Important for user experience and accessibility"
        else:
            return "MEDIUM - Valuable enhancement for user satisfaction"

    def _assess_development_effort(self, title: str) -> str:
        """Assess development effort required."""
        title_lower = title.lower()
        
        if "kanban" in title_lower or "board" in title_lower:
            return "HIGH - Complex frontend with real-time features"
        elif "authentication" in title_lower or "login" in title_lower:
            return "HIGH - Security-critical with multiple integrations"
        elif "performance" in title_lower:
            return "HIGH - Requires optimization across multiple layers"
        elif "scroll" in title_lower or "navigation" in title_lower:
            return "MEDIUM - Frontend-focused with cross-browser considerations"
        else:
            return "MEDIUM - Standard development effort with testing"

    def _assess_story_priority(self, title: str) -> str:
        """Assess priority for the user story."""
        title_lower = title.lower()
        
        if "critical" in title_lower or "urgent" in title_lower:
            return "HIGH - Critical for business operations"
        elif "authentication" in title_lower or "security" in title_lower:
            return "HIGH - Security and compliance requirements"
        elif "performance" in title_lower:
            return "HIGH - Direct impact on user experience"
        elif "kanban" in title_lower or "board" in title_lower:
            return "MEDIUM - Important for team productivity"
        else:
            return "MEDIUM - Valuable enhancement for users"
