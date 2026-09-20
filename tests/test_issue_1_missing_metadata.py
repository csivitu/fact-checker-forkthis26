import os

from fact_checker_bugs.nodes.retriever import retrieve_sources_node


def test_retrieve_sources_keeps_valid_results_when_optional_fields_are_missing(monkeypatch):
    class DummyTavilyClient:
        def search(self, query, max_results):
            return {
                "results": [
                    {
                        "title": "Example result",
                        "url": "https://example.com/article",
                        "content": "Relevant text"
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

    result = retrieve_sources_node({"queries": ["test query"], "sources": []})

    assert result["sources"][0]["title"] == "Example result"
    assert result["sources"][0]["url"] == "https://example.com/article"
    assert result["sources"][0]["snippet"] == "Relevant text"
    assert result["sources"][0]["publishedDate"] is None
