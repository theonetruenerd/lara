import os
from typing import List
from sentence_transformers import SentenceTransformer, util
import torch
import json
from openai import OpenAI
import numpy as np

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
        self.conversation_history = []

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
        Retrieves the top-k relevant context snippets (metadata) based on the user's query.
        :param query: User query string.
        :param top_k: Number of relevant metadata snippets to retrieve.
        """

        # The index is expected to be a list of objects directly
        data = self.index  # Assuming the index is a list of JSON objects
        if not isinstance(data, list) or not data:
            raise ValueError("Index must be a non-empty list of JSON objects.")

        # Extract metadata and embeddings, validating the structure
        metadata_list = []
        embeddings = []

        for entry in data:
            # Verify that each entry contains the expected keys
            if not isinstance(entry, dict) or "id" not in entry or "metadata" not in entry or "embedding" not in entry:
                raise ValueError("Each index entry must contain 'id', 'metadata', and 'embedding' keys.")

            metadata = entry["metadata"]
            embedding = entry["embedding"]

            # Ensure `metadata` is a dictionary containing required fields
            if not isinstance(metadata, dict) or "title" not in metadata or "description" not in metadata:
                raise ValueError("Each 'metadata' must contain at least 'title' and 'description' keys.")

            # Extract metadata fields
            metadata_content = (
                f"Title: {metadata.get('title', 'No Title')}\n"
                f"Description: {metadata.get('description', 'No Description')}\n"
                f"Tags: {', '.join(metadata.get('tags', []))}\n"
                f"Documentation URL: {metadata.get('documentation_url', 'No URL')}"
            )
            metadata_list.append(metadata_content)

            # Validate embedding structure
            if not isinstance(embedding, list) or not all(isinstance(x, (int, float)) for x in embedding):
                raise ValueError("'embedding' must be a list of numeric values.")

            embeddings.append(embedding)

        # Convert embeddings to tensor
        embeddings_tensor = torch.tensor(embeddings, dtype=torch.float)

        # Ensure embeddings is a non-empty 2D tensor
        if embeddings_tensor.size(0) == 0 or embeddings_tensor.dim() != 2:
            raise ValueError("Embeddings must be a non-empty 2D array.")

        # Encode the query into the same format as the embeddings
        query_embedding = embedding_model.encode(query, convert_to_tensor=True)
        if isinstance(query_embedding, np.ndarray):  # Compatibility check
            query_embedding = torch.tensor(query_embedding, dtype=torch.float)

        # Handle case where top_k exceeds the number of available documents
        effective_k = min(top_k, len(metadata_list))

        # Calculate similarity scores
        similarities = util.pytorch_cos_sim(query_embedding, embeddings_tensor)[0]
        top_results = torch.topk(similarities, k=effective_k)

        # Collect results with metadata and similarity scores
        results = []
        for score, idx in zip(top_results[0], top_results[1]):
            results.append((metadata_list[idx], float(score)))

        return results

    def generate_response(self, query: str, context: str):
        """
        Generates the response using OpenAI API given the query and relevant context.
        :param query: The user's query.
        :param context: The relevant context retrieved.
        """
        prompt = f"You are an expert assistant with deep knowledge of liquid handling instruments. Use the following context to answer the user's query as precisely as possible:\n\n{context}\n\nQuery: {query}\n\nAnswer:"
        messages = [
            {"role": "system", "content": "You are a helpful and knowledgeable assistant."},
            {"role": "user", "content": prompt}
        ]

        for msg in self.conversation_history:
            messages.append({"role":msg["role"],"content":msg["content"]})

        messages.append({"role":"user","content":query})

        try:
            response = client.chat.completions.create(
                model="mistralai/devstral-small:free",
                messages=messages
            )
            response_content = response.choices[0].message.content
            self.conversation_history.append({"role":"user","content":query})
            self.conversation_history.append({"role":"assistant","content":response_content})

            max_history = 10
            if len(self.conversation_history) > max_history:
                self.conversation_history = self.conversation_history[-max_history:]

            return response_content

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

    def clear_history(self):
        """
        Clears the conversation history.
        :return:
        """
        self.conversation_history = []
        return "Conversation history cleared."


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
