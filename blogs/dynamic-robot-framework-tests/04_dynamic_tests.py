from robot.api import TestSuite, ResultWriter

OUTPUT_PATH_PREFIX = "./output/04-dynamic-tests"

""" Now for a relevant example. Let's say we want to test connectivity to a set of servers.

    We will get to actually testing the connectivity in a moment, however let's at least generate
    a dynamic set of tests and keywords given a list.

    In this example we are "hardcoding" the list of servers inside the script but it would be a non-trivial
    addition to import this from a JSON file or from an API call.
"""

servers = [
    {"name": "DNS Servers", "ips": ["8.8.8.8", "1.1.1.1"]},
    {"name": "NTP Servers", "ips": ["129.6.15.28", "132.163.97.1"]},
]

suite = TestSuite(name="Testing Connectivity to Servers")


""" Again because we are leveraging Python to "write" the tests, it as simple as a few for loops
    to generate these tests dynamically.
"""
for server in servers:
    test = suite.tests.create(f"Testing {server['name']}")

    for ip in server["ips"]:
        test.body.create_keyword("Log", args=[f"Need to test connectivity to {ip}."])

result = suite.run(output=f"{OUTPUT_PATH_PREFIX}-output.xml")

ResultWriter(f"{OUTPUT_PATH_PREFIX}-output.xml").write_results(
    report=f"{OUTPUT_PATH_PREFIX}-report.html", log=f"{OUTPUT_PATH_PREFIX}-log.html"
)
