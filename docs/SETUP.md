# Setup Guide

## Prerequisites

1. **Python 3.10 or higher**
   ```bash
   python --version
   ```

2. **Ollama installed and running**
   - Download from: https://ollama.ai
   - Start Ollama: `ollama serve`
   - Pull required models:
     ```bash
     ollama pull llama3.1:8b
     ollama pull codellama:13b
     ```

3. **GPU with CUDA support (recommended)**
   - Check GPU: `nvidia-smi`
   - Ollama will automatically use GPU if available

## Installation

### 1. Clone or Navigate to Project
```bash
cd /home/mbl-ph/zzzzz/zzz/multi-model
```

### 2. Create Virtual Environment
```bash
python -m venv venv
source venv/bin/activate  # On Linux/Mac
```

### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

### 4. Configure Environment
```bash
cp .env.example .env
```

Edit `.env` file to match your setup:
```bash
nano .env
```

Key settings:
- `OLLAMA_BASE_URL`: Default is `http://localhost:11434`
- `OLLAMA_MODEL`: Choose your preferred model
- `ENABLE_GPU`: Set to `true` if you have GPU

### 5. Verify Ollama Connection
```bash
curl http://localhost:11434/api/tags
```

This should return a list of available models.

## Quick Start

### 1. Test Simple Agent
```bash
python examples/simple_agent.py
```

### 2. Run Research Pipeline
```bash
python examples/research_pipeline.py
```

### 3. Launch Streamlit UI
```bash
streamlit run streamlit_app/app.py
```

The UI will open at `http://localhost:8501`

## Troubleshooting

### Ollama Not Running
```bash
# Check if Ollama is running
ps aux | grep ollama

# Start Ollama
ollama serve
```

### Model Not Found
```bash
# List available models
ollama list

# Pull missing model
ollama pull llama3.1:8b
```

### GPU Not Detected
- Ensure CUDA is installed
- Check with: `nvidia-smi`
- Ollama should automatically use GPU

### Import Errors
```bash
# Reinstall dependencies
pip install -r requirements.txt --force-reinstall
```

### ChromaDB Issues
```bash
# Clear ChromaDB data
rm -rf ./data/chroma/*
```

## Running Tests

```bash
# Install test dependencies
pip install pytest pytest-asyncio pytest-cov

# Run tests
pytest tests/

# Run with coverage
pytest --cov=src tests/
```

## Next Steps

1. Read the [Architecture Guide](architecture.md)
2. Explore [Creating Custom Agents](custom_agents.md)
3. Check out [Real-World Examples](examples.md)
4. Learn about [Tool Development](tools.md)

## Performance Tuning

### For Low RAM Systems (< 16GB)
- Use smaller models: `llama3.1:7b` or `mistral:7b`
- Reduce `BATCH_SIZE` in `.env`
- Reduce `MAX_CONCURRENT_AGENTS`

### For High-End Systems (32GB+ RAM, GPU)
- Use larger models: `mixtral:8x7b` or `llama3.1:70b`
- Increase `BATCH_SIZE` to 8-16
- Increase `MAX_CONCURRENT_AGENTS` to 5-10
- Set `GPU_MEMORY_FRACTION` to 0.9

### Optimizing for Speed
```bash
# In .env file
BATCH_SIZE=8
MAX_CONCURRENT_AGENTS=5
GPU_MEMORY_FRACTION=0.9
```

## Common Configuration Tweaks

### Using Different Models
Edit `config/agents_config.yaml` to change models per agent:
```yaml
agents:
  researcher:
    model: "mixtral:8x7b"  # Larger model for research
  coder:
    model: "codellama:34b"  # Larger code model
```

### Adjusting Agent Behavior
Change temperature settings:
- Lower (0.1-0.3): More deterministic, factual
- Medium (0.4-0.6): Balanced
- Higher (0.7-0.9): More creative

## Support

For issues or questions:
1. Check the logs in `./logs/agent.log`
2. Review configuration in `.env` and `config/agents_config.yaml`
3. Ensure Ollama is running and models are downloaded
