from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from rag_pipeline import RAGChatbot

app = FastAPI()

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],  # React app default port
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

chatbot = RAGChatbot("rag_data\\hamilton.json")

class ChatRequest(BaseModel):
    message: str

@app.post("/chat")
async def get_chat_response(request: ChatRequest):
    response = chatbot.handle_query(request.message)
    return {"response": response}