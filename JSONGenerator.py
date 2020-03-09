import sys
import random
import json
import argparse
from datetime import datetime, date


parser = argparse.ArgumentParser(description="Creates a random OpenSCAP result json file.")
parser.add_argument("path", help="File(s) to create", nargs="+")
parser.add_argument("-t", "--result_types",
                    help="JSON file to get test result types from.",
                    nargs="?",
                    default="""[{"preparation": true, "initial_scan": true}, {"preparation": false}]""")
args = parser.parse_args()

for path in args.path:
    f = open(path, "w")
    tests = []
    testtypes = json.loads(args.result_types)

    for i in range(random.randint(2, 100)):
        test = testtypes[random.randint(0, len(testtypes)-1)]
        test["run_timestamp"] = f"{date.today().year}-{date.today().month}-{date.today().day} {random.randint(0, 23)}:{random.randint(0, 59)}"
        tests.append(test)

    f.write(json.dumps(tests))
    f.close()
