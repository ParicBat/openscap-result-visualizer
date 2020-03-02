import sys
sys.path.insert(0, "..")
import oscaprv


def test_checkresults():
    assert oscaprv.checkTest({"preparation": True, "initial_scan": True, "remediation": True, "final_scan": True})
    assert not oscaprv.checkTest({"preparation": True, "initial_scan": True, "remediation": False, "final_scan": False})
    assert oscaprv.checkTest({"preparation": True, "initial_scan": True})
    assert not oscaprv.checkTest({"preparation": True, "initial_scan": False})
    assert not oscaprv.checkTest({"preparation": True, "initial_scan": True, "remediation": True, "final_scan": False})
    assert not oscaprv.checkTest({"preparation": True, "initial_scan": True, "remediation": False})
    assert not oscaprv.checkTest({"preparation": False})
    assert not oscaprv.checkTest({"preparation": True})


def test_getResults():
    jsondata = [[{"preparation": True, "initial_scan": True}], [{"preparation": False}]]
    data = []
    for tests in jsondata:
        data.append(oscaprv.checkTests(tests))
    assert oscaprv.getResults(data) == {"fail": [0, 1], "pass": [1, 0]}
