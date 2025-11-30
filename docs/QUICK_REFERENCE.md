# Quick Reference Guide

## Common Commands

### Setup
```bash
# Initial setup
./setup.sh

# Activate virtual environment
source venv/bin/activate

# Install/update dependencies
pip install -r requirements.txt
```

### Running Examples
```bash
# Simple agent
python examples/simple_agent.py

# Research pipeline
python examples/research_pipeline.py

# Code review
python examples/code_review_pipeline.py

# Business intelligence
python examples/business_intelligence.py
```

### Streamlit UI
```bash
streamlit run streamlit_app/app.py
```

### Ollama Management
```bash
# List models
ollama list

# Pull a model
ollama pull llama3.1:8b

# Check if running
curl http://localhost:11434/api/tags
```

## Quick Patterns

### Single Agent
```python
from src.agents import ResearchAgent

agent = ResearchAgent(
    name="MyAgent",
    model="llama3.1:8b",
    system_prompt="You are...",
    temperature=0.7
)

result = agent.execute("Your task here")
print(result.result)
```

### Sequential Pipeline
```python
from src.agents import ResearchAgent, AnalystAgent, WriterAgent
from src.orchestration import AgentOrchestrator

agents = {
    "researcher": ResearchAgent(...),
    "analyst": AnalystAgent(...),
    "writer": WriterAgent(...)
}

orchestrator = AgentOrchestrator(agents)

result = orchestrator.execute_sequential(
    task="Your complex task",
    agent_sequence=["researcher", "analyst", "writer"]
)
```

### Parallel Execution
```python
import asyncio
from src.orchestration import AgentOrchestrator

tasks = [
    {"agent": "agent1", "task": "Task 1", "context": {}},
    {"agent": "agent2", "task": "Task 2", "context": {}},
]

results = await orchestrator.execute_parallel(tasks)
```

### Hierarchical Planning
```python
result = orchestrator.execute_hierarchical(
    task="Complex multi-step task",
    planner_agent="planner"
)
```

## Configuration Quick Tips

### Change Model
```python
# In code
agent = ResearchAgent(
    model="mixtral:8x7b",  # Use different model
    ...
)

# In config/agents_config.yaml
agents:
  researcher:
    model: "mixtral:8x7b"
```

### Adjust Temperature
- 0.1-0.3: Factual, deterministic
- 0.4-0.6: Balanced
- 0.7-0.9: Creative

### Enable Tools
```python
from src.tools import CalculatorTool, FileReadTool

agent = CoderAgent(
    tools=[CalculatorTool(), FileReadTool()],
    ...
)
```

## Troubleshooting Quick Fixes

### Ollama Connection Error
```bash
# Check if running
ps aux | grep ollama

# Start Ollama
ollama serve
```

### Import Errors
```bash
# Reinstall
pip install -r requirements.txt --force-reinstall

# Check virtual environment
which python  # Should show venv path
```

### Memory Issues
```python
# Clear ChromaDB
from src.memory import VectorMemory
memory = VectorMemory()
memory.clear()
```

### Out of Memory
```bash
# In .env file
OLLAMA_MODEL=llama3.1:7b  # Use smaller model
BATCH_SIZE=2  # Reduce batch size
MAX_CONCURRENT_AGENTS=1  # Reduce concurrency
```

## Performance Tips

### For Speed
```bash
# .env
BATCH_SIZE=8
MAX_CONCURRENT_AGENTS=5
GPU_MEMORY_FRACTION=0.9
```

### For Accuracy
```python
# Use larger models
model="llama3.1:70b"  # or mixtral:8x7b

# Lower temperature
temperature=0.1
```

### For Memory Efficiency
```python
# Use smaller models
model="llama3.1:7b"

# Reduce context window
max_tokens=1000
```

## File Structure Quick Map

```
multi-model/
├── src/                      # Core framework
│   ├── agents/              # Agent implementations
│   ├── core/                # LLM, config, messages
│   ├── memory/              # Vector & conversation memory
│   ├── orchestration/       # Multi-agent coordination
│   ├── tools/               # Agent tools
│   └── utils/               # Helper functions
├── examples/                # Usage examples
├── streamlit_app/           # Web UI
├── config/                  # Configuration files
├── docs/                    # Documentation
├── data/                    # Data storage
├── logs/                    # Log files
└── tests/                   # Tests
```

## Environment Variables

```bash
# Essential
OLLAMA_BASE_URL=http://localhost:11434
OLLAMA_MODEL=llama3.1:8b
ENABLE_GPU=true

# Memory
CHROMA_PERSIST_DIR=./data/chroma
MEMORY_TYPE=chromadb

# Performance
BATCH_SIZE=4
MAX_CONCURRENT_AGENTS=3
```

## Common Patterns by Use Case

### Research & Analysis
```
ResearchAgent → AnalystAgent → WriterAgent
```

### Code Development
```
PlannerAgent → CoderAgent → AnalystAgent (review)
```

### Content Creation
```
ResearchAgent → WriterAgent
```

### Business Intelligence
```
AnalystAgent → ResearchAgent → WriterAgent
```

## API Quick Reference

### Agent Methods
```python
agent.execute(task, context)     # Main execution
agent.think(prompt)               # Get LLM response
agent.use_tool(tool_name, **kwargs)  # Use a tool
agent.reset_state()               # Reset state
```

### Orchestrator Methods
```python
orchestrator.execute_sequential(...)
orchestrator.execute_parallel(...)
orchestrator.execute_hierarchical(...)
orchestrator.add_agent(name, agent)
orchestrator.list_agents()
```

### Memory Methods
```python
memory.add(text, metadata)
memory.search(query, top_k)
memory.clear()
memory.get_count()
```
