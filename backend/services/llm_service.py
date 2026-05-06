import re
from llama_cpp import Llama

MODEL_PATH = "models/mistral.gguf"


class LLMService:

    def __init__(self):
        self.llm = Llama(
            model_path=MODEL_PATH,
            n_ctx=4096,
            n_threads=6,
            repeat_penalty=1.1
        )

    def generate_answer(self, question: str, chunks: list, chat_history=None) -> str:

        if not chunks:
            return "Not found in uploaded documents."

        context = "\n---\n".join(chunk["chunk_text"] for chunk in chunks)

        prompt = f"""<s>[INST] You are a precise question-answering assistant.
Extract and return the answer from the context below.

RULES — follow exactly:
- Use ONLY information from the context. Nothing else.
- Do NOT reference or mention the context, chunks, or source in your answer.
- Do NOT use phrases like "From Chunk", "Chunk 1", "the context says", "mentioned that".
- Do NOT generate additional questions or answers after your response.
- Do NOT use "QUESTION:" or "ANSWER:" labels in your response.
- Return names, numbers, dates, and URLs EXACTLY as written in the context.
- If the answer is a list, return each item on its own line with a dash prefix.
- If the answer is truly not present in the context, return only:
  Not found in uploaded documents.

CONTEXT:
{context}

QUESTION:
{question}

ANSWER: [/INST]"""

        response = self.llm(
            prompt,
            max_tokens=300,
            temperature=0.0,
            stop=[
                "[INST]", "</s>",
                "\nQUESTION", "\nQuestion", "\nQ:",
                "ANSWER:", "\nANSWER",
                "(for completeness", "but not required"
            ]
        )

        answer = response["choices"][0]["text"].strip()

        cleanup_patterns = [

            r'\[Chunk\s*\d+\]\s*(mentioned|states?|says?|indicates?|noted?)?\s*(that\s*)?',

            r'\(From Chunk[^)]*\)',

            r'From Chunk\s*[\d\s,and]+[,.]?\s*',

            r'\[Chunk\s*\d+\]\s*',

            r'^Based on the (context|provided information|above)[,.]?\s*',
            r'^According to the (context|document|text)[,.]?\s*',
            r'^The (context|document|text) (states|mentions|says|indicates)[,:]?\s*',
            r'^From the (context|provided)[,.]?\s*',

            r'\s*\(for completeness.*$',
        ]

        for pattern in cleanup_patterns:
            answer = re.sub(pattern, "", answer, flags=re.IGNORECASE | re.DOTALL).strip()

        return answer