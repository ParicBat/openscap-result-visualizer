import tkinter as tk
from tkinter import filedialog
import bokeh, bokeh.plotting, bokeh.layouts, json

# File Dialog

root = tk.Tk()
root.withdraw()

file_path = filedialog.askopenfilename()

# Generating graph

data = json.load(open(file_path, "r"))

x = range(0, len(data))

y_fail = [0]
y_success = [0]

fail = 0
success = 0

bokeh.plotting.output_file("Graph.html")

line_graph = bokeh.plotting.figure(title="Succeeded and Failed tests (Line)", toolbar_location=None, tools="", x_axis_label="Checked Tests", y_axis_label="Number of Tests")
bar_graph  = bokeh.plotting.figure(x_range=["Succeeded", "Failed"], title="Succeeded and Failed tests (Bar)", toolbar_location=None, tools="", y_axis_label="Number of Tests")

for check in data:
    try:
        if check["preparation"] and check["initial_scan"] and check["remediation"] and check["final_scan"]:
            success += 1
        else:
            assert False
    except:
        fail += 1
    
    y_fail.append(fail)
    y_success.append(success)

line_graph.line(x, y_success, legend_label="Succeeded", line_color="blue")
line_graph.line(x, y_fail, legend_label="Failed", line_color="red")

bar_graph.vbar(x=["Succeeded", "Failed"], top=[success, fail], width=0.5, color=["blue", "red"])

line_graph.legend.location = "top_left"

plot = bokeh.layouts.row(line_graph, bar_graph)

bokeh.plotting.show(plot)
