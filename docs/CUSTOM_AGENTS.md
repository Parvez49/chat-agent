# Creating Custom Agents

This guide shows you how to create custom agents for your specific use cases.

## Basic Custom Agent

```python
from src.agents import BaseAgent
from typing import Dict, Any

class CustomAgent(BaseAgent):
    """Your custom agent implementation."""
    
    def process(self, task: str, context: Dict[str, Any]) -> Any:
        """
        Process the task and return results.
        
        Args:
            task: The task description
            context: Additional context dictionary
            
        Returns:
            Result of processing (can be any type)
        """
        # Your custom logic here
        
        # Use self.think() to get LLM response
        prompt = f"Task: {task}\nContext: {context}"
        response = self.think(prompt)
        
        return {"result": response}
```

## Example: Domain-Specific Agent

### 1. Medical Diagnosis Agent

```python
from src.agents import BaseAgent
from typing import Dict, Any, List

class MedicalDiagnosisAgent(BaseAgent):
    """Agent specialized in medical diagnosis assistance."""
    
    def process(self, task: str, context: Dict[str, Any]) -> Dict[str, Any]:
        """Analyze symptoms and provide potential diagnoses."""
        
        symptoms = context.get("symptoms", [])
        patient_history = context.get("history", "")
        
        # Create structured prompt
        prompt = f"""
        Analyze the following medical case:
        
        Symptoms: {', '.join(symptoms)}
        Patient History: {patient_history}
        Question: {task}
        
        Provide:
        1. Potential diagnoses (differential diagnosis)
        2. Recommended tests
        3. Severity assessment
        4. Immediate actions needed
        
        Note: This is for informational purposes only.
        """
        
        analysis = self.think(prompt)
        
        # Extract structured information
        summary_prompt = f"""
        Based on this analysis:
        {analysis}
        
        Provide a brief summary of:
        - Most likely diagnosis
        - Urgency level (Low/Medium/High)
        - Next steps
        """
        
        summary = self.think(summary_prompt)
        
        return {
            "full_analysis": analysis,
            "summary": summary,
            "symptoms": symptoms
        }


# Usage
agent = MedicalDiagnosisAgent(
    name="MedicalDiagnosisAgent",
    model="llama3.1:8b",
    system_prompt="""You are a medical AI assistant with expertise in diagnosis.
    Provide thorough analysis while emphasizing the need for professional medical consultation.
    Always consider patient safety first.""",
    temperature=0.3  # Lower for medical accuracy
)

result = agent.execute(
    "What could be causing these symptoms?",
    context={
        "symptoms": ["persistent cough", "fever", "fatigue"],
        "history": "Non-smoker, no chronic conditions"
    }
)
```

### 2. Financial Analysis Agent

```python
from src.agents import BaseAgent
from src.tools import CalculatorTool
from typing import Dict, Any

class FinancialAnalystAgent(BaseAgent):
    """Agent specialized in financial analysis."""
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Add financial tools
        self.tools.append(CalculatorTool())
    
    def process(self, task: str, context: Dict[str, Any]) -> Dict[str, Any]:
        """Perform financial analysis."""
        
        financial_data = context.get("financial_data", {})
        
        # Calculate key metrics
        metrics = self._calculate_metrics(financial_data)
        
        # Get LLM interpretation
        analysis_prompt = f"""
        Analyze this financial data:
        
        Data: {financial_data}
        Calculated Metrics: {metrics}
        
        Task: {task}
        
        Provide:
        1. Financial health assessment
        2. Key trends and patterns
        3. Risk factors
        4. Recommendations
        """
        
        analysis = self.think(analysis_prompt)
        
        return {
            "metrics": metrics,
            "analysis": analysis,
            "raw_data": financial_data
        }
    
    def _calculate_metrics(self, data: Dict[str, Any]) -> Dict[str, float]:
        """Calculate financial metrics."""
        metrics = {}
        
        revenue = data.get("revenue", 0)
        expenses = data.get("expenses", 0)
        
        if revenue > 0:
            metrics["profit_margin"] = ((revenue - expenses) / revenue) * 100
        
        # Add more calculations as needed
        
        return metrics
```

### 3. Content Moderation Agent

```python
from src.agents import BaseAgent
from typing import Dict, Any, List

class ContentModerationAgent(BaseAgent):
    """Agent for content moderation and safety checking."""
    
    def process(self, task: str, context: Dict[str, Any]) -> Dict[str, Any]:
        """Moderate content for safety and appropriateness."""
        
        content = context.get("content", "")
        guidelines = context.get("guidelines", "General community guidelines")
        
        # Check for issues
        analysis_prompt = f"""
        Review this content according to the guidelines:
        
        Content: {content}
        Guidelines: {guidelines}
        
        Check for:
        1. Inappropriate language
        2. Harmful content
        3. Spam or misleading information
        4. Privacy violations
        5. Community guideline violations
        
        Provide:
        - Overall safety score (0-100)
        - Specific issues found
        - Recommended actions
        - Sanitized version if needed
        """
        
        analysis = self.think(analysis_prompt)
        
        # Extract safety score
        score_prompt = f"""
        Based on this analysis: {analysis}
        
        Provide ONLY a safety score from 0-100 where:
        - 90-100: Safe, no issues
        - 70-89: Minor issues, review recommended
        - 50-69: Moderate issues, action needed
        - 0-49: Serious issues, remove content
        
        Return only the number.
        """
        
        try:
            safety_score = int(self.think(score_prompt).strip())
        except:
            safety_score = 50  # Default to moderate if parsing fails
        
        return {
            "content": content,
            "safety_score": safety_score,
            "analysis": analysis,
            "approved": safety_score >= 70
        }
```

## Agent with RAG (Retrieval-Augmented Generation)

```python
from src.agents import BaseAgent
from src.memory import VectorMemory
from typing import Dict, Any

class RAGAgent(BaseAgent):
    """Agent with RAG capabilities."""
    
    def __init__(self, *args, knowledge_base_collection: str = "knowledge", **kwargs):
        super().__init__(*args, **kwargs)
        self.vector_memory = VectorMemory(collection_name=knowledge_base_collection)
    
    def add_knowledge(self, text: str, metadata: Dict[str, Any] = None):
        """Add information to the knowledge base."""
        self.vector_memory.add(text, metadata)
    
    def process(self, task: str, context: Dict[str, Any]) -> Dict[str, Any]:
        """Process task with RAG."""
        
        # Retrieve relevant knowledge
        relevant_docs = self.vector_memory.search(task, top_k=5)
        
        # Build context from retrieved docs
        retrieved_context = "\n\n".join([
            f"Document {i+1}: {doc['text']}"
            for i, doc in enumerate(relevant_docs)
        ])
        
        # Create prompt with retrieved context
        prompt = f"""
        Task: {task}
        
        Relevant Information:
        {retrieved_context}
        
        Additional Context: {context}
        
        Use the provided information to answer the task thoroughly.
        Cite sources when possible.
        """
        
        response = self.think(prompt)
        
        return {
            "response": response,
            "sources": relevant_docs,
            "retrieved_docs_count": len(relevant_docs)
        }


# Usage
rag_agent = RAGAgent(
    name="KnowledgeAgent",
    model="llama3.1:8b",
    system_prompt="You are a knowledge assistant. Use provided context to answer accurately.",
    temperature=0.4,
    knowledge_base_collection="company_docs"
)

# Add knowledge
rag_agent.add_knowledge(
    "Our company was founded in 2020...",
    metadata={"source": "company_history.pdf", "page": 1}
)

# Query
result = rag_agent.execute("When was our company founded?")
```

## Advanced: Agent with Self-Reflection

```python
from src.agents import BaseAgent
from typing import Dict, Any

class ReflectiveAgent(BaseAgent):
    """Agent that can reflect on and improve its responses."""
    
    def process(self, task: str, context: Dict[str, Any]) -> Dict[str, Any]:
        """Process with self-reflection loop."""
        
        max_iterations = context.get("max_iterations", 3)
        
        # Initial attempt
        current_response = self.think(task)
        
        for iteration in range(max_iterations):
            # Reflect on response
            reflection_prompt = f"""
            Task: {task}
            Current Response: {current_response}
            
            Critique this response:
            1. What's good about it?
            2. What's missing or unclear?
            3. How can it be improved?
            4. Is it complete and accurate?
            
            Be critical and specific.
            """
            
            critique = self.think(reflection_prompt)
            
            # Check if satisfied
            if "complete and accurate" in critique.lower() or iteration == max_iterations - 1:
                break
            
            # Improve response
            improvement_prompt = f"""
            Task: {task}
            Previous Response: {current_response}
            Critique: {critique}
            
            Provide an improved response addressing the critique.
            """
            
            current_response = self.think(improvement_prompt)
        
        return {
            "final_response": current_response,
            "iterations": iteration + 1,
            "improved": iteration > 0
        }
```

## Best Practices for Custom Agents

### 1. Clear System Prompts
```python
system_prompt = """
You are a [ROLE] with expertise in [DOMAIN].

Your responsibilities:
- [Responsibility 1]
- [Responsibility 2]

Guidelines:
- [Guideline 1]
- [Guideline 2]

Output format:
- [Expected format]
"""
```

### 2. Structured Context
```python
def process(self, task: str, context: Dict[str, Any]) -> Dict[str, Any]:
    # Extract and validate context
    required_fields = ["field1", "field2"]
    for field in required_fields:
        if field not in context:
            raise ValueError(f"Missing required field: {field}")
    
    # Process with structured data
    ...
```

### 3. Error Handling
```python
def process(self, task: str, context: Dict[str, Any]) -> Dict[str, Any]:
    try:
        # Your processing logic
        result = self.think(prompt)
        return {"success": True, "result": result}
    except Exception as e:
        logger.error(f"Error in {self.name}: {e}")
        return {"success": False, "error": str(e)}
```

### 4. Type Hints
```python
from typing import Dict, Any, List, Optional

def process(
    self, 
    task: str, 
    context: Dict[str, Any]
) -> Dict[str, Any]:
    """
    Process the task.
    
    Args:
        task: Task description
        context: Additional context
        
    Returns:
        Dictionary with results
    """
    ...
```

## Testing Custom Agents

```python
# test_custom_agent.py
import pytest
from your_module import CustomAgent

def test_custom_agent():
    agent = CustomAgent(
        name="TestAgent",
        model="llama3.1:8b",
        system_prompt="Test prompt",
        temperature=0.1
    )
    
    result = agent.execute(
        "Test task",
        context={"test": "data"}
    )
    
    assert result.success
    assert "result" in result.result
```

## Integration with Orchestrator

```python
from src.orchestration import AgentOrchestrator

# Add custom agent to orchestrator
orchestrator = AgentOrchestrator({
    "custom": CustomAgent(...),
    "other": OtherAgent(...)
})

# Use in workflow
result = orchestrator.execute_sequential(
    task="Complex task",
    agent_sequence=["custom", "other"]
)
```
