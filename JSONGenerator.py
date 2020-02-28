import sys
import random
import json
import argparse
from datetime import datetime, date


parser = argparse.ArgumentParser(description="Creates a random OpenSCAP result json file.")
parser.add_argument("path", help="File(s) to create", nargs="+")
args = parser.parse_args()

for i in range(len(args.path)):
    f = open(args.path[i], "w")
    tests = []
    testtypes = [{"preparation": True, "initial_scan": True}, {"preparation": False}]

    for i in range(random.randint(2, 100)):
        test = testtypes[random.randint(0, len(testtypes)-1)]
        test["run_timestamp"] = f"{date.today().year}-{date.today().month}-{date.today().day} {random.randint(0, 23)}:{random.randint(0, 59)}"
        tests.append(test)

    f.write(json.dumps(tests))
    f.close()
