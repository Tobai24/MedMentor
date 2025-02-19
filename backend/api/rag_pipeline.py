import os
from pinecone import Pinecone
from dotenv import load_dotenv
from sentence_transformers import CrossEncoder
from langchain_openai import OpenAIEmbeddings, OpenAI

load_dotenv()

OPENAI_API_KEY = os.environ.get("OPENAI_API_KEY")
EMBEDDINGS = OpenAIEmbeddings(api_key=os.environ["OPENAI_API_KEY"])
PINECONE_API_KEY = os.getenv("PINECONE_API_KEY")

pc = Pinecone(api_key=PINECONE_API_KEY)
index = pc.Index("final")

def get_query_embeddings(query: str) -> list[float]:
    query_embeddings = EMBEDDINGS.embed_query(query)
    return query_embeddings

def query_pinecone_index(
    query_embeddings: list, top_k: int = 20, include_metadata: bool = True
) -> dict[str, any]:
    query_response = index.query(
        vector=query_embeddings, top_k=top_k, include_metadata=include_metadata
    )
    return query_response

reranker = CrossEncoder("cross-encoder/ms-marco-MiniLM-L-6-v2")

def rerank_documents(query, retrieved_docs):
    
    pairs = []
    doc_list = []

    for doc in retrieved_docs["matches"]:
        text = doc["metadata"].get("page_content") 
        # if text is None:
        #     print(f"Warning: Missing 'page_content' in metadata for document ID {doc['metadata'].get('id', 'Unknown')}")
        #     continue 
        
        pairs.append((query, text))
        doc_list.append(doc)

    if not pairs:
        print("No valid documents found for reranking.")
        return []

    scores = reranker.predict(pairs)

    scored_docs = list(zip(scores, doc_list))
    scored_docs.sort(key=lambda x: x[0], reverse=True)
    reranked_docs = [doc for _, doc in scored_docs]
    
    return reranked_docs

def retreival(q):
    query_text = q['question']
    embeddings = get_query_embeddings(query_text)
    retrieved_results = query_pinecone_index(embeddings, top_k=30)
    reranked_results = rerank_documents(query_text, retrieved_results)
    return reranked_results

def build_prompt(system, search_results):
   
   context = ""
    
    # reduce the length of the search result to include in the prompt because of the context length
   for doc in search_results[:10]:
      context = context + f"content: {doc["metadata"]["page_content"]}\n\n"
      
   prompt_template = f"""You are a medical educator tasked with creating a **clinical case scenario** for an OSCE (Objective Structured Clinical Examination). Your goal is to generate a realistic and detailed case prompt based on the provided **body system/clinical case** and the **context** from the medical database. 
   The case prompt should be suitable for medical students and adhere to OSCE standards for history taking and physical examination.

   ### Instructions:
   1. **Understand the Body System/Clinical Case**:
      - Carefully analyze the provided body system or clinical topic: `{system}`.
      - Consider common pathologies, presentations, and examination techniques related to this system.

   2. **Incorporate Context from the Database**:
      - Use the provided context: `{context}` to ensure the case prompt is grounded in realistic clinical details.
      - Ensure the case aligns with the context while maintaining educational value.

   3. **Generate a Realistic Case Prompt**:
      - The case prompt should include **only the presenting complaint** (e.g., "A 45-year-old male presents with chest pain for 2 hours").
      - Do not include additional history, examination findings, or diagnosis in the prompt.
      - Ensure the complaint is specific, clinically relevant, and appropriate for the given body system.

   4. **Adhere to OSCE Standards**:
      - The case prompt should mimic a real OSCE station, requiring the student to:
      - Take a focused history.
      - Perform a relevant physical examination.
      - Develop a differential diagnosis.
      - Avoid providing excessive details that would make the case too easy or unrealistic.

   5. **Ensure Educational Value**:
      - The case should challenge the student’s clinical reasoning and knowledge.
      - It should be appropriate for the level of a medical student (e.g., not overly complex or obscure).

   ### Input:
   - **Body System/Clinical Case**: {system}
   - **Context from Database**: {context}

   ### Expected Output just text:
   A concise and realistic case prompt based on the body system and context, including only the presenting complaint (e.g., 'A 35-year-old female presents with shortness of breath and fever for 3 days').
   Generate only the case prompt as a single plain text sentence. Do not return JSON, code blocks, or any formatting.
   """.strip()
   
   prompt = prompt_template
   
   return prompt

from openai import OpenAI

client = OpenAI()

def llm(prompt, model='gpt-4o'):
    response = client.chat.completions.create(
        model=model,
        messages=[{"role": "user", "content": prompt}]
    )
    
    return response.choices[0].message.content

def rag(query: dict, model='gpt-4o-mini') -> str:
    search_results = retreival(query)
    prompt = build_prompt(query['question'], search_results)
    answer = llm(prompt, model=model)
    return answer