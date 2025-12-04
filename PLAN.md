# Implementation Plan - Hybrid AI Coding Assistant

**Purpose:** Step-by-step guide to implement changes from TODO.md
**Recovery:** If Claude crashes, continue from the last checked [x] item

---

## Pre-Flight Checklist

- [ ] Backup current working code: `cp -r src src_backup`
- [ ] Verify Ollama running: `ollama list`
- [ ] Verify models installed:
  - [ ] deepseek-r1:70b
  - [ ] qwen2.5:32b
  - [ ] nomic-embed-text

---

## STEP 1: Remove HRM Integration

**Goal:** Clean out HRM code that doesn't apply to this use case.

### 1.1 Update main.py
**File:** `main.py`

- [ ] Remove lines 79-89 (HRM status display in initialization)
- [ ] Remove HRM-related imports if any
- [ ] Keep everything else

**Before (lines 78-90):**
```python
if "multi_glm_system" not in st.session_state:
    with st.spinner("Initializing multi-model system with HRM..."):
        st.session_state.multi_glm_system = MultiModelGLMSystem()

        # Display HRM initialization status  <-- REMOVE THIS BLOCK
        hrm_status = getattr(st.session_state.multi_glm_system, 'hrm_wrapper', None)
        if hrm_status:
            st.success("🧠 HRM Local Wrapper initialized successfully")
            ...
```

**After:**
```python
if "multi_glm_system" not in st.session_state:
    with st.spinner("Initializing AI system..."):
        st.session_state.multi_glm_system = MultiModelGLMSystem()
        st.success("✅ System initialized")
```

### 1.2 Update multi_model_system.py
**File:** `src/core/multi_model_system.py`

- [ ] Read file first to understand structure
- [ ] Remove HRM wrapper imports
- [ ] Remove HRM initialization
- [ ] Remove HRM routing logic
- [ ] Simplify to 2 models: DeepSeek + Qwen

### 1.3 Archive HRM files (don't delete yet)
- [ ] Create `archive/` folder
- [ ] Move `src/integrations/hrm_local_wrapper.py` → `archive/`
- [ ] Move `src/integrations/hrm_integration.py` → `archive/`

### 1.4 Verify app still runs
```bash
streamlit run main.py
```
- [ ] App starts without errors
- [ ] Chat interface works

---

## STEP 2: Simplify Model Configuration

**Goal:** Clear 2-model setup with defined purposes.

### 2.1 Update model definitions
**File:** `src/core/multi_model_system.py`

- [ ] Define models clearly:
```python
MODELS = {
    "DeepSeek-R1:70B (Reasoning)": {
        "name": "deepseek-r1:70b",
        "purpose": "reasoning",
        "description": "Deep reasoning, planning, complex analysis"
    },
    "Qwen2.5:32B (Fast)": {
        "name": "qwen2.5:32b",
        "purpose": "summarization",
        "description": "Quick summaries, titles, simple tasks"
    }
}
```

### 2.2 Update UI model selection
**File:** `src/ui/ui_components.py` (or wherever model selection is)

- [ ] Find model selection dropdown
- [ ] Update to show only 2 models
- [ ] Add purpose hint in selection

### 2.3 Verify model selection works
- [ ] Can select DeepSeek
- [ ] Can select Qwen
- [ ] Both generate responses

---

## STEP 3: Add Export Buttons (Copy/Save/Format)

**Goal:** Add buttons after each AI response.

### 3.1 Find chat rendering code
**File:** `src/ui/ui_components.py` - look for `render_chat_interface`

- [ ] Locate where AI responses are displayed
- [ ] Identify the right place to add buttons (after response)

### 3.2 Add Copy button
```python
if st.button("📋 Copy Response", key=f"copy_{msg_idx}"):
    st.session_state.clipboard_content = response_text
    st.success("✓ Copied! Paste into Claude Code")
```

### 3.3 Add Save button
```python
if st.button("💾 Save to Project", key=f"save_{msg_idx}"):
    from datetime import datetime
    from pathlib import Path

    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    project = st.session_state.get("current_project", "Default")

    save_dir = Path(f"./projects/{project}/reasoning")
    save_dir.mkdir(parents=True, exist_ok=True)

    save_path = save_dir / f"session_{timestamp}.md"

    content = f"""# DeepSeek Reasoning Session
Date: {datetime.now().strftime("%Y-%m-%d %H:%M")}
Project: {project}

## Query
{user_message}

## Response
{response_text}
"""
    save_path.write_text(content)
    st.success(f"✓ Saved to {save_path}")
```

### 3.4 Add Format for Claude button
```python
if st.button("📤 Format for Claude", key=f"format_{msg_idx}"):
    formatted = f"""Based on this reasoning:

{response_text}

---
Please implement the above approach."""

    st.code(formatted, language="markdown")
    st.info("Copy above and paste into Claude Code")
```

### 3.5 Verify export buttons work
- [ ] Copy button shows success message
- [ ] Save button creates .md file in project/reasoning/
- [ ] Format button displays formatted text

---

## STEP 4: Add Summarization Buttons (Uses Qwen)

**Goal:** Quick summaries using Qwen2.5:32B.

### 4.1 Create summarization helper function
**File:** `src/core/multi_model_system.py` (or new file)

```python
def quick_summarize(self, text: str, max_words: int = 50) -> str:
    """Use Qwen for fast summarization"""
    prompt = f"Summarize in {max_words} words or less:\n\n{text}"

    response = self.ollama_client.generate(
        model="qwen2.5:32b",
        prompt=prompt
    )
    return response['response'].strip()

def generate_title(self, chat_history: str) -> str:
    """Generate 6-word title using Qwen"""
    prompt = f"Generate a 6-word title for this conversation:\n\n{chat_history}"

    response = self.ollama_client.generate(
        model="qwen2.5:32b",
        prompt=prompt
    )
    return response['response'].strip()
```

### 4.2 Add Generate Title button
**File:** `src/ui/ui_components.py`

```python
if st.button("📝 Generate Title"):
    with st.spinner("Generating title..."):
        chat_text = "\n".join([m["content"] for m in chat_history])
        title = st.session_state.multi_glm_system.generate_title(chat_text)
        st.session_state.chat_title = title
        st.success(f"Title: {title}")
```

### 4.3 Add Quick Summary button
```python
if st.button("⚡ Quick Summary"):
    with st.spinner("Summarizing..."):
        chat_text = "\n".join([m["content"] for m in chat_history])
        summary = st.session_state.multi_glm_system.quick_summarize(chat_text, max_words=100)
        st.info(f"**Summary:** {summary}")
```

### 4.4 Verify summarization works
- [ ] Generate Title produces short title
- [ ] Quick Summary produces ~100 word summary
- [ ] Both are fast (Qwen, not DeepSeek)

---

## STEP 5: Add Multi-Chat Summarization

**Goal:** Combine multiple saved chats into context summary.

### 5.1 Create saved chats browser
**File:** `src/ui/ui_components.py` or new component

```python
def render_saved_chats_browser(project: str):
    """Browse and select saved reasoning sessions"""
    reasoning_dir = Path(f"./projects/{project}/reasoning")

    if not reasoning_dir.exists():
        st.info("No saved sessions yet")
        return []

    saved_files = list(reasoning_dir.glob("*.md"))

    if not saved_files:
        st.info("No saved sessions yet")
        return []

    # Display as checkboxes
    selected = []
    for f in sorted(saved_files, reverse=True):
        if st.checkbox(f.name, key=f"select_{f.name}"):
            selected.append(f)

    return selected
```

### 5.2 Add Summarize Selected button
```python
if st.button("📚 Summarize Selected Chats"):
    selected_files = render_saved_chats_browser(project)

    if selected_files:
        combined_text = ""
        for f in selected_files:
            combined_text += f.read_text() + "\n\n---\n\n"

        with st.spinner("Summarizing selected chats..."):
            summary = st.session_state.multi_glm_system.quick_summarize(
                combined_text, max_words=200
            )

        st.text_area("Combined Summary", summary, height=200)

        if st.button("📋 Copy Summary"):
            st.session_state.clipboard_content = summary
            st.success("✓ Copied!")
```

### 5.3 Verify multi-chat summarization
- [ ] Can browse saved chats
- [ ] Can select multiple
- [ ] Summary combines them
- [ ] Can copy summary

---

## STEP 6: Final Cleanup & Testing

### 6.1 Remove unused imports
- [ ] Check all modified files for unused imports
- [ ] Remove any remaining HRM references

### 6.2 Update UI text
- [ ] Change "Multi-Model GLM System" → "AI Coding Assistant"
- [ ] Update help text in expanders
- [ ] Remove references to HRM in UI

### 6.3 Full workflow test
- [ ] Start fresh session
- [ ] Ask DeepSeek a reasoning question
- [ ] Wait for response
- [ ] Click Copy → verify clipboard
- [ ] Click Save → verify file created
- [ ] Click Format → verify output
- [ ] Click Generate Title → verify fast response
- [ ] Save multiple sessions
- [ ] Click Summarize Selected → verify combines

### 6.4 Clean up
- [ ] Delete `src_backup` if all works
- [ ] Keep `archive/` for reference
- [ ] Update README if needed

---

## Recovery Points

If something breaks, restore from:

1. **Full restore:** `cp -r src_backup/* src/`
2. **HRM only:** Copy back from `archive/`
3. **Git:** `git checkout -- src/` (if committed)

---

## Files Modified Summary

| File | Changes |
|------|---------|
| `main.py` | Remove HRM init display |
| `src/core/multi_model_system.py` | Remove HRM, add summarize functions |
| `src/ui/ui_components.py` | Add export buttons, summarize buttons |
| `src/integrations/hrm_*.py` | Moved to archive/ |

---

## Next Session Prompt

If Claude crashes, paste this:

```
Continue implementing the Hybrid AI Coding Assistant from PLAN.md.
Read PLAN.md and TODO.md first.
Check which items are marked [x] completed.
Continue from the first unchecked [ ] item.
```

---

*Created: December 2024*
*Last checkpoint: Initial plan created*
