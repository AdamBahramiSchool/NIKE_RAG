from openai import OpenAI

class generator:
    def __init__(self, user_query: str, vector_store):
        self.user_query = user_query
        self.vector_store = vector_store
        self.results = []
        self.client = OpenAI()
        self.user_response = ""
        # collect history of llm responses, users could ask follow up question, use as context in the prompt
        self.last_responses=[]
        self.last_questions=[]

    def similarity_search(self, k: int = 3):
        self.results = self.vector_store.similarity_search(self.user_query, k=k)
        return self.results

    def display_results(self) -> None:
        if not self.results:
            print("No results found.")
            return

        for i, result in enumerate(self.results, start=1):
            source = result.metadata.get("source", "unknown")
            page = result.metadata.get("page", "unknown")
            preview = result.page_content[:240].replace("\n", " ")
            print(f"[{i}] source={source} page={page}")
            print(preview)
            print("-" * 40)

    def llmgeneration(self) -> str:
        if not self.results:
            return "I couldn't find relevant context in the document."

        context_chunks = "\n\n".join(
            f"[Chunk {i}] {result.page_content[:700]}"
            for i, result in enumerate(self.results, start=1)
        )

        prompt=""
        if self.last_questions and self.last_responses:
            prompt=(
                        f"Question: {self.user_query}\n\n"
                        f"Previous LLM question and response, for context, if user asks follow up question: \n{self.last_questions[-1]}\n {self.last_responses[-1]}" 
                        f"Retrieved context:\n{context_chunks}\n\n"
                        "Return one clear final answer sentence."
                    )
        else:
            prompt = (
                f"Question: {self.user_query}\n\n"
                f"Retrieved context:\n{context_chunks}\n\n"
                "Return one clear final answer sentence."
            )
        response = self.client.chat.completions.create(
            model="gpt-4.1-nano",
            messages=[
                {
                    "role": "system",
                    "content": (
                        "You answer questions about a Nike PDF using only provided context. "
                        "If context is insufficient, say so briefly. Keep the answer concise."
                    ),
                },
                {
                    "role": "user",
                    "content": prompt,
                }
            ]
        )
        self.user_response = response.choices[0].message.content.strip()
        self.last_responses.append(self.user_response)
        self.last_questions.append(self.user_query)
        return self.user_response
