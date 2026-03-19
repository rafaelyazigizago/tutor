from .tool_agent import ToolAgent


class LLMAgent(ToolAgent):

    def __init__(self):
        super().__init__("LLMAgent")

    def execute(self, payload):
        prompt = payload.get("prompt")
        memories = self.use_tool("vector_memory", action="search", query=prompt)
        context = "\n".join(memories) if memories else ""
        full_prompt = f"Contexto relevante:\n{context}\n\nPergunta:\n{prompt}"
        response = self.use_tool("llm", prompt=full_prompt)
        print("LLM RESPONSE:")
        print(response)
        self.use_tool("vector_memory", action="store", text=f"Pergunta: {prompt} | Resposta: {response}")
        return response
