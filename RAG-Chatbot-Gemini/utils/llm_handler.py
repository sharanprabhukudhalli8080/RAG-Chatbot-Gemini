import os
import google.generativeai as genai
from dotenv import load_dotenv

load_dotenv()

genai.configure(
    api_key=os.getenv("GOOGLE_API_KEY")
)

MODEL_NAME = "gemini-2.5-flash"


def get_answer(question, vector_db, history=None):

    retriever = vector_db.as_retriever(
        search_kwargs={"k": 5}
    )

    docs = retriever.invoke(question)

    context = "\n".join(
        [doc.page_content for doc in docs]
    )

    history_context = ""

    if history:

        for chat in history[-5:]:

            history_context += (
                f"User: {chat['question']}\n"
            )

            history_context += (
                f"Assistant: {chat['answer']}\n"
            )

    prompt = f"""
You are an intelligent PDF assistant.

Rules:
1. Answer ONLY using the provided document context.
2. If the answer is not present in the context, reply:
   "I could not find that information in the uploaded PDF."
3. Use conversation history only for understanding follow-up questions.
4. Be concise and accurate.

Conversation History:
{history_context}

Document Context:
{context}

Question:
{question}

Answer:
"""

    model = genai.GenerativeModel(
        MODEL_NAME
    )

    response = model.generate_content(
        prompt
    )

    answer = response.text.strip()

    return answer, docs