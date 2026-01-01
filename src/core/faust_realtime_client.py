"""
FAUST Realtime MCP Client for Streamlit Integration

Connects to faust_realtime_server.py MCP server to compile and run
FAUST DSP code in real-time with WebAudio backend.
"""

import json
from typing import Dict, Any, Optional, List
from dataclasses import dataclass, field

# Check for MCP library
try:
    from mcp.client.sse import sse_client
    from mcp.client.session import ClientSession
    MCP_AVAILABLE = True
except ImportError:
    MCP_AVAILABLE = False

# Check for anyio
try:
    import anyio
    ANYIO_AVAILABLE = True
except ImportError:
    ANYIO_AVAILABLE = False


@dataclass
class FaustRealtimeResult:
    """Result from FAUST realtime operations."""
    success: bool
    message: str = ""
    params: List[Dict[str, Any]] = field(default_factory=list)
    error: str = ""

    def to_dict(self) -> Dict[str, Any]:
        return {
            "success": self.success,
            "message": self.message,
            "params": self.params,
            "error": self.error,
        }


class FaustRealtimeClient:
    """Client for faust_realtime_server.py MCP server."""

    def __init__(self, server_url: str = "http://127.0.0.1:8000/sse"):
        self.server_url = server_url

    async def compile_and_start_async(
        self,
        faust_code: str,
        name: str = "dsp",
        latency_hint: str = "interactive"
    ) -> FaustRealtimeResult:
        """
        Compile FAUST code and start real-time playback.

        Args:
            faust_code: The FAUST DSP source code
            name: Optional name for the DSP
            latency_hint: Latency hint ('interactive', 'balanced', 'playback')

        Returns:
            FaustRealtimeResult with success status and params
        """
        if not MCP_AVAILABLE:
            return FaustRealtimeResult(
                success=False,
                error="MCP library not installed. Run: pip install mcp"
            )

        try:
            async with sse_client(self.server_url) as (read, write):
                async with ClientSession(read, write) as session:
                    await session.initialize()

                    result = await session.call_tool(
                        "compile_and_start",
                        {
                            "faust_code": faust_code,
                            "name": name,
                            "latency_hint": latency_hint
                        }
                    )

                    # Parse result
                    if hasattr(result, 'content') and result.content:
                        text = result.content[0].text
                        if text.startswith("Error") or "error" in text.lower():
                            return FaustRealtimeResult(success=False, error=text)

                        try:
                            data = json.loads(text)
                            return FaustRealtimeResult(
                                success=True,
                                message=data.get("message", "DSP started"),
                                params=data.get("params", [])
                            )
                        except json.JSONDecodeError:
                            # Plain text response
                            return FaustRealtimeResult(
                                success=True,
                                message=text
                            )

                    return FaustRealtimeResult(
                        success=False,
                        error="Empty response from server"
                    )

        except Exception as e:
            error_msg = str(e)
            if "Connection refused" in error_msg:
                error_msg = "Cannot connect to realtime server. Is it running on port 8000?"
            return FaustRealtimeResult(success=False, error=error_msg)

    async def stop_async(self) -> FaustRealtimeResult:
        """Stop the currently running DSP."""
        if not MCP_AVAILABLE:
            return FaustRealtimeResult(
                success=False,
                error="MCP library not installed"
            )

        try:
            async with sse_client(self.server_url) as (read, write):
                async with ClientSession(read, write) as session:
                    await session.initialize()

                    result = await session.call_tool("stop", {})

                    if hasattr(result, 'content') and result.content:
                        text = result.content[0].text
                        return FaustRealtimeResult(
                            success=True,
                            message=text
                        )

                    return FaustRealtimeResult(
                        success=True,
                        message="DSP stopped"
                    )

        except Exception as e:
            return FaustRealtimeResult(success=False, error=str(e))

    async def get_params_async(self) -> FaustRealtimeResult:
        """Get parameters from the running DSP."""
        if not MCP_AVAILABLE:
            return FaustRealtimeResult(
                success=False,
                error="MCP library not installed"
            )

        try:
            async with sse_client(self.server_url) as (read, write):
                async with ClientSession(read, write) as session:
                    await session.initialize()

                    result = await session.call_tool("get_params", {})

                    if hasattr(result, 'content') and result.content:
                        text = result.content[0].text
                        try:
                            params = json.loads(text)
                            return FaustRealtimeResult(
                                success=True,
                                params=params if isinstance(params, list) else []
                            )
                        except json.JSONDecodeError:
                            return FaustRealtimeResult(
                                success=False,
                                error=f"Invalid params response: {text}"
                            )

                    return FaustRealtimeResult(
                        success=False,
                        error="No params returned"
                    )

        except Exception as e:
            return FaustRealtimeResult(success=False, error=str(e))

    async def set_param_async(self, path: str, value: float) -> FaustRealtimeResult:
        """Set a parameter value on the running DSP."""
        if not MCP_AVAILABLE:
            return FaustRealtimeResult(
                success=False,
                error="MCP library not installed"
            )

        try:
            async with sse_client(self.server_url) as (read, write):
                async with ClientSession(read, write) as session:
                    await session.initialize()

                    result = await session.call_tool(
                        "set_param",
                        {"path": path, "value": value}
                    )

                    if hasattr(result, 'content') and result.content:
                        return FaustRealtimeResult(
                            success=True,
                            message=result.content[0].text
                        )

                    return FaustRealtimeResult(success=True)

        except Exception as e:
            return FaustRealtimeResult(success=False, error=str(e))

    async def check_syntax_async(
        self,
        faust_code: str,
        name: str = "faust-check"
    ) -> FaustRealtimeResult:
        """
        Check FAUST code syntax without starting audio.

        Args:
            faust_code: The FAUST DSP source code
            name: Optional name for the check

        Returns:
            FaustRealtimeResult with success status and params if valid
        """
        if not MCP_AVAILABLE:
            return FaustRealtimeResult(
                success=False,
                error="MCP library not installed. Run: pip install mcp"
            )

        try:
            async with sse_client(self.server_url) as (read, write):
                async with ClientSession(read, write) as session:
                    await session.initialize()

                    result = await session.call_tool(
                        "check_syntax",
                        {
                            "faust_code": faust_code,
                            "name": name
                        }
                    )

                    # Parse result
                    if hasattr(result, 'content') and result.content:
                        text = result.content[0].text
                        if text.startswith("Error") or "error" in text.lower():
                            return FaustRealtimeResult(success=False, error=text)

                        try:
                            data = json.loads(text)
                            return FaustRealtimeResult(
                                success=True,
                                message=data.get("message", "Syntax OK"),
                                params=data.get("params", [])
                            )
                        except json.JSONDecodeError:
                            # Plain text response
                            return FaustRealtimeResult(
                                success=True,
                                message=text
                            )

                    return FaustRealtimeResult(
                        success=False,
                        error="Empty response from server"
                    )

        except Exception as e:
            error_msg = str(e)
            if "Connection refused" in error_msg:
                error_msg = "Cannot connect to realtime server. Is it running on port 8000?"
            return FaustRealtimeResult(success=False, error=error_msg)


# Synchronous wrappers

def run_faust(
    faust_code: str,
    server_url: str = "http://127.0.0.1:8000/sse",
    name: str = "dsp"
) -> FaustRealtimeResult:
    """
    Compile and start FAUST code in real-time.

    Args:
        faust_code: FAUST DSP source code
        server_url: Realtime server URL
        name: DSP name

    Returns:
        FaustRealtimeResult with success status
    """
    if not ANYIO_AVAILABLE:
        return FaustRealtimeResult(
            success=False,
            error="anyio library not installed. Run: pip install anyio"
        )

    async def _run():
        client = FaustRealtimeClient(server_url)
        return await client.compile_and_start_async(faust_code, name)

    return anyio.run(_run)


def stop_faust(server_url: str = "http://127.0.0.1:8000/sse") -> FaustRealtimeResult:
    """Stop the currently running DSP."""
    if not ANYIO_AVAILABLE:
        return FaustRealtimeResult(
            success=False,
            error="anyio library not installed"
        )

    async def _stop():
        client = FaustRealtimeClient(server_url)
        return await client.stop_async()

    return anyio.run(_stop)


def get_faust_params(server_url: str = "http://127.0.0.1:8000/sse") -> FaustRealtimeResult:
    """Get parameters from running DSP."""
    if not ANYIO_AVAILABLE:
        return FaustRealtimeResult(
            success=False,
            error="anyio library not installed"
        )

    async def _get():
        client = FaustRealtimeClient(server_url)
        return await client.get_params_async()

    return anyio.run(_get)


def set_faust_param(
    path: str,
    value: float,
    server_url: str = "http://127.0.0.1:8000/sse"
) -> FaustRealtimeResult:
    """Set a parameter on the running DSP."""
    if not ANYIO_AVAILABLE:
        return FaustRealtimeResult(
            success=False,
            error="anyio library not installed"
        )

    async def _set():
        client = FaustRealtimeClient(server_url)
        return await client.set_param_async(path, value)

    return anyio.run(_set)


def check_faust_syntax_realtime(
    faust_code: str,
    server_url: str = "http://127.0.0.1:8000/sse",
    name: str = "faust-check"
) -> FaustRealtimeResult:
    """
    Check FAUST code syntax via realtime server (no local faust needed).

    Args:
        faust_code: FAUST DSP source code
        server_url: Realtime server URL
        name: Check name

    Returns:
        FaustRealtimeResult with success status and params if valid
    """
    if not ANYIO_AVAILABLE:
        return FaustRealtimeResult(
            success=False,
            error="anyio library not installed. Run: pip install anyio"
        )

    async def _check():
        client = FaustRealtimeClient(server_url)
        return await client.check_syntax_async(faust_code, name)

    return anyio.run(_check)


def check_realtime_server(server_url: str = "http://127.0.0.1:8000/sse") -> bool:
    """Check if realtime server is running."""
    if not MCP_AVAILABLE or not ANYIO_AVAILABLE:
        return False

    async def _check():
        try:
            async with sse_client(server_url) as (read, write):
                async with ClientSession(read, write) as session:
                    await session.initialize()
                    return True
        except Exception:
            return False

    try:
        return anyio.run(_check)
    except Exception:
        return False


# Test code
if __name__ == "__main__":
    test_dsp = """
import("stdfaust.lib");
process = os.osc(440) * 0.3;
"""

    print("Checking realtime server...")
    if check_realtime_server():
        print("Server is running!")
        print("\nStarting test DSP...")
        result = run_faust(test_dsp)
        if result.success:
            print(f"Started: {result.message}")
            print(f"Params: {result.params}")
        else:
            print(f"Error: {result.error}")
    else:
        print("Realtime server is not running on :8000")
