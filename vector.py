from langchain_ollama import OllamaEmbeddings
from langchain_chroma import Chroma
from langchain_core.documents import Document
import os
import pandas as pd

# Load your knowledge base in the same way (you can adapt this based on actual data input location)
df = pd.read_json("Tunning.jsonl", lines=True)

# Initialize embeddings model
embeddings = OllamaEmbeddings(model="deepseek-r1:1.5b")

# Set up database location
db_location = "./chrome_langchain_db"
add_documents = not os.path.exists(db_location)

# Add documents if they are not already added
if add_documents:
    documents = []
    ids = []

    # Loop through the rows of the data
    for i, row in df.iterrows():
        # Build the document based on the knowledge base context
        document = Document(
            page_content=row["contents"][0]["parts"][0]["text"] + " " + row["contents"][1]["parts"][0]["text"],  # User query and model response
            metadata={"service": row["contents"][1]["parts"][0]["text"]},  # Metadata can store other relevant info like service, features, etc.
            id=str(i)
        )
        ids.append(str(i))
        documents.append(document)

# Initialize Chroma vector store (always, regardless of add_documents)
vector_store = Chroma(
    collection_name="compliance_services",
    persist_directory=db_location,
    embedding_function=embeddings
)

# Add documents to the vector store if needed
if add_documents:
    vector_store.add_documents(documents=documents, ids=ids)

# Set up retriever for querying
retriever = vector_store.as_retriever(
    search_kwargs={"k": 5}  # You can adjust "k" based on how many results you want to retrieve
)
