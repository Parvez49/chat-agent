# Multi-Agent System Architecture

## Overview

This framework implements a production-ready multi-agent system designed for solving complex real-world problems using local LLMs (Ollama).

## Core Components

### 1. Agent Layer (`src/agents/`)

#### BaseAgent
- Abstract base class for all agents
- Handles common functionality: thinking, tool usage, state management
- Provides execution framework with error handling

#### Specialized Agents
- **ResearchAgent**: Information gathering and synthesis
- **AnalystAgent**: Data analysis and critical thinking
- **CoderAgent**: Code generation and analysis
- **PlannerAgent**: Task decomposition and planning
- **WriterAgent**: Content creation

Each agent has:
- Specific system prompt defining its role
- Configurable LLM parameters (temperature, max_tokens)
- Tool access for specialized capabilities
- State tracking for conversation history

### 2. Orchestration Layer (`src/orchestration/`)

#### AgentOrchestrator
Manages multi-agent coordination with three patterns:

**Sequential Execution**
```python
orchestrator.execute_sequential(
    task="Analyze data",
    agent_sequence=["researcher", "analyst", "writer"]
)
```
- Agents execute in order
- Each agent receives results from previous agents
- Good for pipeline-style workflows

**Parallel Execution**
```python
await orchestrator.execute_parallel([
    {"agent": "analyst1", "task": "Analyze security"},
    {"agent": "analyst2", "task": "Analyze performance"}
])
```
- Multiple agents work simultaneously
- Controlled concurrency (max_concurrent parameter)
- Good for independent analysis tasks

**Hierarchical Execution**
```python
orchestrator.execute_hierarchical(
    task="Complex project",
    planner_agent="planner"
)
```
- Planner breaks down task into subtasks
- Delegates subtasks to specialist agents
- Good for complex, multi-step problems

### 3. Core Framework (`src/core/`)

#### OllamaLLM
- Wrapper for Ollama API
- Supports sync/async generation
- Streaming support
- Embedding generation
- GPU optimization

#### Messages & State
- `Message`: Individual conversation messages
- `AgentState`: Tracks agent execution state
- `TaskResult`: Standardized result format
- Conversation history management

#### Configuration
- Pydantic-based settings
- Environment variable loading
- Directory management
- Validation

### 4. Memory System (`src/memory/`)

#### VectorMemory (ChromaDB)
- Semantic search over past interactions
- Persistent storage
- Embedding-based retrieval
- Metadata filtering

#### ConversationMemory
- Short-term conversation buffer
- Fixed size window (configurable)
- Fast access to recent context

#### HybridMemory
- Combines vector and conversation memory
- Best of both: recency + relevance
- Context retrieval for LLM prompts

### 5. Tool System (`src/tools/`)

#### BaseTool
- Abstract interface for tools
- Parameter validation
- Schema generation for function calling

#### Common Tools
- **CalculatorTool**: Math operations
- **FileReadTool**: File reading
- **FileWriteTool**: File writing
- **PythonExecutorTool**: Safe code execution
- **SearchTool**: Document search

Tools are:
- Modular and extensible
- Type-safe with Pydantic
- Isolated execution for safety

## Data Flow

```
User Input
    ↓
Orchestrator (decides execution pattern)
    ↓
Agent(s) Selected
    ↓
Agent.execute()
    ├─→ Think (LLM generation)
    ├─→ Use Tools (if needed)
    ├─→ Memory Retrieval
    └─→ State Management
    ↓
TaskResult
    ↓
Context passed to next agent (sequential)
or
Results aggregated (parallel/hierarchical)
    ↓
Final Result
```

## Key Design Patterns

### 1. Agent Specialization
Each agent has a narrow, well-defined role. This enables:
- Better prompt engineering
- Clearer responsibility boundaries
- Easier debugging and improvement

### 2. State Management
Agents maintain state throughout execution:
- Conversation history
- Tool usage tracking
- Status updates
- Metadata

### 3. Async Support
Framework supports both sync and async execution:
- Parallel agent execution
- Non-blocking operations
- Better resource utilization

### 4. Error Handling
Comprehensive error handling:
- Try-catch at agent level
- TaskResult always returned
- Errors logged and tracked
- Graceful degradation

### 5. Modularity
Components are loosely coupled:
- Agents don't depend on orchestrator
- Tools are independent
- Memory systems are pluggable
- Easy to extend and customize

## Configuration Architecture

### Three Levels of Configuration

**1. Environment Variables (`.env`)**
- System-level settings
- API keys and URLs
- Performance parameters

**2. YAML Configuration (`config/agents_config.yaml`)**
- Agent definitions
- Model assignments
- Tool configurations
- Orchestration patterns

**3. Runtime Parameters**
- Task-specific context
- Dynamic agent creation
- On-the-fly tool assignment

## Execution Patterns

### Pattern Selection Guide

| Use Case | Pattern | Why |
|----------|---------|-----|
| Research → Analysis → Report | Sequential | Each step builds on previous |
| Multi-perspective analysis | Parallel | Independent analyses |
| Complex problem solving | Hierarchical | Needs planning & coordination |
| Simple query | Single Agent | Straightforward task |

### Scaling Considerations

**Vertical Scaling** (single machine)
- GPU acceleration (CUDA)
- Batch processing
- Memory optimization
- Model quantization

**Horizontal Scaling** (multiple machines)
- Distributed memory (Redis)
- Distributed execution (Ray)
- Load balancing
- State synchronization

## Best Practices

### 1. Agent Design
- Keep system prompts focused and specific
- Use lower temperature for factual tasks
- Use higher temperature for creative tasks
- Assign tools only when needed

### 2. Orchestration
- Choose appropriate pattern for task
- Limit concurrent agents based on resources
- Pass context efficiently between agents
- Monitor execution time

### 3. Memory Management
- Use vector memory for long-term knowledge
- Use conversation memory for recent context
- Clear memory periodically
- Index on relevant metadata

### 4. Tool Development
- Make tools atomic (single responsibility)
- Validate inputs thoroughly
- Handle errors gracefully
- Document parameters clearly

### 5. Performance
- Use GPU when available
- Batch similar requests
- Cache frequent queries
- Profile and optimize bottlenecks

## Extension Points

The framework is designed to be extended:

1. **Custom Agents**: Inherit from `BaseAgent`
2. **Custom Tools**: Inherit from `BaseTool`
3. **Custom Memory**: Implement memory interface
4. **Custom Orchestration**: Extend `AgentOrchestrator`
5. **Custom Models**: Adapt `OllamaLLM` or create new LLM class

## Security Considerations

- Code execution is sandboxed
- File operations are restricted to workspace
- No direct shell access by default
- Input validation on all tools
- Configurable operation allowlists
