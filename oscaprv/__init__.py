import json
import os
import webbrowser
import bokeh
import bokeh.plotting
import bokeh.layouts
import datetime


def checkTest(test):
    """Checks if the test has failed or succeeded. Returns True if suceeded."""
    if test["preparation"] and test.get("initial_scan", False) and test.get("remediation", True) and test.get("final_scan", True):
        return True
    else:
        return False


def checkTests(tests):
    results = []
    for test in tests:
        results.append(checkTest(test))
    return results


def processResults(data):
    jsondata = []
    for item in data:
        jsondata.append(item)

    jsondata.sort(key=lastDate)
    lastTestDates = []
    checked_tests = []
    for tests in jsondata:
        checked_tests.append(checkTests(tests))
        lastTestDates.append(str(lastDate(tests)))
    return {"results": getResults(checked_tests), "dates": lastTestDates}


def lastDate(value):
    return datetime.datetime.strptime(value[-1]["run_timestamp"], "%Y-%m-%d %H:%M")


def getResults(data):
    """Returns a dictionary with the results.

    Keys:  
    fail  - Failed results  
    pass - Passed results"""
    resultsPass = []
    resultsFail = []
    for results in data:
        p = 0
        f = 0
        for result in results:
            if result:
                p += 1
            else:
                f += 1
        resultsPass.append(p)
        resultsFail.append(f)

    return {"fail": resultsFail, "pass": resultsPass}


def makeLineGraph(data):
    """Creates a line graph from multiple json files with the results"""

    rs = processResults(data)
    results = rs["results"]
    lastTestDates = rs["dates"]

    graph = bokeh.plotting.figure(x_range=lastTestDates,
                                  title="Tests in test files sorted by date",
                                  plot_width=1280,
                                  y_axis_label="Number of Tests")

    graph.line(lastTestDates, results["pass"], line_width=2, line_color="blue")
    graph.line(lastTestDates, results["fail"], line_width=2, line_color="red")

    return graph


def MakeGraph(files, output, show=False, out=False):
    """Makes a html document with graphs of the results"""
    if os.path.exists(files[0]):
        files = [json.load(open(os.path.join(files[0], f))) for f in os.listdir(files[0])]
    if out:
        print("Creating line graph...")
    graph = makeLineGraph(files)

    if out:
        print("Creating file...")
    bokeh.plotting.output_file(output)
    bokeh.plotting.save(graph)

    if show:
        webbrowser.open('file://' + os.path.realpath(output))
