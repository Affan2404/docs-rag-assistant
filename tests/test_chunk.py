from chunk import split_into_sentences, chunk_sentences

def test_split_into_sentences_basic():
    text = "This is one. This is two! Is this three?"
    result = split_into_sentences(text)
    assert result == ["This is one.", "This is two!", "Is this three?"]

def test_chunk_sentences_respects_max_chars():
    sentences = ["A" * 200 + ".", "B" * 200 + ".", "C" * 200 + "."]
    chunks = chunk_sentences(sentences)
    for chunk in chunks:
        assert len(chunk) <= 500 + 200  # allow one sentence over, since we don't split mid-sentence

def test_chunk_sentences_overlap():
    sentences = ["Short one.", "Short two.", "A" * 490 + "."]
    chunks = chunk_sentences(sentences)
    assert len(chunks) >= 2
    assert chunks[0].split(". ")[-1].strip(".") in chunks[1]