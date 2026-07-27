from typing import Generator

from langchain_groq import ChatGroq

from app.core.config import GROQ_API_KEY


class GroqLLM:
    """
    Wrapper class for Groq LLM.
    Supports both normal and streaming responses.
    """

    def __init__(
        self,
        model: str = "llama-3.1-8b-instant",
        temperature: float = 0.2,
    ):
        self.llm = ChatGroq(
            model=model,
            api_key=GROQ_API_KEY,
            temperature=temperature,
            streaming=True,
        )

    def generate(self, prompt: str) -> str:
        """
        Generate a complete response.
        """
        try:
            response = self.llm.invoke(prompt)
            return response.content

        except Exception as e:
            raise RuntimeError(f"Groq API Error: {e}")

    def stream(self, prompt: str) -> Generator[str, None, None]:
        """
        Stream response token by token.
        """

        try:
            for chunk in self.llm.stream(prompt):

                if chunk.content:
                    yield chunk.content

        except Exception as e:
            raise RuntimeError(f"Groq Streaming Error: {e}")