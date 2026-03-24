from llama_cpp import Llama

MODEL_PATH = "models/mistral.gguf"


class LLMService:

    def __init__(self):

        self.llm = Llama(
            model_path=MODEL_PATH,
            n_ctx=4096,
            n_threads=6
        )

    def generate_answer(self, question, chunks):

        context = "\n".join([c["chunk_text"] for c in chunks])

        prompt = f"""
You are an assistant that answers questions ONLY from the provided context.

Context:
{context}

Question:
{question}

If the answer is not present in the context, respond exactly with:
No answer for your question in the uploaded data

Answer:
"""

        response = self.llm(
            prompt,
            max_tokens=200,
            temperature=0.2
        )

        return response["choices"][0]["text"].strip()