from fact_checker_bugs.graph import route_research


def test_route_research_ends_after_loop_limit_reached():
    state = {
        "loop_count": 2,
        "sources": [{"url": "https://example.com/one"}],
    }

    assert route_research(state) == "scorer"
