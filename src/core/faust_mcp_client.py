"""
FAUST MCP Client for Streamlit Integration

Connects to faust-mcp SSE server to compile and analyze FAUST DSP code.
Uses the MCP protocol for proper communication.
"""

import json
import subprocess
import importlib.util
from typing import Dict, Any, Optional
from dataclasses import dataclass, field

# Check for MCP library
try:
    from mcp.client.sse import sse_client
    from mcp.client.session import ClientSession
    MCP_AVAILABLE = True
except ImportError:
    MCP_AVAILABLE = False
    sse_client = None  # type: ignore
    ClientSession = None  # type: ignore

# Check for anyio
try:
    import anyio
    ANYIO_AVAILABLE = True
except ImportError:
    ANYIO_AVAILABLE = False
    anyio = None  # type: ignore


@dataclass
class FaustAnalysisResult:
    """Result from FAUST compilation and analysis."""
    status: str
    max_amplitude: float = 0.0
    rms: float = 0.0
    is_silent: bool = True
    waveform_ascii: str = ""
    num_outputs: int = 0
    channels: list = field(default_factory=list)
    features: Dict[str, Any] = field(default_factory=dict)
    error: str = ""
    dawdreamer_info: Dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary for serialization."""
        return {
            "status": self.status,
            "max_amplitude": self.max_amplitude,
            "rms": self.rms,
            "is_silent": self.is_silent,
            "waveform_ascii": self.waveform_ascii,
            "num_outputs": self.num_outputs,
            "channels": self.channels,
            "features": self.features,
            "error": self.error,
            "dawdreamer_info": self.dawdreamer_info,
        }

    def get_summary(self) -> str:
        """Get a human-readable summary of the analysis."""
        if self.status == "error":
            return f"Analysis failed: {self.error}"

        lines = [
            f"Status: {self.status}",
            f"Outputs: {self.num_outputs} channel(s)",
            f"Max Amplitude: {self.max_amplitude:.4f}",
            f"RMS: {self.rms:.4f}",
            f"Silent: {'Yes' if self.is_silent else 'No'}",
        ]

        if self.waveform_ascii:
            lines.append(f"Waveform: {self.waveform_ascii}")

        if self.features:
            if self.features.get("spectral_available"):
                lines.extend([
                    f"Spectral Centroid: {self.features.get('spectral_centroid', 0):.2f} Hz",
                    f"Spectral Bandwidth: {self.features.get('spectral_bandwidth', 0):.2f} Hz",
                    f"Spectral Flatness: {self.features.get('spectral_flatness', 0):.4f}",
                ])
            if self.features.get("crest_factor"):
                lines.append(f"Crest Factor: {self.features.get('crest_factor', 0):.2f}")
            if self.features.get("dc_offset"):
                lines.append(f"DC Offset: {self.features.get('dc_offset', 0):.6f}")

        return "\n".join(lines)


class FaustMCPClient:
    """Client for faust-mcp SSE server using MCP protocol."""

    def __init__(self, server_url: str = "http://127.0.0.1:8765/sse"):
        self.server_url = server_url

    async def compile_and_analyze_async(self, faust_code: str) -> FaustAnalysisResult:
        """
        Compile FAUST code and return audio/spectral analysis.

        Args:
            faust_code: The FAUST DSP source code

        Returns:
            FaustAnalysisResult with analysis metrics
        """
        if not MCP_AVAILABLE:
            return FaustAnalysisResult(
                status="error",
                error="MCP library not installed. Run: pip install mcp"
            )

        try:
            async with sse_client(self.server_url) as (read, write):  # type: ignore[misc]
                async with ClientSession(read, write) as session:  # type: ignore[misc]
                    await session.initialize()

                    result = await session.call_tool(
                        "compile_and_analyze",
                        {"faust_code": faust_code}
                    )

                    # Parse the result - always use content[0].text as it contains the JSON
                    data = None
                    if hasattr(result, 'content') and result.content and len(result.content) > 0:
                        text = getattr(result.content[0], 'text', '')
                        if text.startswith("Error") or text.startswith("System Error"):
                            return FaustAnalysisResult(status="error", error=text)
                        data = json.loads(text)

                    if data is None:
                        return FaustAnalysisResult(
                            status="error",
                            error="Empty response from server"
                        )

                    return FaustAnalysisResult(
                        status=data.get("status", "unknown"),
                        max_amplitude=data.get("max_amplitude", 0.0),
                        rms=data.get("rms", 0.0),
                        is_silent=data.get("is_silent", True),
                        waveform_ascii=data.get("waveform_ascii", ""),
                        num_outputs=data.get("num_outputs", 0),
                        channels=data.get("channels", []),
                        features=data.get("features", {}),
                        dawdreamer_info=data.get("dawdreamer", {}),
                    )

        except Exception as e:
            error_msg = str(e)
            if "Connection refused" in error_msg:
                error_msg = "Cannot connect to faust-mcp server. Is it running on port 8765?"
            return FaustAnalysisResult(status="error", error=error_msg)


def analyze_faust_code(
    faust_code: str,
    server_url: str = "http://127.0.0.1:8765/sse"
) -> FaustAnalysisResult:
    """
    Synchronous wrapper for FAUST analysis.

    Args:
        faust_code: FAUST DSP source code
        server_url: faust-mcp server URL

    Returns:
        FaustAnalysisResult with analysis metrics
    """
    if not ANYIO_AVAILABLE:
        return FaustAnalysisResult(
            status="error",
            error="anyio library not installed. Run: pip install anyio"
        )

    async def _run():
        client = FaustMCPClient(server_url)
        return await client.compile_and_analyze_async(faust_code)

    return anyio.run(_run)  # type: ignore[union-attr]


def check_faust_server(server_url: str = "http://127.0.0.1:8765/sse") -> bool:
    """
    Check if faust-mcp server is running.

    Attempts a simple connection to verify the server is available.
    """
    if not MCP_AVAILABLE or not ANYIO_AVAILABLE:
        return False

    async def _check():
        try:
            async with sse_client(server_url) as (read, write):  # type: ignore[misc]
                async with ClientSession(read, write) as session:  # type: ignore[misc]
                    await session.initialize()
                    return True
        except Exception:
            return False

    try:
        return anyio.run(_check)  # type: ignore[union-attr]
    except Exception:
        return False


def detect_faust_backend() -> str:
    """
    Detect which faust-mcp backend is available.

    Returns:
        'cpp' if Faust CLI and g++ available
        'dawdreamer' if DawDreamer installed
        'none' if neither available
    """
    # Check for Faust CLI + g++
    try:
        subprocess.run(
            ['faust', '--version'],
            capture_output=True,
            timeout=5,
            check=True
        )
        subprocess.run(
            ['g++', '--version'],
            capture_output=True,
            timeout=5,
            check=True
        )
        return 'cpp'
    except (subprocess.SubprocessError, FileNotFoundError):
        pass

    # Check for DawDreamer
    if importlib.util.find_spec('dawDreamer') or importlib.util.find_spec('dawdreamer'):
        return 'dawdreamer'

    return 'none'


def get_faust_version() -> Optional[str]:
    """Get the installed Faust compiler version."""
    try:
        result = subprocess.run(
            ['faust', '--version'],
            capture_output=True,
            text=True,
            timeout=5
        )
        if result.returncode == 0:
            # Parse version from output like "FAUST Version 2.81.10"
            lines = result.stdout.strip().split('\n')
            if lines:
                return lines[0]
        return None
    except (subprocess.SubprocessError, FileNotFoundError):
        return None


def check_faust_syntax(faust_code: str) -> Dict[str, Any]:
    """
    Fast syntax check using faust compiler directly.

    Args:
        faust_code: FAUST DSP source code

    Returns:
        Dict with 'success' bool and 'errors' string if failed
    """
    import tempfile
    import os

    # Write code to temp file
    try:
        with tempfile.NamedTemporaryFile(
            mode='w',
            suffix='.dsp',
            delete=False,
            encoding='utf-8'
        ) as f:
            f.write(faust_code)
            temp_path = f.name
    except Exception as e:
        return {"success": False, "errors": f"Failed to create temp file: {e}"}

    try:
        # Run faust with null output to just check syntax
        result = subprocess.run(
            ['faust', '-o', '/dev/null', temp_path],
            capture_output=True,
            text=True,
            timeout=10
        )

        if result.returncode == 0:
            return {"success": True, "errors": None}
        else:
            # Extract meaningful error message
            error_text = result.stderr.strip()
            # Replace temp path with more readable name
            error_text = error_text.replace(temp_path, "<code>")
            return {"success": False, "errors": error_text}

    except subprocess.TimeoutExpired:
        return {"success": False, "errors": "Syntax check timed out (10s)"}
    except FileNotFoundError:
        return {"success": False, "errors": "Faust compiler not found. Is it installed?"}
    except Exception as e:
        return {"success": False, "errors": f"Syntax check failed: {e}"}
    finally:
        # Clean up temp file
        try:
            os.unlink(temp_path)
        except Exception:
            pass


# Simple test code
if __name__ == "__main__":
    # Test code
    test_dsp = """
import("stdfaust.lib");
process = os.osc(440);
"""

    print("Checking faust-mcp server...")
    if check_faust_server():
        print("Server is running!")
        print("\nAnalyzing test DSP code...")
        result = analyze_faust_code(test_dsp)
        print(result.get_summary())
    else:
        print("Server is not running.")
        print(f"\nDetected backend: {detect_faust_backend()}")
        print(f"Faust version: {get_faust_version()}")
