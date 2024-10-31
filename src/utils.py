# src/utils.py

import tiktoken


def chunk_text(text, max_tokens=7500):
    """
    Splits text into chunks that are less than max_tokens when tokenized.
    """
    # Initialize tokenizer for the GPT-4 model
    tokenizer = tiktoken.encoding_for_model("gpt-4")
    tokens = tokenizer.encode(text)
    chunks = []
    for i in range(0, len(tokens), max_tokens):
        chunk = tokenizer.decode(tokens[i : i + max_tokens])
        chunks.append(chunk)
    return chunks
