from langchain_community.llms import Ollama
from langchain_core.prompts import PromptTemplate
from app.core.config import settings
import os

class GenerationService:
    def __init__(self):
        self.llm = Ollama(model=settings.OLLAMA_MODEL, base_url=settings.OLLAMA_HOST)
        
        template = """You are an expert football tactics assistant. Answer the question based ONLY on the provided context.
If the context does not contain the answer, say "I don't know based on the provided documents."
When you provide an answer, try to cite the source document.

Context from Rulebooks/Coaching Manuals:
{context}

Tactical Vision Context (from YOLOv8 image analysis):
{vision_context}

Question: {question}

Answer:"""
        self.prompt = PromptTemplate.from_template(template)

    def generate_answer(self, question: str, docs: list, vision_context: str = "") -> tuple[str, list[str]]:
        """Generates an answer using Ollama and returns it with sources."""
        
        # Format the context
        formatted_docs = []
        sources = set()
        for d in docs:
            source_file = os.path.basename(d.metadata.get("source", "Unknown"))
            sources.add(source_file)
            formatted_docs.append(f"[Source: {source_file}]\n{d.page_content}")
            
        context_str = "\n\n".join(formatted_docs)
        
        # Generate the answer
        formatted_prompt = self.prompt.format(
            context=context_str,
            vision_context=vision_context if vision_context else "No image provided.",
            question=question
        )
        
        answer = self.llm.invoke(formatted_prompt)
        
        return answer, list(sources)

generation_service = GenerationService()
