import json
import os
import webbrowser
import sys
import bokeh
import bokeh.plotting
import bokeh.layouts

def checkTest(test):
    """Checks if the test has failed or succeeded. Returns True if suceeded."""
    try:
        if test["final_scan"]:
            return True
    except:
        pass
    return False

def makeGraph(file, output):
    """Creates a html document with graphs of the results. Outputs the location of the file"""
    data = json.load(file)

    fail = 0
    success = 0

    bar_graph = bokeh.plotting.figure(
        x_range=["Succeeded", "Failed"],
        title="Succeeded and Failed tests (Bar)",
        toolbar_location=None, tools="",
        y_axis_label="Number of Tests")

    for test in data:
        if checkTest(test):
            success += 1
        else:
            fail += 1
    bar_graph.vbar(x=["Succeeded", "Failed"], top=[success, fail], width=0.5, color=["blue", "red"])

    plot = bokeh.layouts.row(bar_graph)

    bokeh.plotting.output_file(output)
    return bokeh.plotting.save(plot)

def ShowGraph(file, output):
    """Shows a html document with graphs of the results"""
    webbrowser.open('file://' + os.path.realpath(makeGraph(file, output)))

if __name__ == "__main__":
    output_file = "Graph.html"
    if len(sys.argv) > 1:
        if len(sys.argv) > 2:
            output_file = sys.argv[2]
        ShowGraph(open(sys.argv[1]), output_file)
