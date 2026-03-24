from services.retrieval_service import RetrievalService
from services.llm_service import LLMService

retriever = RetrievalService()
llm = LLMService()

question = "Who is the manager?"

chunks = retriever.retrieve(question)

answer = llm.generate_answer(question, chunks)

print("\nQUESTION:", question)

print("\nRETRIEVED CONTEXT:")
for c in chunks:
    print("-", c["chunk_text"])

print("\nFINAL ANSWER:")
print(answer)