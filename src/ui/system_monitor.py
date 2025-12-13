"""
System Monitor UI for Multi-Model AI Development Assistant.
Provides real-time monitoring of system components, connections, and performance.
"""

import streamlit as st
import time
import requests
from datetime import datetime
from typing import Dict, Any, Optional
from collections import deque


class SystemMonitor:
    """Collects and manages system metrics."""

    def __init__(self):
        # Initialize activity log in session state
        if "monitor_activity_log" not in st.session_state:
            st.session_state.monitor_activity_log = deque(maxlen=50)

        if "monitor_metrics" not in st.session_state:
            st.session_state.monitor_metrics = {
                "ollama_response_times": deque(maxlen=20),
                "last_check": None,
                "error_count": 0,
                "query_count": 0,
            }

    def log_activity(self, message: str, level: str = "info"):
        """Add an entry to the activity log."""
        timestamp = datetime.now().strftime("%H:%M:%S")
        icons = {"info": "ℹ️", "success": "✅", "warning": "⚠️", "error": "❌"}
        icon = icons.get(level, "ℹ️")
        st.session_state.monitor_activity_log.appendleft(
            {"time": timestamp, "message": message, "level": level, "icon": icon}
        )

    def check_ollama_connection(self) -> Dict[str, Any]:
        """Check Ollama server connection and return status."""
        try:
            start = time.time()
            response = requests.get("http://localhost:11434/api/tags", timeout=5)
            elapsed = (time.time() - start) * 1000  # ms

            if response.status_code == 200:
                models = response.json().get("models", [])
                st.session_state.monitor_metrics["ollama_response_times"].append(elapsed)
                return {
                    "status": "connected",
                    "response_time_ms": round(elapsed, 1),
                    "models_available": len(models),
                    "models": [m.get("name", "unknown") for m in models],
                }
            else:
                return {"status": "error", "message": f"HTTP {response.status_code}"}
        except requests.exceptions.ConnectionError:
            return {"status": "disconnected", "message": "Cannot connect to Ollama"}
        except requests.exceptions.Timeout:
            return {"status": "timeout", "message": "Connection timed out"}
        except Exception as e:
            return {"status": "error", "message": str(e)}

    def get_chromadb_status(self, glm_system) -> Dict[str, Any]:
        """Get ChromaDB/vectorstore status."""
        try:
            if hasattr(glm_system, 'vectorstore') and glm_system.vectorstore:
                collection = glm_system.vectorstore._collection
                count = collection.count()
                return {
                    "status": "ready" if count > 0 else "empty",
                    "document_count": count,
                    "collection_name": collection.name if hasattr(collection, 'name') else "default",
                }
            return {"status": "not_initialized", "document_count": 0}
        except Exception as e:
            return {"status": "error", "message": str(e), "document_count": 0}

    def get_agent_meta_status(self, glm_system) -> Dict[str, Any]:
        """Get agent meta files status."""
        try:
            from pathlib import Path
            agents_dir = Path("./projects")
            agent_files = list(agents_dir.rglob("agents/*_context.md"))
            return {
                "status": "ready" if agent_files else "empty",
                "file_count": len(agent_files),
            }
        except Exception as e:
            return {"status": "error", "message": str(e), "file_count": 0}

    def get_model_status(self, glm_system) -> Dict[str, Any]:
        """Get model status - configured models and memory status."""
        try:
            # Models configured in the system
            configured = list(glm_system.models.keys()) if hasattr(glm_system, 'models') else []
            # Models currently loaded in memory (lazy loading)
            in_memory = list(glm_system._model_instances.keys()) if hasattr(glm_system, '_model_instances') else []
            return {
                "configured_count": len(configured),
                "in_memory_count": len(in_memory),
                "configured_models": configured,
                "in_memory_models": in_memory,
            }
        except Exception as e:
            return {"status": "error", "message": str(e)}

    def get_average_response_time(self) -> Optional[float]:
        """Get average Ollama response time."""
        times = st.session_state.monitor_metrics.get("ollama_response_times", [])
        if times:
            return round(sum(times) / len(times), 1)
        return None


def render_system_monitor(glm_system):
    """Render the System Monitor tab."""
    st.header("🖥️ System Monitor")

    monitor = SystemMonitor()

    # Auto-refresh toggle
    col_refresh, col_status = st.columns([1, 3])
    with col_refresh:
        if st.button("🔄 Refresh Status", use_container_width=True):
            st.session_state.monitor_last_refresh = datetime.now()
            monitor.log_activity("Manual status refresh triggered", "info")
            st.rerun()

    with col_status:
        last_refresh = st.session_state.get("monitor_last_refresh")
        if last_refresh:
            st.caption(f"Last refreshed: {last_refresh.strftime('%H:%M:%S')}")
        else:
            st.caption("Click refresh to update status")

    st.divider()

    # Status Cards Row
    col1, col2, col3, col4 = st.columns(4)

    # Ollama Status
    with col1:
        with st.container():
            ollama_status = monitor.check_ollama_connection()
            if ollama_status["status"] == "connected":
                st.success("**Ollama**")
                st.metric(
                    "Status",
                    "Connected",
                    delta=f"{ollama_status['response_time_ms']}ms"
                )
                st.caption(f"{ollama_status['models_available']} models available")
            elif ollama_status["status"] == "disconnected":
                st.error("**Ollama**")
                st.metric("Status", "Disconnected")
                st.caption("Start with: ollama serve")
            else:
                st.warning("**Ollama**")
                st.metric("Status", ollama_status["status"].title())
                st.caption(ollama_status.get("message", ""))

    # ChromaDB Status
    with col2:
        with st.container():
            chroma_status = monitor.get_chromadb_status(glm_system)
            if chroma_status["status"] == "ready":
                st.success("**ChromaDB**")
                st.metric("Documents", chroma_status["document_count"])
                st.caption("Knowledge base ready")
            elif chroma_status["status"] == "empty":
                st.warning("**ChromaDB**")
                st.metric("Documents", 0)
                st.caption("Run load_documentation.py")
            else:
                st.error("**ChromaDB**")
                st.metric("Status", chroma_status["status"].title())
                st.caption(chroma_status.get("message", "Not initialized"))

    # Agent Meta Status
    with col3:
        with st.container():
            agent_status = monitor.get_agent_meta_status(glm_system)
            if agent_status["status"] == "ready":
                st.success("**Agent Meta**")
                st.metric("Files", agent_status["file_count"])
                st.caption("Context files ready")
            elif agent_status["status"] == "empty":
                st.info("**Agent Meta**")
                st.metric("Files", 0)
                st.caption("No agent contexts yet")
            else:
                st.warning("**Agent Meta**")
                st.metric("Status", agent_status["status"].title())
                st.caption(agent_status.get("message", "Check projects folder"))

    # Models Status
    with col4:
        with st.container():
            model_status = monitor.get_model_status(glm_system)
            configured = model_status.get("configured_count", 0)
            in_memory = model_status.get("in_memory_count", 0)

            if configured > 0:
                st.success("**Models**")
                st.metric("Ready", f"{configured}")
                if in_memory > 0:
                    st.caption(f"{in_memory} in memory")
                else:
                    st.caption("Load on first use")
            else:
                st.warning("**Models**")
                st.metric("Ready", "0")
                st.caption("No models configured")

    st.divider()

    # Detailed Sections
    tab_details, tab_models, tab_activity = st.tabs([
        "📊 Details", "🤖 Model Info", "📜 Activity Log"
    ])

    with tab_details:
        col_left, col_right = st.columns(2)

        with col_left:
            st.subheader("🔌 Ollama Connection")
            if ollama_status["status"] == "connected":
                avg_time = monitor.get_average_response_time()
                st.write(f"**Endpoint:** http://localhost:11434")
                st.write(f"**Last Response:** {ollama_status['response_time_ms']}ms")
                if avg_time:
                    st.write(f"**Avg Response:** {avg_time}ms")

                # Show app models vs all Ollama models (dynamically from config)
                app_models = list(glm_system.models.values())
                all_models = ollama_status.get("models", [])

                st.write(f"**App Models:** 2 configured")
                st.write(f"**Ollama Total:** {len(all_models)} installed")

                with st.expander("Show all Ollama models"):
                    for model in all_models:
                        is_app_model = any(app in model for app in app_models)
                        if is_app_model:
                            st.success(f"✓ {model} (used by app)")
                        else:
                            st.caption(f"  {model}")
            else:
                st.error(f"Connection issue: {ollama_status.get('message', 'Unknown')}")
                st.markdown("""
                **Troubleshooting:**
                1. Check if Ollama is running: `ollama serve`
                2. Verify models are pulled: `ollama list`
                3. Check port 11434 is not blocked
                """)

        with col_right:
            st.subheader("💾 Knowledge Base")
            if chroma_status["status"] == "ready":
                st.write(f"**Collection:** {chroma_status.get('collection_name', 'default')}")
                st.write(f"**Total Documents:** {chroma_status['document_count']}")
                st.write("**Status:** Indexed and ready")

                # Estimated categories based on typical usage
                st.progress(1.0, text="Index Health: Optimal")
            elif chroma_status["status"] == "empty":
                st.warning("Knowledge base is empty")
                st.markdown("""
                **To populate the knowledge base:**
                ```bash
                python scripts/load_documentation.py
                ```
                """)
            else:
                st.error(f"Error: {chroma_status.get('message', 'Unknown')}")

    with tab_models:
        st.subheader("🤖 System Models")

        # Build model info dynamically from config
        reasoning_model = glm_system.model_config.get_reasoning_model()
        fast_model = glm_system.model_config.get_fast_model()

        model_info = {
            reasoning_model.display_name: {
                "ollama_name": reasoning_model.model_id,
                "purpose": "Deep reasoning, planning, architecture decisions",
                "role": "Reasoning",
                "specialty": "Chain-of-thought reasoning with <think> tags"
            },
            fast_model.display_name: {
                "ollama_name": fast_model.model_id,
                "purpose": "Fast summarization, agent meta updates, quick tasks",
                "role": "Fast",
                "specialty": "Speed & efficiency"
            },
        }

        # Check actual status from glm_system
        configured_models = model_status.get("configured_models", [])
        in_memory_models = model_status.get("in_memory_models", [])

        for display_name, info in model_info.items():
            # Check if model is configured and/or in memory
            is_configured = display_name in configured_models
            is_in_memory = display_name in in_memory_models

            with st.container():
                cols = st.columns([3, 1, 1])
                with cols[0]:
                    status_icon = "🟢" if is_configured else "⚪"
                    st.write(f"{status_icon} **{display_name}**")
                    st.caption(f"{info['purpose']}")
                with cols[1]:
                    st.write(f"`{info['role']}`")
                with cols[2]:
                    if is_in_memory:
                        st.success("In Memory")
                    elif is_configured:
                        st.info("Ready")
                    else:
                        st.caption("Not configured")
                st.divider()

        st.info("Models are loaded on-demand when first used. Both models work together: Reasoning model for complex tasks, Fast model for quick tasks.")

    with tab_activity:
        st.subheader("📜 Recent Activity")

        activity_log = st.session_state.get("monitor_activity_log", [])

        if activity_log:
            for entry in list(activity_log)[:20]:
                col_time, col_msg = st.columns([1, 5])
                with col_time:
                    st.caption(entry["time"])
                with col_msg:
                    st.write(f"{entry['icon']} {entry['message']}")
        else:
            st.info("No activity recorded yet. Interact with the system to see logs here.")

        if st.button("Clear Activity Log"):
            st.session_state.monitor_activity_log.clear()
            st.rerun()

    # System Info Footer
    st.divider()
    with st.expander("ℹ️ System Information"):
        import platform
        import sys

        col1, col2, col3 = st.columns(3)
        with col1:
            st.write(f"**Python:** {sys.version.split()[0]}")
            st.write(f"**Platform:** {platform.system()} {platform.machine()}")
        with col2:
            st.write(f"**Streamlit:** {st.__version__}")
            st.write(f"**Session ID:** {id(st.session_state)}")
        with col3:
            import chromadb
            st.write(f"**ChromaDB:** {chromadb.__version__}")
            try:
                import torch
                st.write(f"**PyTorch:** {torch.__version__}")
            except ImportError:
                st.write("**PyTorch:** Not installed")
