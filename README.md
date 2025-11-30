# Multi-Agent System Framework

A production-ready multi-agent system framework for solving real-world problems using local Ollama models with GPU acceleration.

## 🏗️ Architecture Overview

This framework implements a sophisticated multi-agent system with:
- **Agent Orchestration**: Coordinator pattern for complex task decomposition
- **Specialized Agents**: Research, Analysis, Planning, Execution agents
- **Memory Management**: Short-term and long-term memory with vector storage
- **Tool Integration**: Extensible tool system for agents
- **Local LLM**: Ollama integration with GPU optimization
- **Observability**: Comprehensive logging and monitoring

## 📁 Project Structure

```
multi-model/
├── src/
│   ├── agents/              # Agent implementations
│   ├── core/                # Core framework components
│   ├── memory/              # Memory systems
│   ├── tools/               # Agent tools
│   ├── orchestration/       # Multi-agent coordination
│   └── utils/               # Utilities
├── config/                  # Configuration files
├── data/                    # Data storage
├── examples/                # Real-world use cases
├── streamlit_app/           # Streamlit UI
└── tests/                   # Test suite
```

## 🚀 Features

- **Multi-Agent Coordination**: Hierarchical and collaborative agent patterns
- **RAG-Enhanced Agents**: Built-in RAG pipeline integration
- **Async Processing**: Efficient concurrent agent execution
- **State Management**: Persistent conversation and task state
- **Tool Ecosystem**: Extensible tools for web search, code execution, file ops
- **GPU Optimization**: Batch processing and memory management
- **Production-Ready**: Error handling, retries, logging

## 🎯 Real-World Use Cases

1. **Research Assistant**: Multi-agent research with validation
2. **Code Analysis & Refactoring**: Automated code review and improvement
3. **Business Intelligence**: Data analysis with multiple specialized agents
4. **Content Generation Pipeline**: Multi-stage content creation

## 🔧 Prerequisites

- Python 3.10+
- Ollama running locally
- GPU with CUDA support (recommended)
- 16GB+ RAM

## 📦 Installation

```bash
# Create virtual environment
python -m venv venv
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Set up environment variables
cp .env.example .env
# Edit .env with your configuration
```

## 🏃 Quick Start

```bash
# Run a simple example
python examples/simple_agent.py

# Run multi-agent research example
python examples/research_pipeline.py

# Launch Streamlit UI
streamlit run streamlit_app/app.py
```

## 🛠️ Configuration

Edit `config/agents_config.yaml` to customize:
- Agent personalities and capabilities
- Model selection (Ollama models)
- Memory settings
- Tool configurations

## 📚 Documentation

See `docs/` for detailed documentation on:
- Agent architecture
- Creating custom agents
- Tool development
- Orchestration patterns
- Best practices

## 🧪 Testing

```bash
# Run all tests
pytest tests/

# Run specific test suite
pytest tests/agents/

# Run with coverage
pytest --cov=src tests/
```

## 🎨 Streamlit Interface

The Streamlit app provides:
- Agent conversation visualization
- Real-time task monitoring
- Memory inspector
- Configuration management
- Performance metrics

## 📈 Performance Tips

- Use batch processing for multiple queries
- Enable GPU memory optimization in config
- Adjust context window based on available RAM
- Use caching for repeated queries

## 🤝 Contributing

See `CONTRIBUTING.md` for guidelines.

## 📝 License

MIT License
