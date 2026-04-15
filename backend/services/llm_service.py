from llama_cpp import Llama

MODEL_PATH = "models/mistral.gguf"


class LLMService:

    def __init__(self):

        self.llm = Llama(
            model_path=MODEL_PATH,
            n_ctx=4096,
            n_threads=6
        )

    def generate_answer(self, question, chunks, chat_history=None):

        context = "\n".join([c["chunk_text"] for c in chunks])
        # context = chunks[0]["chunk_text"]
        
        history = ""
        if chat_history:
            for q, a in chat_history[-2:]:
                history += f"User: {q}\nAssistant: {a}\n"


        prompt = f"""
You are an assistant that answers questions ONLY from the provided context.

Give precise answer
Do NOT explain extra details

Chat History:
{history}

Context:
{context}

Question:
{question}

If the answer is not present in the context, respond exactly with:
No answer for your question in the uploaded data

Answer (short and precise):
"""

        response = self.llm(
            prompt,
            # max_tokens=200,
            # temperature=0.2
            max_tokens=80-120,
            temperature=0.1-0.2            
        )

        return response["choices"][0]["text"].strip()
    
    
# few other rules which could be used
# 1. You are a strict question-answering system.
#   Rules:
#       - Answer ONLY what is asked
#       - Be concise and to the point
#       - Do NOT explain extra details
#       - Do NOT repeat full paragraphs
#       - Extract the exact answer from context