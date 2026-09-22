from fact_checker_bugs.nodes.retriever import retrieve_sources_node


def test_retrieve_sources_preserves_previous_evidence_across_rounds(monkeypatch):
    class DummyTavilyClient:
        def search(self, query, max_results):
            return {
                "results": [
                    {
                        "title": "New source",
                        "url": "https://example.com/new-source",
                        "content": "Fresh evidence",
                        "publishedDate": "2024-01-01",
                    }
                ]
            }

    monkeypatch.setenv("TAVILY_API_KEY", "test-key")
    monkeypatch.setattr(
        "fact_checker_bugs.nodes.retriever.TavilyClient",
        lambda api_key: DummyTavilyClient(),
    )
    monkeypatch.setattr(
        "fact_checker_bugs.nodes.retriever.get_all_keys",
        lambda: ["test-key"],
    )

    state = {
        "queries": ["test query"],
        "sources": [
            {
                "title": "Old source",
                "url": "https://example.com/old-source",
                "snippet": "Previous evidence",
                "publishedDate": "2023-01-01",
            }
        ],
    }

    result = retrieve_sources_node(state)

    assert len(result["sources"]) == 2
    urls = [source["url"] for source in result["sources"]]
    assert "https://example.com/old-source" in urls
    assert "https://example.com/new-source" in urls
