import sys
import random
import json

f = open(sys.argv[1], "w")
tests = []
testtypes = [{"final_scan": True}, {"final_scan": False}]

for i in range(random.randint(2, 100)):
    tests.append(testtypes[random.randint(0, len(testtypes)-1)])

f.write(json.dumps(tests))
