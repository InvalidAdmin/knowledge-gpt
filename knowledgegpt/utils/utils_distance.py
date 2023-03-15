# https://github.com/openai/openai-cookbook/blob/main/examples/Question_answering_using_embeddings.ipynb sourced from here
import numpy as np
from knowledgegpt.utils.utils_embedding import get_hf_embeddings, get_embedding

def vector_similarity(x: list[float], y: list[float]) -> float:
    """
    Returns the similarity between two vectors.
    
    Because OpenAI Embeddings are normalized to length 1, the cosine similarity is the same as the dot product.
    :param x: The first vector.
    :param y: The second vector.
    :return: The similarity between the two vectors.
    """
    return np.dot(np.array(x), np.array(y))

def order_document_sections_by_query_similarity(query: str,  contexts: dict[(str, str), np.array], embedding_type:str = "hf", model_lang:str='en') -> list[(float, (str, str))]:
    """
    Find the query embedding for the supplied query, and compare it against all of the pre-calculated document embeddings
    to find the most relevant sections. 
    
    Return the list of document sections, sorted by relevance in descending order.
    :param query: The query to answer.
    :param contexts: The embeddings of the document sections.
    :param embedding_type: The type of embedding used. Can be "hf" or "tf".
    :param model_lang: The language of the model. Can be "en" or "tr".
    :return: The list of document sections, sorted by relevance in descending order.
    """

    print("model_lang", model_lang)
    if embedding_type == "hf":
        query_embedding = get_hf_embeddings(query, model_lang)
    else:
        query_embedding = get_embedding(query)

    document_similarities = sorted([
        (vector_similarity(query_embedding, doc_embedding), doc_index) for doc_index, doc_embedding in contexts.items()
    ], reverse=True)
    
    return document_similarities