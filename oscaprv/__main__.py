import oscaprv
import argparse

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Creates a graph from tests from json file.")
    parser.add_argument("files", help="JSON files or folder to get data from.", nargs="+")
    parser.add_argument("-o", "--output_file", nargs='?', default="Graph.html",
                        help="Specifies the output file for the graphs.")
    parser.add_argument("-s", "--show", action="store_true", help="Shows the results.")
    parser.add_argument("-p", "--progress", action="store_true", help="Print out progress.")
    args = parser.parse_args()
    oscaprv.MakeGraph(args.files, args.output_file, args.show, args.progress)
