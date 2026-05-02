from backend.services.db_service import DBService
import re

def process_uploads():
    db = DBService()
    data = db.get_all_paragraphs()
    chunks = []
    for item in data:
        text = item["text"]
        upload_id = str(item["_id"])
        timestamp = item["timestamp"]
        item_chunks = chunk_text(text, upload_id, timestamp)
        chunks.extend(item_chunks)
    return chunks

def chunk_text(text, upload_id, timestamp):
    """
    Smart chunking with colon-header merging.

    Key fix: when a prose sentence ends with ':' or ': -' and the
    next block is a list, they are merged into ONE chunk so the
    header context and the list items are always retrieved together.

    Example (DOC 7):
        "MOIL produces and sells different grades. They are: -
         High Grade Ores for production of Ferro manganese
         Medium grade ore..."
    Without merging: header → prose chunk, grades → separate chunk.
    With merging: both → single chunk → LLM sees complete answer.
    """
    chunks = []

    # Split into logical blocks on blank lines
    blocks = re.split(r'\n\s*\n', text)
    blocks = [b.strip() for b in blocks if b.strip()]

    # Merge a block ending with ':' with the next block
    merged_blocks = []
    i = 0
    while i < len(blocks):
        block = blocks[i]
        # Check if this block ends with a colon (header introducing a list)
        stripped = block.rstrip()
        if (stripped.endswith(':') or stripped.endswith(': -') or stripped.endswith(':-')) \
                and i + 1 < len(blocks):
            # Merge with next block
            merged_blocks.append(block + "\n" + blocks[i + 1])
            i += 2
        else:
            merged_blocks.append(block)
            i += 1

    for block in merged_blocks:
        block = block.strip()
        if not block:
            continue

        lines = block.splitlines()

        # Also treat newline-only separated items (no bullets) as structured
        # if the block has 3+ short lines — typical for uploaded plain lists
        structured = _is_structured_block(lines)

        if structured:
            entry_chunks = _split_structured_block(lines, upload_id, timestamp)
            chunks.extend(entry_chunks)
        else:
            prose_chunks = _split_prose(block, upload_id, timestamp)
            chunks.extend(prose_chunks)

    return chunks

def _is_structured_block(lines):
    """
    Detect structured blocks: bullets, numbered lists, key:value, or
    plain newline-separated short items (3+ lines, avg length < 120 chars).
    """
    non_empty = [l.strip() for l in lines if l.strip()]
    if len(non_empty) < 2:
        return False

    structured_count = 0
    for line in non_empty:
        if (re.match(r'^[•·●◦▪\-\*]\s', line) or
                re.match(r'^\d+[\.\)]\s', line) or
                (': ' in line and len(line) < 400)):
            structured_count += 1

    if structured_count >= len(non_empty) * 0.5:
        return True

    # Plain newline-separated list: 3+ lines, each reasonably short
    if len(non_empty) >= 3:
        avg_len = sum(len(l) for l in non_empty) / len(non_empty)
        if avg_len < 150:
            return True

    return False

def _split_structured_block(lines, upload_id, timestamp):
    """
    Keep structured/list blocks together up to 1200 chars.
    Larger limit ensures full lists stay in one chunk.
    """
    chunks = []
    temp = ""

    for line in lines:
        line = line.strip()
        if not line:
            continue
        if len(temp) + len(line) + 1 < 1200:
            temp += line + "\n"
        else:
            if temp.strip():
                chunks.append({
                    "upload_id": upload_id,
                    "timestamp": timestamp,
                    "chunk_text": temp.strip()
                })
            temp = line + "\n"

    if temp.strip():
        chunks.append({
            "upload_id": upload_id,
            "timestamp": timestamp,
            "chunk_text": temp.strip()
        })

    return chunks

def _split_prose(text, upload_id, timestamp):
    """
    Split prose into 600-char sentence windows with 1-sentence overlap.
    """
    CHUNK_SIZE = 600
    chunks = []

    sentences = re.split(r'(?<=[.!?])\s+', text)
    sentences = [s.strip() for s in sentences if s.strip()]

    if not sentences:
        return chunks

    temp_chunk = ""
    last_sentence = ""

    for sent in sentences:
        if len(temp_chunk) + len(sent) + 1 < CHUNK_SIZE:
            temp_chunk += (" " if temp_chunk else "") + sent
        else:
            if temp_chunk.strip():
                chunks.append({
                    "upload_id": upload_id,
                    "timestamp": timestamp,
                    "chunk_text": temp_chunk.strip()
                })
            temp_chunk = (last_sentence + " " + sent).strip() if last_sentence else sent
        last_sentence = sent

    if temp_chunk.strip():
        chunks.append({
            "upload_id": upload_id,
            "timestamp": timestamp,
            "chunk_text": temp_chunk.strip()
        })

    return chunks