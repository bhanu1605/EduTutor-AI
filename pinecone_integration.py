
import pinecone
from langchain.embeddings import OpenAIEmbeddings

# Initialize Pinecone
pinecone.init(api_key="YOUR_PINECONE_API_KEY", environment="YOUR_PINECONE_ENV")
index_name = "edututor-user-profiles"

# Create index if not exists
if index_name not in pinecone.list_indexes():
    pinecone.create_index(name=index_name, dimension=1536)

index = pinecone.Index(index_name)

# Example: Store user profile embedding
def store_user_profile(user_id, profile_text):
    embeddings = OpenAIEmbeddings()
    embedding_vector = embeddings.embed_query(profile_text)
    index.upsert([(user_id, embedding_vector)])

# Example: Update quiz metadata
def update_quiz_metadata(user_id, quiz_metadata):
    # Store metadata separately or include in Pinecone metadata
    index.update(id=user_id, set_metadata=quiz_metadata)

# Example: Fetch student progress
def fetch_student_progress(user_id):
    result = index.fetch([user_id])
    return result

if __name__ == "__main__":
    # Example usage
    store_user_profile("user123", "John Doe likes math and science.")
    update_quiz_metadata("user123", {"last_score": 85, "topic": "Algebra", "date": "2025-06-30"})
    progress = fetch_student_progress("user123")
    print(progress)
