from fastapi import FastAPI
from rag_pipeline import RAGChatbot
app = FastAPI()

chatbot = RAGChatbot("rag_data\\hamilton.json")

@app.get("/")
async def root():
    return {"message": "Hello World"}


@app.get("/hello/{name}")
async def say_hello(name: str):
    return {"message": f"Hello {name}"}

@app.post("/chat")
async def get_chat_response(question: str):
    response = chatbot.handle_query(question)
    return {"response": response}