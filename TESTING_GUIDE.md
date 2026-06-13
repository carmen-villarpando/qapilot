# 🎮 QAPilot Testing Guide in GitHub UI

Step-by-step guide to test QAPilot directly in the GitHub interface.

## 🚀 **Step 1: Go to Repository**

**URL:** `https://github.com/carmen-villarpando/qapilot`

## 📝 **Step 2: Create an Issue**

1. **Click on "Issues"** (top bar of repository)
2. **Click on "New issue"** (green button)
3. **Complete the issue:**
   - **Title**: `scroll not working in dashboard`
   - **Description**: (leave empty or put something simple)
   - **Labels**: (don't select anything)
4. **Click on "Submit new issue"**

## 💬 **Step 3: Activate QAPilot**

1. **In the newly created issue**, look for the comments section
2. **Write the command:**
   ```
   /improve-issue
   ```
3. **Click on "Comment"**

## ⏱️ **Step 4: Wait for the Magic**

### **What You'll See Happen:**

**🔥 Immediate (1-5 seconds):**
- QAPilot will add a 👍 reaction to your comment

**⚡ Processing (30-60 seconds):**
- Go to the **"Actions"** tab of the repository
- You'll see the **"Improve Issue with QAPilot"** workflow running
- The workflow will show: `⏳ Running` → `✅ Success`

**🎉 Result (1-2 minutes total):**
- The issue will automatically update with:
  - 📝 **Detailed description**
  - 🔧 **Reproduction steps**
  - ✅ **Expected behavior**
  - 🏷️ **Suggested labels**
  - 📊 **Priority and assignee**

## 🔍 **Step 5: Verify the Result**

**The issue will now contain:**

```markdown
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

## 🎯 **Step 6: See the Confirmation Comment**

QAPilot will add a comment like:
```
🚀 **Issue improved by QAPilot!**

Triggered by @your-username
Added description, reproduction steps, expected behavior, and labels.
```

## ⚠️ **If It Doesn't Work**

### **Check GitHub Actions:**
1. Go to: `https://github.com/carmen-villarpando/qapilot/actions`
2. Look for the most recent workflow
3. If it's red ❌, click to see the logs

### **Possible Issues:**
- **GitHub Actions not enabled**: Go to Settings → Actions
- **Incorrect secrets**: Check QAPILOT_GITHUB_TOKEN and QAPILOT_MODELS_TOKEN
- **Insufficient permissions**: Token needs `repo` and `workflow` scopes

## 🎪 **For Hackathon Demo**

**Suggested Script:**

> "Look at this issue with a simple title: 'scroll not working'. Now I'll improve it with QAPilot."
> 
> *(Comment `/improve-issue`)*
> 
> "Watch as QAPilot automatically transforms this into a complete, professional issue with description, steps, expected behavior, and proper labels!"

## 🌟 **Advanced Features to Showcase**

### **App-Specific Terminology**
Try titles like:
- `"kanban board not loading"` → Detects Taiga, adds Kanban terminology
- `"login authentication fails"` → Detects security context, adds auth terminology

### **Role-Based Perspectives**
QAPilot automatically detects the appropriate role:
- **QA Manager**: Focus on testing and quality
- **Frontend Engineer**: Focus on UI/UX
- **Security Engineer**: Focus on authentication and vulnerabilities

### **Feature Validation**
QAPilot validates if mentioned features exist:
- ✅ **Confirmed**: Feature exists in the detected app
- ⚠️ **Not confirmed**: Feature doesn't exist or needs clarification

## 📊 **Expected Results**

**Before QAPilot:**
- Title: `"bug"`
- Description: Empty
- Labels: None

**After QAPilot:**
- Title: Enhanced with context
- Description: Complete with sections
- Labels: Relevant and specific
- Assignee: Suggested based on content
- Priority: Automatically determined

---

## 🎯 **Success Metrics**

✅ **Issue improved in under 2 minutes**
✅ **Complete description with technical details**
✅ **Proper labels and assignee suggestions**
✅ **Role-based perspective included**
✅ **App-specific terminology when applicable**

**Ready for your demo!** 🚀
