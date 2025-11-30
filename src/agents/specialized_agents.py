"""
Specialized agent implementations.
"""
from typing import Dict, Any, List
import json
from loguru import logger

from .base_agent import BaseAgent


class ResearchAgent(BaseAgent):
    """Agent specialized in research and information gathering."""
    
    def process(self, task: str, context: Dict[str, Any]) -> Dict[str, Any]:
        """Conduct research on the given task."""
        
        # Create research plan
        plan_prompt = f"""
        Task: {task}
        
        Create a detailed research plan with specific steps to gather comprehensive information.
        Format your response as a JSON list of research steps.
        """
        
        plan_response = self.think(plan_prompt)
        
        # Execute research
        research_prompt = f"""
        Task: {task}
        Research Plan: {plan_response}
        
        Based on your knowledge and the research plan, provide a comprehensive research report.
        Include:
        1. Key findings
        2. Supporting evidence
        3. Different perspectives
        4. Conclusions
        
        Format as a structured report.
        """
        
        research_result = self.think(research_prompt)
        
        return {
            "plan": plan_response,
            "findings": research_result,
            "sources": context.get("sources", [])
        }


class AnalystAgent(BaseAgent):
    """Agent specialized in data analysis and critical thinking."""
    
    def process(self, task: str, context: Dict[str, Any]) -> Dict[str, Any]:
        """Analyze the given task or data."""
        
        data = context.get("data", "")
        
        analysis_prompt = f"""
        Task: {task}
        Data: {data}
        
        Perform a comprehensive analysis:
        1. Identify key patterns and trends
        2. Calculate relevant metrics
        3. Draw insights and conclusions
        4. Provide actionable recommendations
        
        Be specific and data-driven in your analysis.
        """
        
        analysis = self.think(analysis_prompt)
        
        # Generate summary
        summary_prompt = f"""
        Based on this analysis:
        {analysis}
        
        Provide a concise executive summary (3-5 key points).
        """
        
        summary = self.think(summary_prompt)
        
        return {
            "analysis": analysis,
            "summary": summary,
            "metrics": context.get("metrics", {})
        }


class CoderAgent(BaseAgent):
    """Agent specialized in code generation and analysis."""
    
    def process(self, task: str, context: Dict[str, Any]) -> Dict[str, Any]:
        """Generate or analyze code."""
        
        code_context = context.get("code", "")
        language = context.get("language", "python")
        
        if "generate" in task.lower() or "write" in task.lower():
            # Code generation
            prompt = f"""
            Task: {task}
            Language: {language}
            Context: {code_context}
            
            Generate clean, efficient, and well-documented code.
            Include:
            1. Implementation
            2. Comments explaining key logic
            3. Example usage
            4. Error handling
            """
            
            code = self.think(prompt)
            
            return {
                "code": code,
                "language": language,
                "type": "generation"
            }
        else:
            # Code analysis
            prompt = f"""
            Task: {task}
            Code to analyze:
            ```{language}
            {code_context}
            ```
            
            Analyze the code and provide:
            1. Code quality assessment
            2. Potential issues or bugs
            3. Performance considerations
            4. Improvement suggestions
            5. Best practices violations
            """
            
            analysis = self.think(prompt)
            
            return {
                "analysis": analysis,
                "code": code_context,
                "language": language,
                "type": "analysis"
            }


class PlannerAgent(BaseAgent):
    """Agent specialized in task planning and decomposition."""
    
    def process(self, task: str, context: Dict[str, Any]) -> Dict[str, Any]:
        """Create a detailed plan for the task."""
        
        available_agents = context.get("available_agents", [])
        
        planning_prompt = f"""
        Task: {task}
        Available agents: {', '.join(available_agents)}
        
        Create a detailed execution plan:
        1. Break down the task into logical subtasks
        2. Assign each subtask to the most appropriate agent
        3. Define dependencies between subtasks
        4. Estimate complexity and order of execution
        
        Format your response as a structured plan with clear steps.
        """
        
        plan = self.think(planning_prompt)
        
        # Extract actionable steps
        steps_prompt = f"""
        Based on this plan:
        {plan}
        
        Extract a list of actionable steps in JSON format:
        [
            {{"step": 1, "description": "...", "agent": "...", "dependencies": []}},
            ...
        ]
        """
        
        steps_response = self.think(steps_prompt)
        
        try:
            # Try to parse JSON steps
            import re
            json_match = re.search(r'\[.*\]', steps_response, re.DOTALL)
            if json_match:
                steps = json.loads(json_match.group())
            else:
                steps = []
        except:
            steps = []
        
        return {
            "plan": plan,
            "steps": steps,
            "total_steps": len(steps)
        }


class WriterAgent(BaseAgent):
    """Agent specialized in content creation and writing."""
    
    def process(self, task: str, context: Dict[str, Any]) -> Dict[str, Any]:
        """Generate written content."""
        
        content_type = context.get("content_type", "article")
        tone = context.get("tone", "professional")
        length = context.get("length", "medium")
        
        writing_prompt = f"""
        Task: {task}
        Content Type: {content_type}
        Tone: {tone}
        Length: {length}
        
        Create high-quality written content that:
        1. Is well-structured and organized
        2. Matches the requested tone and style
        3. Is engaging and clear
        4. Includes relevant examples or details
        
        Generate the complete content now.
        """
        
        content = self.think(writing_prompt)
        
        return {
            "content": content,
            "type": content_type,
            "word_count": len(content.split())
        }
