import re

def rewrite_query(query: str, llm=None) -> str:

    cleaned = query.strip().lower()

    # Remove leading question phrase patterns that add noise to the embedding
    # These words don't help retrieve documents — strip them
    filler_prefixes = [
        r"^can you (tell me |please |)?",
        r"^please (tell me |)?",
        r"^could you (tell me |)?",
        r"^i want to know ",
        r"^i need to know ",
        r"^tell me ",
        r"^what (is|are|was|were) (the |a |an )?",
        r"^who (is|are|was|were) (the |a |an )?",
        r"^where (is|are|was|were) (the |a |an )?",
        r"^when (is|are|was|were) (the |a |an )?",
        r"^how (many|much|is|are|was|were) (the |a |an )?",
        r"^which (are|is|were|was) (the |a |an )?",
        r"^list (all |the |)?",
        r"^give me (all |the |a list of |)?",
        r"^show me (all |the |)?",
    ]

    for pattern in filler_prefixes:
        cleaned = re.sub(pattern, "", cleaned, flags=re.IGNORECASE).strip()

    # Remove trailing punctuation
    cleaned = cleaned.rstrip("?.,!").strip()

    # If cleaning made it empty (edge case), return original
    if not cleaned:
        return query.strip().lower()

    return cleaned
