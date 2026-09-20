from fact_checker_bugs.nodes.cross_referencer import cross_reference_node


def test_cross_reference_deduplicates_urls_with_tracking_parameters():
    state = {
        "sources": [
            {
                "url": "https://example.com/article?utm_source=search&utm_medium=cpc&ref=abc#top",
                "title": "First source",
            },
            {
                "url": "https://example.com/article?ref=abc#top",
                "title": "Second source",
            },
        ]
    }

    result = cross_reference_node(state)

    assert len(result["sources"]) == 1
    assert result["sources"][0]["url"] == "https://example.com/article?ref=abc"
