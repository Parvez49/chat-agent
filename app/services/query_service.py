import asyncio

from langchain.callbacks.streaming_aiter import AsyncIteratorCallbackHandler
from langchain.chains import RetrievalQA
from langchain.docstore.document import Document
from langchain.prompts import PromptTemplate
from langchain_community.chat_models import ChatOllama
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_community.vectorstores import Chroma

# Embedding + DB Setup
embedding = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")

docs = [
    Document(page_content="We specialize in sweaters, knitwear, and woven apparel, but we can also support categories like outerwear, activewear, and fashion accessories depending on your needs."),
    Document(page_content="Yes, unlike traditional manufacturers, we accept small-to-medium order quantities to support emerging brands and testing new collections."),
    Document(page_content="You can share sketches, tech packs, or even mood boards. Our design & sampling team will translate them into knitdowns, CADs, and samples. We also provide AI design assistance for faster development."),
    Document(page_content="Typically, brands go through 2–3 rounds of samples. We allow iterative improvements until you are satisfied."),
    Document(page_content="Pricing is based on yarn/fabric cost, trims, labor (CM), and order volume. We provide transparent costing breakdowns so you understand exactly where your money goes."),
    Document(page_content="Yes, we can quote both FOB (Free on Board) and LDP (Landed Duty Paid) depending on your preference."),
    Document(page_content="Development samples: 2–3 weeks. Bulk production: 60–90 days depending on complexity, material sourcing, and order size."),
    Document(page_content="Our partner factories collectively produce over 500,000 units per month, with flexibility to allocate capacity for both small and large brands."),
    Document(page_content="We follow AQL (Acceptable Quality Level) standards and have in-line + final inspections. You will also receive digital QC reports with photos and defect analysis."),
    Document(page_content="We proactively fix issues before shipment. If a defect is identified after shipping, we offer replacement or compensation depending on the contract."),
    Document(page_content="Yes, we work with factories that are BSCI, SEDEX, WRAP, OEKO-TEX, GRS, and Higg Index certified. We prioritize ethical and sustainable sourcing"),
    Document(page_content="Yes, we can source organic cotton, recycled polyester, sustainable viscose, and other eco-friendly materials upon request."),
    Document(page_content="You’ll have access to a digital order management dashboard showing live updates on sampling, production, QC, and shipping milestones."),
    Document(page_content="Yes, you’ll receive immediate alerts if there are any risks to the timeline, along with proposed solutions."),
    Document(page_content="We support FOB, CIF, and LDP shipping. Our logistics team can help with freight forwarding and customs clearance if needed."),
    Document(page_content="Yes, we can arrange dropshipping and warehouse fulfillment services, especially for smaller brands or online retailers."),
    Document(page_content="We lock in material costs upon PO confirmation to minimize risk for you. For volatile markets, we recommend early booking."),
    Document(page_content="We maintain buffer time in production schedules and can shift capacity between partner factories to meet deadlines."),
]

db = Chroma.from_documents(docs, embedding, persist_directory='db')
db.persist()

# LLM Setup
llm = ChatOllama(model="mistral")

# Prompt Template
template = """
you are sourcing and manufacturing specialist, here to simplify apparel sourcing. I help you move from design concept to final shipment by connecting you with reliable factories, managing samples, ensuring quality, and providing transparency at every stage. 
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
