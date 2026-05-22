import asyncio

import aioconsole

from chunker import chunker
from embeddor import embeddor
from generator import generator
from loader import loader
from vectorstore import vectorstore


async def main():
    doc_loader = loader("./source/doc.pdf")
    doc_chunker = chunker(doc_loader.documents)
    doc_embeddor = embeddor(data_chunks=doc_chunker.chunked_data)
    doc_vectorstore = vectorstore(
        embedding_model=doc_embeddor.embeddings_model,
        data_chunks=doc_chunker.chunked_data,
    )

    question_counter = 0
    while True:
        user_input = await aioconsole.ainput("Ask question about nike docs (q to quit): ")
        cleaned_input = user_input.strip()

        if cleaned_input.lower() in {"q", "quit"}:
            break

        if len(cleaned_input) <= 5:
            print("Redo question, too short")
            continue

        question_counter += 1
        print(f"Question #{question_counter}")

        rag_generator = generator(
            user_query=cleaned_input,
            vector_store=doc_vectorstore.vector_store,
        )
        rag_generator.similarity_search(k=3)
        final_answer = rag_generator.llmgeneration()
        print(final_answer)


if __name__ == "__main__":
    asyncio.run(main())
