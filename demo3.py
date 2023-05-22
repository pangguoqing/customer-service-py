
from pyexpat import model
from langchain.prompts.example_selector import SemanticSimilarityExampleSelector
from langchain.vectorstores import FAISS
from langchain.embeddings import OpenAIEmbeddings
from langchain.prompts import FewShotPromptTemplate, PromptTemplate
from langchain.llms import OpenAI

import openai
openai.api_key='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'

text = '我是谁'
model = "text-embedding-ada-002"

emb_req =  openai.Embedding.create(input=[text], model=model)

emb = emb_req.data[0].embedding

print(len(emb))


print(emb_req.data)