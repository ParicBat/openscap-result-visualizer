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


def makeBarGraph(files):
    """Creates a graph from json file with the results."""
    jsondata = []
    for file in files:
        jsondata.append(json.load(open(file)))

    jsondata.sort(key=lastDate)
    data = []
    for tests in jsondata:
        data.append(checkTests(tests))
    rs = getResults(data)

    bar_graph = bokeh.plotting.figure(
        x_range=[f"Succeeded ({rs['pass'][-1]})", f"Failed ({rs['fail'][-1]})"],
        title=f"Succeeded and Failed tests from latest file ({jsondata[-1][-1]['run_timestamp']})",
        y_axis_label="Number of Tests")

    bar_graph.vbar(
        x=[f"Succeeded ({rs['pass'][-1]})", f"Failed ({rs['fail'][-1]})"],
        top=[rs['pass'][-1], rs['fail'][-1]],
        width=0.5,
        color=["blue", "red"])

    return bar_graph


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


def makeLineGraph(files):
    """Creates a line graph from multiple json files with the results"""
    jsonData = []
    for file in files:
        jsonData.append(json.load(open(file)))

    jsonData.sort(key=lastDate)
    data = []
    lastTestDates = []
    for tests in jsonData:
        data.append(checkTests(tests))
        lastTestDates.append(lastDate(tests))

    for i in range(len(lastTestDates)):
        lastTestDates[i] = lastTestDates[i].strftime("%Y-%m-%d %H:%M")

    results = getResults(data)

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
        files = [os.path.join(files[0], f) for f in os.listdir(files[0])]
    if out:
        print("Creating line graph...")
    graphs = [makeLineGraph(files)]

    if out:
        print("Creating bar graph...")
    graphs.append(makeBarGraph(files))

    if out:
        print("Creating file...")
    plot = bokeh.layouts.column(graphs)
    bokeh.plotting.output_file(output)
    bokeh.plotting.save(plot)

    if show:
        webbrowser.open('file://' + os.path.realpath(output))
