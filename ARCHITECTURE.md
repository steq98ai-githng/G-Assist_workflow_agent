# 🏛️ System Workflow Agent Architecture

This document describes the high-level architecture of the **System Workflow Agent** v4.0.4, a specialized plugin for NVIDIA Project G-Assist.

## 🏗️ System Overview

The System Workflow Agent is designed as a modular, agentic bridge between the NVIDIA G-Assist platform and various developer tools (via the Model Context Protocol - MCP). It uses Google Gemini 2.0 as its "reasoning engine" to understand complex system-level requests.

### Core Components

```mermaid
graph TD
    GA[NVIDIA G-Assist App] <-->|Protocol V2 / JSON-RPC| P[plugin.py]
    P <--> PR[core/plugin_runtime.py]

    subgraph Core Logic
        PR --> IR[core/intent_router.py]
        PR --> EB[core/event_bus.py]
        PR --> CL[config/loader.py]
    end

    subgraph Capabilities
        IR --> Gemini[Google Gemini 2.0 AI]
        IR --> VD[vision/diagnostic.py]
        IR --> MCPM[mcp/client.py & registry.py]
    end

    subgraph External Tools
        MCPM <--> MCPS[MCP Servers / e.g. GitKraken]
    end

    subgraph SDK
        PR --> SDK[libs/gassist_sdk/]
    end
```

## 📦 Module Descriptions

### 1. Entry Point & Runtime (`plugin.py`, `core/`)
- **`plugin.py`**: The standard entry point required by G-Assist. It initializes the `PluginRuntime` and defines the main command handlers.
- **`core/plugin_runtime.py`**: The central orchestrator. It manages the lifecycle of all services (config, registry, MCP, intent routing) and ensures no global states are used, facilitating stability and testing.
- **`core/intent_router.py`**: The "brain" of the agent. It manages the conversation with Gemini, performs function calling, and coordinates between vision diagnostics and MCP tools.
- **`core/event_bus.py`**: Provides a simple pub/sub mechanism for decoupled internal communication.

### 2. Tooling & MCP (`mcp/`)
- **mcp/client.py**: Implements the MCPManager which manages multiple MCP clients (Stdio) and handles tool routing.
- **`mcp/registry.py`**: Handles dynamic discovery of tools from MCP servers and registers them as G-Assist functions so the G-Assist platform (and Gemini) "sees" them.

### 3. Multi-modal Capabilities (`vision/`)
- **`vision/diagnostic.py`**: Provides system snapshot capabilities, allowing the AI to "see" what is happening on the screen for performance or error diagnostics.

### 4. SDK Layer (`libs/gassist_sdk/`)
A local copy of the G-Assist Plugin SDK which handles:
- **Protocol**: Implementation of the length-prefixed JSON-RPC 2.0 protocol over `stdin`/`stdout`.
- **Types**: Shared data structures for Messages, Context, and Command Results.
- **MCP**: Abstractions for MCP Clients and Transports.

## 🔄 Data Flow: A Query Lifecycle

1.  **Request**: G-Assist sends a `system_workflow_agent` command via `stdin`.
2.  **Dispatch**: `plugin.py` receives the request and calls `IntentRouter.process_query`.
3.  **Reasoning**:
    - `IntentRouter` gathers available tools (local functions + MCP tools).
    - It sends the user query and tool definitions to **Gemini 2.0**.
4.  **Execution**:
    - Gemini returns a "Function Call" request.
    - `IntentRouter` executes the tool (e.g., calling an MCP server to "list git commits").
    - The result is sent back to Gemini for final summarization.
5.  **Response**: The final answer is streamed back to the user interface in G-Assist.

## 📡 Communication Protocols

### NVIDIA G-Assist Protocol V2
The plugin communicates with the host NVIDIA app using a custom JSON-RPC 2.0 protocol.
- **Transport**: Standard I/O (`stdin`/`stdout`).
- **Framing**: Each JSON message is prefixed with a 4-byte big-endian unsigned integer indicating the payload length.

### Model Context Protocol (MCP)
The agent acts as an **MCP Client**, connecting to **MCP Servers**.
- Support for stdio (subprocesses) transport.
- Dynamic tool discovery allows the agent to expand its capabilities without code changes.

## ⚙️ Configuration (`config/`)
- Uses internal validation logic in config/loader.py for configuration integrity.
- Supports dynamic merging of default settings with user-defined `config.json`.
- Gemini API keys are loaded from environment variables or `gemini-api.key` files.
