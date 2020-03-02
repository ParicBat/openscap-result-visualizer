import MakeGraph


def test_results():
    assert MakeGraph.checkTest({"preparation": True, "initial_scan": True, "remediation": True, "final_scan": True})
    assert not MakeGraph.checkTest({"preparation": True, "initial_scan": True, "remediation": False, "final_scan": False})
    assert MakeGraph.checkTest({"preparation": True, "initial_scan": True})
    assert not MakeGraph.checkTest({"preparation": True, "initial_scan": False})
    assert not MakeGraph.checkTest({"preparation": True, "initial_scan": True, "remediation": True, "final_scan": False})
    assert not MakeGraph.checkTest({"preparation": True, "initial_scan": True, "remediation": False})
    assert not MakeGraph.checkTest({"preparation": False})
    assert not MakeGraph.checkTest({"preparation": True})
