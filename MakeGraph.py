import json
import os
import webbrowser
import argparse
import bokeh
import bokeh.plotting
import bokeh.layouts
import datetime


def checkTest(test):
    """Checks if the test has failed or succeeded. Returns True if suceeded."""
    try:
        if test["final_scan"]:
            return True
    except:
        pass
    return False


def checkTests(tests):
    results = []
    for test in tests:
        results.append(checkTest(test))
    return results


def makeBarGraph(file):
    """Creates a html document with graphs of the results. Outputs the location of the file"""
    data = json.load(file)

    fail = 0
    success = 0

    for test in data:
        if checkTest(test):
            success += 1
        else:
            fail += 1

    bar_graph = bokeh.plotting.figure(
        x_range=[f"Succeeded ({success})", f"Failed ({fail})"],
        title=f"Succeeded and Failed tests (Bar) ({file.name})",
        toolbar_location=None, tools="wheel_zoom",
        y_axis_label="Number of Tests")

    bar_graph.vbar(
        x=[f"Succeeded ({success})", f"Failed ({fail})"],
        top=[success, fail],
        width=0.5,
        color=["blue", "red"])

    return bar_graph


def sortByDateInJSON(value):
    return datetime.datetime.strptime(value[-1]["run_timestamp"], "%Y-%m-%d %H:%M")


def makeLineGraph(files):
    jsonData = []
    for file in files:
        jsonData.append(json.load(open(file)))

    jsonData.sort(key=sortByDateInJSON)
    data = []
    lastTestDates = []
    for tests in jsonData:
        data.append(checkTests(tests))
        lastTestDates.append(datetime.datetime.strptime(tests[-1]["run_timestamp"], "%Y-%m-%d %H:%M"))

    lastTestDates.sort()
    for i in range(len(lastTestDates)):
        lastTestDates[i] = str(lastTestDates[i])

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

    graph = bokeh.plotting.figure(x_range=lastTestDates,
                                  title="Tests in test files sorted by date",
                                  toolbar_location=None,
                                  tools="wheel_zoom",
                                  y_axis_label="Number of Tests")

    graph.line(lastTestDates, resultsPass, line_width=2, line_color="blue")
    graph.line(lastTestDates, resultsFail, line_width=2, line_color="red")

    return graph


def ShowGraph(files, output):
    """Shows a html document with graphs of the results"""
    graphs = [makeLineGraph(files)]
    for file in files:
        graphs.append(makeBarGraph(open(file)))

    plot = bokeh.layouts.column(graphs)
    bokeh.plotting.output_file(output)
    bokeh.plotting.save(plot)

    webbrowser.open('file://' + os.path.realpath(output))


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Creates a graph of tests from json file.")
    parser.add_argument("-f", "--files", help="JSON file to get data from.", nargs="+")
    parser.add_argument("-o", "--output_file", nargs='?', default="Graph.html")
    args = parser.parse_args()
    ShowGraph(args.files, args.output_file)
