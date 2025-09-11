from langchain.chains import RetrievalQA
from langchain.docstore.document import Document
from langchain.prompts import PromptTemplate
from langchain_community.chat_models import ChatOllama
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_community.vectorstores import Chroma
from langchain.callbacks.streaming_aiter import AsyncIteratorCallbackHandler

import asyncio
# Embedding + DB Setup
embedding = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")

docs = [
    Document(page_content="Our return policy allows returns within 30 days."),
    Document(page_content="Shipping is free for orders above $50."),
    Document(page_content="Red Summer Dress – $45."),
    Document(page_content="Blue Denim Jacket – $89."),
]

db = Chroma.from_documents(docs, embedding, persist_directory='db')
db.persist()

# LLM Setup
llm = ChatOllama(model="mistral")

# Prompt Template
template = """
You are a helpful assistant for a fashion business. 
Answer customer questions using the context provided.

Context: {context}
Question: {question}
Answer:"""

prompt = PromptTemplate(template=template, input_variables=["context", "question"])

qa = RetrievalQA.from_chain_type(
    llm=llm,
    retriever=db.as_retriever(search_kwargs={"k": 2}),
    chain_type="stuff",
    chain_type_kwargs={"prompt": prompt}
)


def get_replay(query: str) -> str:
    return qa.run(query)


async def stream_replay(query: str):
    callback = AsyncIteratorCallbackHandler()

    llm = ChatOllama(model="mistral", callbacks=[callback], streaming=True)

    qa = RetrievalQA.from_chain_type(
        llm=llm,
        retriever=db.as_retriever(search_kwargs={"k": 2}),
        chain_type="stuff",
        chain_type_kwargs={"prompt": prompt},
    )

    # Start async execution
    task = asyncio.create_task(qa.acall({"query": query}))

    # Yield tokens as they come
    async for token in callback.aiter():
        yield token

    await task