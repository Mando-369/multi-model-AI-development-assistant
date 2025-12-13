"""Project Meta UI - Dedicated tab for project-level strategic planning."""

import streamlit as st
from datetime import datetime
from typing import Optional
from ..core.prompts import AGENT_MODES


def render_project_meta_tab(glm_system, selected_project: str):
    """Render the Project Meta tab interface."""
    st.header("📋 Project Meta")

    # Check for Default project
    if selected_project == "Default":
        st.info(
            "**Project Meta is not available for the Default project.**\n\n"
            "Create a named project to use Project Meta features:\n"
            "- Strategic roadmap and milestones\n"
            "- Cross-agent coordination\n"
            "- Export queue for Claude Code"
        )
        return

    st.caption(f"Project: **{selected_project}** | Strategic planning and cross-agent coordination")

    # Ensure PROJECT_META.md exists
    project_meta = glm_system.project_meta_manager.ensure_project_meta(selected_project)

    # Quick Actions Bar
    render_quick_actions(glm_system, selected_project)

    st.write("---")

    # Main content: Two columns
    col_meta, col_chat = st.columns([3, 2])

    with col_meta:
        render_meta_viewer_editor(glm_system, selected_project)

    with col_chat:
        render_orchestrator_chat(glm_system, selected_project)


def render_quick_actions(glm_system, project_name: str):
    """Render quick action buttons."""
    st.subheader("⚡ Quick Actions")

    # Session state keys
    summary_key = f"project_summary_{project_name}"
    init_result_key = f"init_agents_result_{project_name}"

    col1, col2, col3, col4, col5 = st.columns(5)

    with col1:
        if st.button("🚀 Initialize Agents", help="Create initial context for each agent based on PROJECT_META"):
            with st.spinner("Initializing agents..."):
                result = initialize_all_agents(glm_system, project_name)
                st.session_state[init_result_key] = result
                st.rerun()

    with col2:
        if st.button("🔄 Sync from Agents", help="Synthesize all agent metas into PROJECT_META"):
            render_sync_dialog(glm_system, project_name)

    with col3:
        if st.button("📊 Generate Summary", help="Create exportable project summary"):
            with st.spinner("Generating summary..."):
                summary = _generate_summary_content(glm_system, project_name)
                if summary:
                    st.session_state[summary_key] = summary
                    st.rerun()

    with col4:
        if st.button("📤 Export Queue", help="Show items ready for Claude Code"):
            show_export_queue(glm_system, project_name)

    with col5:
        if st.button("🔃 Refresh", help="Reload PROJECT_META.md"):
            st.rerun()

    # Display initialization result if available
    if st.session_state.get(init_result_key):
        result = st.session_state[init_result_key]
        st.write("---")
        if result["success"]:
            st.success(f"✅ Initialized {result['count']} agents: {', '.join(result['agents'])}")
        else:
            st.error(f"❌ Failed to initialize agents: {result.get('error', 'Unknown error')}")
        if st.button("Dismiss", key="dismiss_init_result"):
            st.session_state[init_result_key] = None
            st.rerun()

    # Display summary OUTSIDE columns (full width) if available
    if st.session_state.get(summary_key):
        st.write("---")
        st.markdown("### 📋 Project Summary")
        st.code(st.session_state[summary_key], language="markdown")
        col_a, col_b = st.columns([1, 5])
        with col_a:
            if st.button("❌ Close Summary", key="close_summary"):
                st.session_state[summary_key] = None
                st.rerun()
        with col_b:
            st.info("Use the copy button (top-right of code block) to copy to Claude Code")


def render_meta_viewer_editor(glm_system, project_name: str):
    """Render markdown viewer/editor for PROJECT_META.md."""
    st.subheader("📄 PROJECT_META.md")

    # Get current content
    content = glm_system.project_meta_manager.read_project_meta(project_name)
    update_info = glm_system.project_meta_manager.get_last_update_info(project_name)

    # Show last update info
    if update_info["timestamp"]:
        st.caption(f"Last updated: {update_info['timestamp'][:19]} by {update_info['updated_by']}")

    # Edit mode toggle
    edit_key = f"project_meta_edit_mode_{project_name}"
    if edit_key not in st.session_state:
        st.session_state[edit_key] = False

    col1, col2, col3 = st.columns([1, 1, 2])
    with col1:
        if st.button("📝 Edit" if not st.session_state[edit_key] else "👁️ View"):
            st.session_state[edit_key] = not st.session_state[edit_key]
            st.rerun()

    with col2:
        if st.session_state[edit_key]:
            if st.button("💾 Save", type="primary"):
                new_content = st.session_state.get(f"meta_editor_{project_name}", content)
                if glm_system.project_meta_manager.save_project_meta(project_name, new_content, "manual"):
                    st.success("Saved!")
                    st.session_state[edit_key] = False
                    st.rerun()
                else:
                    st.error("Failed to save")

    # Display content
    if st.session_state[edit_key]:
        # Edit mode
        st.text_area(
            "Edit PROJECT_META.md:",
            value=content,
            height=500,
            key=f"meta_editor_{project_name}",
            help="Edit the project meta file directly. Save when done."
        )
    else:
        # View mode with styled markdown
        st.markdown(
            """
            <style>
            .project-meta-view {
                background: linear-gradient(135deg, #1e1e2e 0%, #313244 100%);
                padding: 20px;
                border-radius: 10px;
                border: 1px solid #45475a;
                max-height: 500px;
                overflow-y: auto;
            }
            </style>
            """,
            unsafe_allow_html=True
        )
        with st.container():
            st.markdown(content)


def render_orchestrator_chat(glm_system, project_name: str):
    """Render chat interface scoped to Orchestrator agent."""
    st.subheader("🎯 Orchestrator Chat")
    st.caption("Chat with the Orchestrator to update PROJECT_META.md")

    # Orchestrator chat history (separate from main chat)
    chat_key = f"orchestrator_chat_{project_name}"
    suggestion_key = f"orchestrator_suggestion_{project_name}"
    loaded_key = f"orchestrator_loaded_{project_name}"

    # Load saved chats from file on first access
    if chat_key not in st.session_state:
        saved_chats = glm_system.project_manager.load_project_chats(project_name, "Orchestrator")
        st.session_state[chat_key] = saved_chats if saved_chats else []
        st.session_state[loaded_key] = True

    if suggestion_key not in st.session_state:
        st.session_state[suggestion_key] = None

    # Model selection for Orchestrator
    model_options = list(glm_system.models.keys())
    selected_model = st.selectbox(
        "Model:",
        model_options,
        index=0,
        key=f"orchestrator_model_{project_name}",
        help="Reasoning model for complex planning, Fast model for quick updates"
    )

    # Chat input
    question = st.text_area(
        "Ask Orchestrator:",
        placeholder="Examples:\n- Mark filter design as complete\n- Add new milestone for GUI\n- Update the roadmap\n- What's blocking progress?",
        height=350,
        key=f"orchestrator_input_{project_name}"
    )

    col1, col2, col3 = st.columns(3)
    with col1:
        send_disabled = not question.strip()
        if st.button("🚀 Send", disabled=send_disabled, key=f"orchestrator_send_{project_name}"):
            with st.spinner(f"🧠 {selected_model} (Orchestrator) thinking..."):
                # Get response from Orchestrator agent
                result = glm_system.generate_response(
                    prompt=question,
                    selected_model=selected_model,
                    use_context=True,
                    project_name=project_name,
                    chat_history=st.session_state[chat_key],
                    agent_mode="Orchestrator"
                )

                response = result.get("response", "Error getting response")

                # Add to chat history (with agent_mode)
                st.session_state[chat_key].append((question, response, "Orchestrator"))

                # Save to project chat file (with agent_mode)
                glm_system.project_manager.save_chat_to_project(
                    project_name, "Orchestrator", question, response, "Orchestrator"
                )

                # Clear any previous suggestion
                st.session_state[suggestion_key] = None

                st.rerun()

    with col2:
        # Generate suggestion button - only show if there's chat history
        suggest_disabled = len(st.session_state[chat_key]) == 0
        if st.button("✨ Suggest Update", disabled=suggest_disabled, key=f"orchestrator_suggest_{project_name}",
                     help="Generate suggested changes to PROJECT_META.md based on conversation"):
            with st.spinner("Generating suggestion..."):
                suggestion = generate_meta_suggestion(glm_system, project_name, st.session_state[chat_key])
                if suggestion:
                    st.session_state[suggestion_key] = suggestion
                    st.rerun()

    with col3:
        if st.button("🗑️ Clear", key=f"orchestrator_clear_{project_name}"):
            st.session_state[chat_key] = []
            st.session_state[suggestion_key] = None
            st.rerun()

    # Display suggestion with approval if available
    if st.session_state[suggestion_key]:
        render_suggestion_approval(glm_system, project_name, suggestion_key)

    # Display all exchanges (no limit)
    if st.session_state[chat_key]:
        st.write("---")
        st.caption(f"All exchanges ({len(st.session_state[chat_key])} total):")
        for i, entry in enumerate(reversed(st.session_state[chat_key])):
            # Handle both 2-tuple (legacy) and 3-tuple (with agent_mode) formats
            q, a = entry[0], entry[1]
            agent = entry[2] if len(entry) == 3 else "Orchestrator"
            with st.expander(f"Q{len(st.session_state[chat_key]) - i} [{agent}]: {q[:50]}...", expanded=(i == 0)):
                st.caption(f"🏷️ **Agent:** {agent}")
                st.markdown(f"**Question:** {q}")
                st.markdown("**Response:**")
                st.code(a, language="markdown")


def generate_meta_suggestion(glm_system, project_name: str, chat_history: list) -> Optional[str]:
    """Generate suggested PROJECT_META.md update based on Orchestrator conversation."""
    try:
        current_meta = glm_system.project_meta_manager.read_project_meta(project_name)
        if not current_meta:
            return None

        # Format recent conversation (handle both 2-tuple and 3-tuple formats)
        recent_exchanges = chat_history[-5:]  # Last 5 exchanges
        conversation = "\n\n".join([
            f"USER: {entry[0]}\nORCHESTRATOR: {entry[1]}"
            for entry in recent_exchanges
        ])

        prompt = f"""You are updating a PROJECT_META.md file based on an Orchestrator conversation.

CURRENT PROJECT_META.md:
{current_meta}

RECENT ORCHESTRATOR CONVERSATION:
{conversation}

TASK:
Based on the conversation, generate an UPDATED PROJECT_META.md that incorporates:
- Status changes mentioned (planned → in-progress → completed)
- New milestones or tasks discussed
- Architecture decisions made
- Items ready for export
- Any other relevant updates

RULES:
- Preserve the existing structure
- Only change sections that need updating based on the conversation
- Keep all unchanged content intact
- Update the "Last Updated" timestamp and set "Updated By: orchestrator"

Return ONLY the complete updated PROJECT_META.md content, nothing else."""

        # Use fast model for suggestion generation
        fast_model = glm_system.get_fast_model_name()
        llm = glm_system.get_model_instance(fast_model)
        if llm:
            result = llm.invoke(prompt)
            return result.strip()
        return None

    except Exception as e:
        print(f"Error generating meta suggestion: {e}")
        return None


def render_suggestion_approval(glm_system, project_name: str, suggestion_key: str):
    """Render suggestion preview with approve/reject buttons."""
    st.write("---")
    st.subheader("📝 Suggested Update")
    st.caption("Review the suggested changes to PROJECT_META.md")

    suggestion = st.session_state[suggestion_key]

    # Show suggestion in expandable view
    with st.expander("Preview suggested PROJECT_META.md", expanded=True):
        st.code(suggestion, language="markdown")

    col1, col2 = st.columns(2)
    with col1:
        if st.button("✅ Apply Changes", type="primary", key=f"apply_suggestion_{project_name}"):
            if glm_system.project_meta_manager.save_project_meta(project_name, suggestion, "orchestrator"):
                st.success("PROJECT_META.md updated!")
                st.session_state[suggestion_key] = None
                st.rerun()
            else:
                st.error("Failed to save changes")

    with col2:
        if st.button("❌ Discard", key=f"discard_suggestion_{project_name}"):
            st.session_state[suggestion_key] = None
            st.rerun()


def render_sync_dialog(glm_system, project_name: str):
    """Render sync dialog with merge/replace options."""
    st.write("---")
    st.subheader("🔄 Sync from Agents")

    # Get all agent metas
    all_metas = glm_system.project_meta_manager.get_all_agent_metas(project_name)

    if not all_metas:
        st.warning("No agent context files found. Chat with specialist agents first to generate context.")
        return

    st.info(f"Found {len(all_metas)} agent contexts: {', '.join(all_metas.keys())}")

    # Show preview of what will be synced
    with st.expander("Preview agent contexts"):
        for agent, content in all_metas.items():
            st.markdown(f"**{agent}:**")
            st.text(content[:500] + "..." if len(content) > 500 else content)
            st.write("---")

    # Sync mode selection
    sync_mode = st.radio(
        "Sync mode:",
        ["merge", "replace"],
        format_func=lambda x: "Merge (add new info, preserve manual edits)" if x == "merge" else "Replace (regenerate from agent contexts)",
        key=f"sync_mode_{project_name}"
    )

    if st.button("✅ Confirm Sync", type="primary"):
        with st.spinner("Syncing from agents..."):
            success = sync_from_agents(glm_system, project_name, sync_mode)
            if success:
                st.success("Sync complete! PROJECT_META.md updated.")
                st.rerun()
            else:
                st.error("Sync failed. Check console for errors.")


def sync_from_agents(glm_system, project_name: str, mode: str) -> bool:
    """Sync PROJECT_META.md from all agent metas using fast model."""
    try:
        all_metas = glm_system.project_meta_manager.get_all_agent_metas(project_name)
        if not all_metas:
            return False

        current_meta = glm_system.project_meta_manager.read_project_meta(project_name)

        # Build sync prompt
        combined_agents = "\n\n".join([
            f"=== {agent.upper()} AGENT ===\n{content}"
            for agent, content in all_metas.items()
        ])

        if mode == "merge":
            prompt = f"""You are updating a PROJECT_META.md file by MERGING new information from agent contexts.

CURRENT PROJECT_META.md:
{current_meta}

AGENT CONTEXTS TO MERGE:
{combined_agents}

TASK:
1. Read the current PROJECT_META.md structure
2. Add new information from agent contexts WITHOUT removing existing manual edits
3. Update milestone statuses based on what agents report
4. Add new items to Export Queue if agents mention completed work
5. Preserve the document structure

Return ONLY the updated PROJECT_META.md content."""

        else:  # replace
            prompt = f"""You are regenerating a PROJECT_META.md file from agent contexts.

PROJECT NAME: {project_name}

AGENT CONTEXTS:
{combined_agents}

TASK:
Generate a complete PROJECT_META.md with:
- Vision & Goals (synthesized from agent work)
- Current Roadmap (milestones from agent contexts)
- Architecture Decisions (technical choices made)
- Agent Handoffs (based on what each agent is doing)
- Export Queue (items ready for implementation)
- Completed Work (what's been finished)
- Cross-Cutting Concerns (shared patterns)

Use this exact structure:
# Project: {project_name}
Last Updated: {datetime.now().isoformat()}
Updated By: auto-sync

## Vision & Goals
...

## Current Roadmap
| Milestone | Status | Target | Notes |
...

## Architecture Decisions
...

## Agent Handoffs
...

## Export Queue (Ready for Claude Code)
...

## Completed Work
...

## Cross-Cutting Concerns
...

Return ONLY the PROJECT_META.md content."""

        # Use fast model for speed
        fast_model = glm_system.get_fast_model_name()
        llm = glm_system.get_model_instance(fast_model)
        if llm:
            updated_content = llm.invoke(prompt)
            return glm_system.project_meta_manager.save_project_meta(
                project_name, updated_content.strip(), "auto-sync"
            )

        return False

    except Exception as e:
        print(f"Error syncing from agents: {e}")
        return False


def _generate_summary_content(glm_system, project_name: str) -> Optional[str]:
    """Generate project summary content (helper function)."""
    project_meta = glm_system.project_meta_manager.read_project_meta(project_name)
    if not project_meta:
        st.warning("No PROJECT_META.md found")
        return None

    prompt = f"""Summarize this project for export to a coding tool (like Claude Code).

PROJECT_META.md:
{project_meta}

Create a concise summary (200 words max) covering:
1. Project goal
2. Current status
3. Next steps
4. Key technical decisions

Format for easy copy-paste."""

    fast_model = glm_system.get_fast_model_name()
    llm = glm_system.get_model_instance(fast_model)
    if llm:
        return llm.invoke(prompt)
    return None


def initialize_all_agents(glm_system, project_name: str) -> dict:
    """Initialize context files for all specialist agents based on PROJECT_META.md.

    Creates initial context for each agent (FAUST, JUCE, Math, Physics, General)
    tailored to their specialty based on the project's vision and roadmap.

    Returns:
        dict with 'success', 'count', 'agents', and optionally 'error' keys
    """
    try:
        project_meta = glm_system.project_meta_manager.read_project_meta(project_name)
        if not project_meta or len(project_meta.strip()) < 100:
            return {
                "success": False,
                "error": "PROJECT_META.md is empty or too short. Fill in the vision and roadmap first."
            }

        # Agents to initialize (excluding Orchestrator - it manages, doesn't do work)
        agents_to_init = ["General", "FAUST", "JUCE", "Math", "Physics"]
        initialized = []

        fast_model = glm_system.get_fast_model_name()
        llm = glm_system.get_model_instance(fast_model)
        if not llm:
            return {"success": False, "error": f"Could not get fast model ({fast_model})"}

        # Get agent modes for specialization info
        agent_modes = AGENT_MODES

        for agent_name in agents_to_init:
            if agent_name not in agent_modes:
                continue

            agent_info = agent_modes[agent_name]
            file_prefix = agent_info["file_prefix"]
            description = agent_info["description"]

            prompt = f"""Based on this project, create an initial context file for the {agent_name} specialist agent.

PROJECT_META.md:
{project_meta}

AGENT SPECIALTY:
{description}

TASK:
Create a focused context file (~200-300 words) that helps the {agent_name} agent understand:
1. What aspects of this project relate to their specialty
2. Specific tasks or challenges they may be asked about
3. Any constraints or decisions that affect their domain
4. Key files or components they should be aware of

If this project doesn't seem relevant to {agent_name}'s specialty, create a brief note explaining that and suggesting they may not be the primary agent for this project.

Format as markdown with clear sections. Start with "# {agent_name} Context for [Project Name]"."""

            try:
                context = llm.invoke(prompt)
                if context:
                    # Save to agent context file
                    agents_dir = glm_system.project_meta_manager.projects_dir / project_name / "agents"
                    agents_dir.mkdir(parents=True, exist_ok=True)

                    context_file = agents_dir / f"{file_prefix}_context.md"
                    context_file.write_text(context.strip(), encoding="utf-8")
                    initialized.append(agent_name)
            except Exception as e:
                print(f"Error initializing {agent_name}: {e}")
                continue

        if initialized:
            return {
                "success": True,
                "count": len(initialized),
                "agents": initialized
            }
        else:
            return {"success": False, "error": "No agents could be initialized"}

    except Exception as e:
        print(f"Error in initialize_all_agents: {e}")
        return {"success": False, "error": str(e)}


def generate_project_summary(glm_system, project_name: str):
    """Generate an exportable project summary (legacy wrapper)."""
    summary = _generate_summary_content(glm_system, project_name)
    if summary:
        st.code(summary, language="markdown")
        st.info("Copy above and paste into Claude Code")


def show_export_queue(glm_system, project_name: str):
    """Display and manage export queue items."""
    items = glm_system.project_meta_manager.extract_export_queue(project_name)

    st.write("---")
    st.subheader("📤 Export Queue")

    if not items:
        st.info("Export queue is empty. Add items ready for Claude Code implementation.")
        return

    st.success(f"**{len(items)} items ready for export:**")

    for i, item in enumerate(items):
        col1, col2 = st.columns([4, 1])
        with col1:
            st.markdown(f"- {item}")
        with col2:
            if st.button("📋", key=f"copy_export_{i}", help="Copy to clipboard"):
                st.code(item)
