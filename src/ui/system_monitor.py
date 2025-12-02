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

    def get_hrm_status(self, glm_system) -> Dict[str, Any]:
        """Get HRM wrapper status."""
        try:
            if hasattr(glm_system, 'hrm_wrapper') and glm_system.hrm_wrapper:
                hrm = glm_system.hrm_wrapper
                return {
                    "status": "ready",
                    "device": getattr(hrm, 'device', 'unknown'),
                    "model_loaded": getattr(hrm, 'model_loaded', False),
                    "caching_enabled": getattr(hrm, 'enable_caching', False),
                    "cache_size": len(getattr(hrm, '_decomposition_cache', {})),
                }
            return {"status": "not_initialized"}
        except Exception as e:
            return {"status": "error", "message": str(e)}

    def get_model_status(self, glm_system) -> Dict[str, Any]:
        """Get loaded model instances status."""
        try:
            loaded = list(glm_system._model_instances.keys()) if hasattr(glm_system, '_model_instances') else []
            available = list(glm_system.models.keys()) if hasattr(glm_system, 'models') else []
            return {
                "loaded_count": len(loaded),
                "available_count": len(available),
                "loaded_models": loaded,
                "available_models": available,
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

    # HRM Status
    with col3:
        with st.container():
            hrm_status = monitor.get_hrm_status(glm_system)
            if hrm_status["status"] == "ready":
                device = hrm_status.get("device", "cpu").upper()
                if device == "MPS":
                    st.success("**HRM**")
                    st.metric("Device", "MPS")
                    st.caption("M-series acceleration")
                elif device == "CUDA":
                    st.success("**HRM**")
                    st.metric("Device", "CUDA")
                    st.caption("GPU acceleration")
                else:
                    st.info("**HRM**")
                    st.metric("Device", "CPU")
                    st.caption("Standard mode")

                if hrm_status.get("caching_enabled"):
                    st.caption(f"Cache: {hrm_status.get('cache_size', 0)} entries")
            else:
                st.warning("**HRM**")
                st.metric("Status", "Pattern-based")
                st.caption("Using fallback routing")

    # Models Status
    with col4:
        with st.container():
            model_status = monitor.get_model_status(glm_system)
            loaded = model_status.get("loaded_count", 0)
            available = model_status.get("available_count", 0)

            if loaded > 0:
                st.success("**Models**")
            else:
                st.info("**Models**")

            st.metric("Loaded", f"{loaded}/{available}")
            st.caption("Lazy loading enabled")

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
                st.write(f"**Available Models:** {ollama_status['models_available']}")

                with st.expander("Show loaded models"):
                    for model in ollama_status.get("models", []):
                        st.code(model)
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
        st.subheader("🤖 Available Models")

        model_info = {
            "DeepSeek-R1 (Reasoning)": {
                "ollama_name": "deepseek-r1:70b",
                "purpose": "Complex reasoning, debugging, architecture",
                "params": "70B",
                "specialty": "Chain-of-thought reasoning"
            },
            "Qwen2.5-Coder (Implementation)": {
                "ollama_name": "qwen2.5-coder:32b",
                "purpose": "Code implementation, FAUST/C++",
                "params": "32B",
                "specialty": "Code generation"
            },
            "Qwen2.5 (Math/Physics)": {
                "ollama_name": "qwen2.5:32b",
                "purpose": "Mathematical computations, DSP theory",
                "params": "32B",
                "specialty": "Mathematical reasoning"
            },
        }

        loaded_models = model_status.get("loaded_models", [])

        for display_name, info in model_info.items():
            is_loaded = display_name in loaded_models

            with st.container():
                cols = st.columns([3, 1, 1])
                with cols[0]:
                    status_icon = "🟢" if is_loaded else "⚪"
                    st.write(f"{status_icon} **{display_name}**")
                    st.caption(f"{info['purpose']}")
                with cols[1]:
                    st.write(f"`{info['params']}`")
                with cols[2]:
                    st.write("Loaded" if is_loaded else "Not loaded")
                st.divider()

        st.info("Models are loaded on-demand when first used to save memory.")

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
