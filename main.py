from langchain_ollama.llms import OllamaLLM
from langchain_core.prompts import ChatPromptTemplate
from vector import retriever

model = OllamaLLM(model="deepseek-r1:1.5b")

template = """
You are an expert in answering questions about compliance services for various industries.

Here are some relevant details about the services: {services}

Here is the question to answer: {question}
"""
prompt = ChatPromptTemplate.from_template(template)
chain = prompt | model

while True:
    print("\n\n-------------------------------")
    question = input("Ask your question (q to quit): ")
    print("\n\n")
    if question == "q":
        break
    
    services = retriever.invoke(question)
    result = chain.invoke({"services": services, "question": question})
    print(result)
