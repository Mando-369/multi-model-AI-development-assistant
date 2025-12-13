"""
Model Setup UI - Configure which models to use for Reasoning and Fast tasks.
"""

import streamlit as st
from typing import List, Dict, Any
from ..core.model_backends import get_backend_manager, ModelInfo
from ..core.model_config import get_model_config, reload_model_config


def render_model_setup_tab(glm_system):
    """Render the Model Setup tab for configuring model roles."""
    st.header("⚙️ Model Setup")
    st.caption("Configure which models to use for Reasoning and Fast tasks")

    # Get backend manager and current config
    backend_manager = get_backend_manager()
    model_config = get_model_config()

    # Current configuration display
    st.subheader("📊 Current Configuration")

    col1, col2 = st.columns(2)
    with col1:
        reasoning = model_config.get_reasoning_model()
        st.info(f"""
        **🧠 Reasoning Model**
        - Display Name: `{reasoning.display_name}`
        - Model ID: `{reasoning.model_id}`
        - Backend: `{reasoning.backend}`
        """)

    with col2:
        fast = model_config.get_fast_model()
        st.info(f"""
        **⚡ Fast Model**
        - Display Name: `{fast.display_name}`
        - Model ID: `{fast.model_id}`
        - Backend: `{fast.backend}`
        """)

    st.divider()

    # Scan for available models
    st.subheader("🔍 Available Models")

    if st.button("🔄 Scan Ollama Models", use_container_width=True):
        with st.spinner("Scanning for available models..."):
            st.session_state.available_models = scan_available_models(backend_manager)
        st.rerun()

    # Get available models from session state or scan
    if "available_models" not in st.session_state:
        st.session_state.available_models = scan_available_models(backend_manager)

    available_models = st.session_state.available_models

    if not available_models.get("ollama"):
        st.warning("No Ollama models found. Make sure Ollama is running and has models installed.")
        st.code("ollama list  # Check installed models\nollama pull <model>  # Pull a model")
    else:
        # Display available models
        with st.expander(f"📋 Ollama Models ({len(available_models['ollama'])} found)", expanded=True):
            for model in available_models["ollama"]:
                cols = st.columns([3, 1, 1])
                with cols[0]:
                    st.write(f"**{model.name}**")
                    st.caption(f"`{model.id}`")
                with cols[1]:
                    st.caption(model.size)
                with cols[2]:
                    # Mark if currently selected
                    if model.id == reasoning.model_id:
                        st.success("Reasoning")
                    elif model.id == fast.model_id:
                        st.success("Fast")

    st.divider()

    # Model selection form
    st.subheader("🔧 Configure Model Roles")

    # Build options list from available models
    model_options = []
    model_id_map = {}

    for model in available_models.get("ollama", []):
        display = f"{model.name} ({model.id})"
        model_options.append(display)
        model_id_map[display] = model

    if not model_options:
        st.warning("No models available to select. Scan for models first.")
        return

    # Find current selections in options
    current_reasoning_idx = 0
    current_fast_idx = 0

    for i, option in enumerate(model_options):
        model = model_id_map[option]
        if model.id == reasoning.model_id:
            current_reasoning_idx = i
        if model.id == fast.model_id:
            current_fast_idx = i

    col1, col2 = st.columns(2)

    with col1:
        st.markdown("**🧠 Reasoning Model**")
        st.caption("For complex tasks: planning, architecture, deep analysis")
        new_reasoning = st.selectbox(
            "Select reasoning model:",
            model_options,
            index=current_reasoning_idx,
            key="reasoning_model_select",
            label_visibility="collapsed"
        )

    with col2:
        st.markdown("**⚡ Fast Model**")
        st.caption("For quick tasks: summarization, titles, simple queries")
        new_fast = st.selectbox(
            "Select fast model:",
            model_options,
            index=current_fast_idx,
            key="fast_model_select",
            label_visibility="collapsed"
        )

    # Custom display name inputs
    st.markdown("---")
    st.markdown("**📝 Custom Display Names** (optional)")
    col1, col2 = st.columns(2)

    reasoning_model_info = model_id_map.get(new_reasoning)
    fast_model_info = model_id_map.get(new_fast)

    with col1:
        default_reasoning_name = f"{reasoning_model_info.name} (Reasoning)" if reasoning_model_info else ""
        reasoning_display_name = st.text_input(
            "Reasoning model display name:",
            value=reasoning.display_name if reasoning.model_id == reasoning_model_info.id else default_reasoning_name,
            key="reasoning_display_name"
        )

    with col2:
        default_fast_name = f"{fast_model_info.name} (Fast)" if fast_model_info else ""
        fast_display_name = st.text_input(
            "Fast model display name:",
            value=fast.display_name if fast.model_id == fast_model_info.id else default_fast_name,
            key="fast_display_name"
        )

    st.divider()

    # Save button
    col1, col2, col3 = st.columns([2, 2, 1])

    with col1:
        if st.button("💾 Save Configuration", type="primary", use_container_width=True):
            # Get selected models
            reasoning_model = model_id_map.get(new_reasoning)
            fast_model = model_id_map.get(new_fast)

            if reasoning_model and fast_model:
                # Update configuration
                model_config.set_reasoning_model(
                    model_id=reasoning_model.id,
                    backend="ollama",
                    display_name=reasoning_display_name or f"{reasoning_model.name} (Reasoning)"
                )
                model_config.set_fast_model(
                    model_id=fast_model.id,
                    backend="ollama",
                    display_name=fast_display_name or f"{fast_model.name} (Fast)"
                )

                # Reload GLM system config and clear model cache
                glm_system.reload_config()

                st.success("✅ Configuration saved! Model selection updated.")
                st.rerun()
            else:
                st.error("Please select valid models")

    with col2:
        if st.button("🔄 Reset to Defaults", use_container_width=True):
            # Reset to default configuration
            model_config.set_reasoning_model(
                model_id="deepseek-r1:32b",
                backend="ollama",
                display_name="DeepSeek-R1:32B (Reasoning)"
            )
            model_config.set_fast_model(
                model_id="qwen2.5:32b",
                backend="ollama",
                display_name="Qwen2.5:32B (Fast)"
            )
            glm_system.reload_config()
            st.success("✅ Reset to default configuration")
            st.rerun()

    with col3:
        if st.button("🧪 Test", use_container_width=True):
            test_model_connection(glm_system)

    # Help section
    st.divider()
    with st.expander("ℹ️ Help & Tips"):
        st.markdown("""
        ### Model Roles

        **Reasoning Model** - Used for:
        - Complex planning and architecture decisions
        - Deep analysis and debugging
        - Main chat conversations
        - Detailed code generation

        **Fast Model** - Used for:
        - Quick summarization
        - Generating titles
        - Agent meta updates
        - Simple queries

        ### Adding New Models

        To add new models to Ollama:
        ```bash
        ollama pull <model-name>
        ```

        Common models:
        - `deepseek-r1:32b` - Deep reasoning with <think> tags
        - `qwen2.5:32b` - Fast and efficient
        - `llama3.1:70b` - Large general purpose
        - `codellama:34b` - Code focused

        ### Tips

        - Use larger models for reasoning (better quality)
        - Use smaller/faster models for quick tasks
        - Test connections after changing models
        - Restart the app if models don't load properly
        """)


def scan_available_models(backend_manager) -> Dict[str, List[ModelInfo]]:
    """Scan all backends for available models."""
    all_models = {}

    # Scan Ollama
    ollama_backend = backend_manager.get_backend("ollama")
    if ollama_backend:
        all_models["ollama"] = ollama_backend.list_models()

    # Future: scan other backends
    # huggingface_backend = backend_manager.get_backend("huggingface")
    # if huggingface_backend:
    #     all_models["huggingface"] = huggingface_backend.list_models()

    return all_models


def test_model_connection(glm_system):
    """Test connection to configured models."""
    with st.spinner("Testing model connections..."):
        results = glm_system.check_model_availability()

    for model_name, status in results.items():
        if "✅" in status:
            st.success(f"{status} - {model_name}")
        elif "❌" in status:
            st.error(f"{status} - {model_name}")
        else:
            st.warning(f"{status} - {model_name}")
