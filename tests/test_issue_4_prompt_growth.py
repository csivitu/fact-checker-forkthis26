from fact_checker_bugs.nodes.query_formulator import formulate_queries_node


def test_formulate_queries_truncates_previous_evidence_for_prompt_size(monkeypatch):
    captured = {}

    class DummyResult:
        queries = ["Updated search query"]

    monkeypatch.setattr(
        "fact_checker_bugs.nodes.query_formulator.get_all_keys",
        lambda: ["test-key"],
    )
    def fake_invoke(build_llm, prompt, **kwargs):
        captured["prompt"] = prompt
        return DummyResult()

    monkeypatch.setattr(
        "fact_checker_bugs.nodes.query_formulator.invoke_with_backoff",
        fake_invoke,
    )

    state = {
        "claim": "Large claim",
        "sources": [
            {"title": f"Source {i}", "url": f"https://example.com/{i}", "snippet": "A very long snippet " * 50}
            for i in range(5)
        ],
    }

    result = formulate_queries_node(state)

    prompt = captured["prompt"]
    assert result["queries"] == ["Updated search query"]
    assert prompt.count("Title:") <= 3
