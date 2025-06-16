import os
from typing import List
from sentence_transformers import SentenceTransformer, util
import torch
import json
from openai import OpenAI

client = OpenAI(
  base_url="https://openrouter.ai/api/v1",
    api_key=os.environ.get("LARA_KEY")
)
# Initialize the Embedding Model
EMBEDDING_MODEL = 'all-MiniLM-L6-v2'  # Change based on your GPU/CPU resources
embedding_model = SentenceTransformer(EMBEDDING_MODEL)


class RAGChatbot:
    def __init__(self, index_path: str):
        """
        Initializes the RAG Chatbot.
        :param index_path: Path to JSON file containing the index of documents.
        """
        self.index = self.load_index(index_path)

    @staticmethod
    def load_index(index_path: str):
        """
        Loads the document index for retrievals.
        :param index_path: Path to document index.
        """
        if not os.path.exists(index_path):
            raise FileNotFoundError(f"Index file not found at {index_path}")

        with open(index_path, 'r', encoding='utf-8') as f:
            return json.load(f)

    def retrieve_context(self, query: str, top_k: int = 5):
        """
        Retrieves the top-k relevant context snippets based on user query.
        :param query: User query string.
        :param top_k: Number of relevant snippets to retrieve.
        """
        # Ensure that the index contains both documents and embeddings
        if "documents" not in self.index or "embeddings" not in self.index:
            raise ValueError("Index must contain both 'documents' and 'embeddings'.")

        docs = self.index["documents"]
        embeddings = self.index["embeddings"]

        # Ensure embeddings and docs have the same length
        if len(docs) != len(embeddings):
            raise ValueError(
                f"Mismatch between number of documents ({len(docs)}) "
                f"and embeddings ({len(embeddings)})."
            )

        # Handle empty documents list
        if not docs:
            return []

        # Encode the query
        query_embedding = embedding_model.encode(query, convert_to_tensor=True)
        doc_embeddings = torch.tensor(embeddings)

        # Handle case where top_k is greater than the number of documents
        effective_k = min(top_k, len(docs))

        # Calculate similarity scores
        similarities = util.pytorch_cos_sim(query_embedding, doc_embeddings)[0]
        top_results = torch.topk(similarities, k=effective_k)

        # Collect results
        results = []
        for score, idx in zip(top_results[0], top_results[1]):
            results.append((docs[idx], float(score)))
        return results

    @staticmethod
    def generate_response(query: str, context: str):
        """
        Generates the response using OpenAI API given the query and relevant context.
        :param query: The user's query.
        :param context: The relevant context retrieved.
        """
        prompt = f"You are an expert assistant with deep knowledge of liquid handling instruments. Use the following context to answer the user's query as precisely as possible:\n\n{context}\n\nQuery: {query}\n\nAnswer:"

        try:
            response = client.chat.completions.create(
                model="mistralai/devstral-small:free",
                messages=[
                    {"role": "system", "content": "You are a helpful and knowledgeable assistant."},
                    {"role": "user", "content": prompt}
                ]
            )
            return response.choices[0].message.content
        except Exception as e:
            print(f"Error generating response: {e}")
            return "I'm sorry, I encountered an issue generating the response."

    def handle_query(self, query: str):
        """
        Handles the entire RAG pipeline for a query.
        :param query: User's query.
        """
        # Step 1: Retrieve relevant context
        relevant_docs = self.retrieve_context(query)
        context = "\n".join([f"Document {i + 1}: {doc[0]}" for i, doc in enumerate(relevant_docs)])

        # Step 2: Generate response
        response = self.generate_response(query, context)
        return response


# Utility functions
def build_index(documents: List[str], output_path: str):
    """
    Builds an embedding-based index for retrieval.
    :param documents: List of document strings for indexing.
    :param output_path: Path to save the index JSON file.
    """
    # Create embeddings for documents
    embeddings = embedding_model.encode(documents, convert_to_tensor=False)

    # Save the index
    data = {"documents": documents, "embeddings": embeddings.tolist()}
    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=4)
    print(f"Index created and saved to {output_path}")


if __name__ == "__main__":
    index_file = "hamilton.json"

    # Initialize the chatbot
    chatbot = RAGChatbot(index_file)

    # Example Query
    user_query = "How would I go about debugging 0xa1230029"
    response = chatbot.handle_query(user_query)
    print("Chatbot Response:", response)
