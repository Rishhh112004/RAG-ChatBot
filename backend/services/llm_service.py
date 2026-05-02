# from llama_cpp import Llama

# MODEL_PATH = "models/mistral.gguf"


# class LLMService:

#     def __init__(self):

#         self.llm = Llama(
#             model_path=MODEL_PATH,
#             n_ctx=4096,
#             n_threads=6
#         )

#     def generate_answer(self, question, chunks, chat_history=None):

#         if len(chunks) > 1:
#             context = "\n".join([c["chunk_text"] for c in chunks[:2]])
#         else:
#             context = chunks[0]["chunk_text"]

#         prompt = f"""
#     You are a strict information extraction system.

#     Rules:
#     - Extract ONLY from given context
#     - Do NOT assume or guess anything

#     - Return numbers EXACTLY as written
 
#     - Return only the final answer

    
#     Output format rules:
#     1. If one direct answer exists:
#     Return one short sentence only
#     2. If multiple exact answers exist:
#     Return in bullet points
#     3. If answer is missing:
#     Return exactly:
#     No relevant information found


#     Context:
#     {context}

#     Question:
#     {question}

#     Answer (ONLY extracted facts):
#     """

#         response = self.llm(
#             prompt,
#             max_tokens=120,
#             temperature=0.0
#         )

#         return response["choices"][0]["text"].strip()
    
    
#     #     - If answer is not clearly present, say: "No relevant information found"
#     #    - Do NOT add notes, disclaimers, or reasoning for the answer in the end of the response
#     #     - DO NOT invent or guess


# import re
# from llama_cpp import Llama

# MODEL_PATH = "models/mistral.gguf"


# class LLMService:

#     def __init__(self):
#         self.llm = Llama(
#             model_path=MODEL_PATH,
#             n_ctx=4096,
#             n_threads=6
#         )

#     def generate_answer(self, question: str, chunks: list, chat_history=None) -> str:
#         """
#         Generate a precise answer strictly from retrieved context chunks.

#         Key fixes vs original:
#         1. Uses ALL retrieved chunks, not just top 2
#         2. Each chunk is numbered so the model can reference them clearly
#         3. Prompt uses proper Mistral [INST]...[/INST] format
#         4. max_tokens raised to 300 (list answers need more room than 120)
#         5. Stop tokens prevent the model from generating follow-up questions
#         6. Post-processing strips common LLM filler phrases
#         """

#         if not chunks:
#             return "No relevant information found in the uploaded documents."

#         # Build numbered context from ALL retrieved chunks
#         context_parts = []
#         for i, chunk in enumerate(chunks, 1):
#             context_parts.append(f"[Chunk {i}]\n{chunk['chunk_text']}")
#         context = "\n\n".join(context_parts)

#         prompt = f"""<s>[INST] You are a precise question-answering assistant.
# Your ONLY job is to extract and return information from the context below.

# STRICT RULES:
# - Answer ONLY using information present in the context
# - Do NOT add explanations, reasoning, or disclaimers
# - Do NOT say "based on the context" or "according to the document"
# - Return names, numbers, and dates EXACTLY as written in the context
# - If the answer is a list, return each item on its own line
# - If the answer is not in the context, return exactly:
#   Not found in uploaded documents.

# CONTEXT:
# {context}

# QUESTION:
# {question}

# ANSWER: [/INST]"""

#         response = self.llm(
#             prompt,
#             max_tokens=300,
#             temperature=0.0,
#             # Stop generation if the model starts a new question or prompt
#             stop=["[INST]", "</s>", "\nQuestion:", "\nQ:"]
#         )

#         answer = response["choices"][0]["text"].strip()

#         # Strip common LLM filler phrases that leak through despite instructions
#         filler_patterns = [
#             r"^Based on the (context|provided information|above)[,.]?\s*",
#             r"^According to the (context|document|text)[,.]?\s*",
#             r"^The (context|document|text) (states|mentions|says|indicates)[,:]?\s*",
#             r"^From the (context|provided)[,.]?\s*",
#         ]
#         for pattern in filler_patterns:
#             answer = re.sub(pattern, "", answer, flags=re.IGNORECASE).strip()

#         return answer


# import re
# from llama_cpp import Llama

# MODEL_PATH = "models/mistral.gguf"

# class LLMService:

#     def __init__(self):
#         self.llm = Llama(
#             model_path=MODEL_PATH,
#             n_ctx=4096,
#             n_threads=6,
#             repeat_penalty=1.1      # discourages the model from repeating Q/A patterns
#         )

#     def generate_answer(self, question: str, chunks: list, chat_history=None) -> str:

#         if not chunks:
#             return "Not found in uploaded documents."

#         # Build numbered context from ALL retrieved chunks
#         context_parts = []
#         for i, chunk in enumerate(chunks, 1):
#             context_parts.append(f"[Chunk {i}]\n{chunk['chunk_text']}")
#         context = "\n\n".join(context_parts)

#         prompt = f"""<s>[INST] You are a precise question-answering assistant.
# Extract and return the answer from the context below.

# RULES — follow exactly:
# - Use ONLY information from the context. Nothing else.
# - Do NOT generate additional questions or answers after your response.
# - Do NOT use "QUESTION:" or "ANSWER:" labels in your response.
# - Do NOT say "based on the context" or "according to the document".
# - Return names, numbers, dates EXACTLY as written.
# - If the answer is a list, return each item on its own line with a dash prefix.
# - If the answer is not present, return only: Not found in uploaded documents.

# CONTEXT:
# {context}

# QUESTION:
# {question}

# ANSWER (one response only, then stop): [/INST]"""

#         response = self.llm(
#             prompt,
#             max_tokens=300,
#             temperature=0.0,
#             stop=["[INST]", "</s>", "\nQUESTION", "\nQuestion", "\nQ:", "ANSWER:"]
#         )

#         answer = response["choices"][0]["text"].strip()

#         # Strip common LLM filler phrases that leak through
#         filler_patterns = [
#             r"^Based on the (context|provided information|above)[,.]?\s*",
#             r"^According to the (context|document|text)[,.]?\s*",
#             r"^The (context|document|text) (states|mentions|says|indicates)[,:]?\s*",
#             r"^From the (context|provided)[,.]?\s*",
#         ]
#         for pattern in filler_patterns:
#             answer = re.sub(pattern, "", answer, flags=re.IGNORECASE).strip()

#         return answer



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

        # Build numbered context from ALL retrieved chunks
        context_parts = []
        for i, chunk in enumerate(chunks, 1):
            context_parts.append(f"[Chunk {i}]\n{chunk['chunk_text']}")
        context = "\n\n".join(context_parts)

        prompt = f"""<s>[INST] You are a precise question-answering assistant.
Extract and return the answer from the context below.

RULES:
- Answer ONLY using information present in the context. Nothing else.
- Do NOT generate additional questions or answers after your response.
- Do NOT use "QUESTION:" or "ANSWER:" labels in your response.
- Do NOT say "based on the context" or "according to the document".
- Do NOT add explanations or reasoning after your answer.
- Return names, numbers, dates, and URLs EXACTLY as written in the context.
- If the context contains a link or URL relevant to the question, return it as the answer.
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

        # Strip common LLM filler phrases
        filler_patterns = [
            r"^Based on the (context|provided information|above)[,.]?\s*",
            r"^According to the (context|document|text)[,.]?\s*",
            r"^The (context|document|text) (states|mentions|says|indicates)[,:]?\s*",
            r"^From the (context|provided)[,.]?\s*",
        ]
        for pattern in filler_patterns:
            answer = re.sub(pattern, "", answer, flags=re.IGNORECASE).strip()

        # Remove any trailing parenthetical reasoning the model adds
        # e.g. "(for completeness, but not required): Not found..."
        answer = re.sub(r'\s*\(for completeness.*$', '', answer,
                        flags=re.IGNORECASE | re.DOTALL).strip()

        return answer