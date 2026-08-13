from retrieve import retrieve

def test_retrieve_returns_relevant_results():
    results = retrieve("How do I create an automation rule that runs every hour?")
    assert len(results) > 0
    for r in results:
        assert r["distance"] <= 1.0

def test_retrieve_filters_irrelevant_query():
    results = retrieve("What's the best pizza topping?")
    assert results == []