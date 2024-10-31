# src/utils.py

import tiktoken


def chunk_paragraphs(paragraphs, max_tokens=7500, model="gpt-4"):
    """
    Splits paragraphs into chunks that are less than max_tokens when tokenized.
    """
    tokenizer = tiktoken.encoding_for_model(model)
    chunks = []
    current_chunk = []
    current_tokens = 0

    for p in paragraphs:
        p_text = p.text
        tokens = tokenizer.encode(p_text)
        num_tokens = len(tokens)
        # Check if adding the paragraph would exceed the max tokens
        if current_tokens + num_tokens <= max_tokens:
            current_chunk.append(p)
            current_tokens += num_tokens
        else:
            if current_chunk:
                chunks.append(current_chunk)
            current_chunk = [p]
            current_tokens = num_tokens

    if current_chunk:
        chunks.append(current_chunk)

    return chunks


def chunk_shapes(shapes_with_text, max_tokens=7500, model="gpt-4-turbo"):
    """
    Splits shapes into chunks that are less than max_tokens when tokenized.
    """
    tokenizer = tiktoken.encoding_for_model(model)
    chunks = []
    current_chunk = []
    current_tokens = 0

    for shape, text in shapes_with_text:
        tokens = tokenizer.encode(text)
        num_tokens = len(tokens)
        if current_tokens + num_tokens <= max_tokens:
            current_chunk.append((shape, text))
            current_tokens += num_tokens
        else:
            if current_chunk:
                chunks.append(current_chunk)
            current_chunk = [(shape, text)]
            current_tokens = num_tokens

    if current_chunk:
        chunks.append(current_chunk)

    return chunks
