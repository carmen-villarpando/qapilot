# 🎭 QAPilot Demo Guide

Complete guide to configure and demonstrate QAPilot for hackathon or presentation.

## 🎯 **5-Minute Demo**

### **Problem Scenario**
"Developers create issues with poor titles like 'bug' or 'not working', wasting time on clarifications."

### **QAPilot Solution**
QAPilot automatically transforms simple titles into complete, professional issues.

---

## 🚀 **Step-by-Step Setup (For Demo)**

### **Step 1: GitHub Secrets (2 minutes)**

Go to: **https://github.com/carmen-villarpando/qapilot/settings/secrets/actions**

**1. GITHUB_TOKEN**
- Click "New repository secret"
- Name: `GITHUB_TOKEN`
- Value: `ghp_xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx`
- *Get from: GitHub → Settings → Developer settings → Personal access tokens → Tokens (classic)*

**2. GITHUB_MODELS_TOKEN**
- Click "New repository secret"
- Name: `GITHUB_MODELS_TOKEN`
- Value: `ghp_xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx`
- *Get from: GitHub → Settings → Developer settings → GitHub Models*

### **Step 2: Enable GitHub Actions (30 seconds)**

Go to: **https://github.com/carmen-villarpando/qapilot/settings/actions**

- ✅ "Allow all actions"
- ✅ "Allow read and write permissions"

---

## 🎪 **Demo Script**

### **Intro (30 seconds)**
> "Today I'm presenting QAPilot: the automatic solution for improving GitHub issues. Ever received an issue that just says 'bug' and don't know what to do? QAPilot fixes it automatically."

### **Live Demo (2 minutes)**

**1. Create Issue**
```
Title: "scroll not working"
```

**2. Activate QAPilot**
```
Comment: /improve-issue
```

**3. Automatic Magic**
- 🤖 QAPilot analyzes the title
- 📝 Generates detailed description
- 🔧 Adds reproduction steps
- ✅ Defines expected behavior
- 🏷️ Suggests relevant labels
- 📊 Assigns priority

### **Final Result**
```
## 📝 Problem Description
Team member reports scrolling issues in the interface. This issue affects the navigation experience when trying to access content that exceeds the visible screen area...

## 🔧 Steps to Reproduce
1. Access the application/website
2. Navigate to the affected section
3. Attempt to scroll vertically or horizontally
4. Observe that scroll doesn't respond or works incorrectly

## ✅ Expected Behavior
The user should be able to smoothly scroll through all content using mouse wheel, trackpad, or touch gestures...

## 📊 Metadata
**Priority:** medium
**Suggested Assignee:** frontend-team
```

---

## 💡 **Key Demo Points**

### **🎯 Problem Solved**
- **Before**: Ambiguous issues → wasted time
- **After**: Complete issues → efficient development

### **🚀 Benefits**
- **100% Free**: No hidden costs
- **GitHub Native**: No external apps
- **Manual Control**: User decides when to use it
- **Powerful AI**: GitHub Models API

### **🌟 Advanced Features**
- **App Detection**: Automatically identifies Taiga, OpenProject, GitHub
- **Role-Based Perspectives**: QA Manager, Frontend, Security, etc.
- **Feature Validation**: ✅ Confirmed or ⚠️ Not confirmed functionality
- **English Support**: Full internationalization

---

## 📊 **Cost Analysis**

### **GitHub Actions (Free Tier)**
- **2,000 minutes/month** free
- **QAPilot usage**: ~1 minute per issue
- **Result**: **2,000 issues/month free**

### **GitHub Models API (Beta)**
- **Currently free** during beta
- **No token limits** for testing
- **Production-ready**: Affordable pricing expected

### **Total Cost: $0/month** 🎉

---

## 🎯 **Success Metrics**

✅ **Issue improved in under 2 minutes**
✅ **Complete description with technical details**
✅ **Proper labels and assignee suggestions**
✅ **Role-based perspective included**
✅ **App-specific terminology when applicable**

---

## 🚀 **Call to Action**

> "QAPilot transforms how teams handle GitHub issues. From ambiguous bug reports to complete, actionable tasks - automatically. Try it today in your repository!"

**Ready for your demo!** 🎭
