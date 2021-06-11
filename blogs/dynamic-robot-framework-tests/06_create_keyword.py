from robot.api import TestSuite, ResultWriter

OUTPUT_PATH_PREFIX = "./output/06-create-keyword"


""" Thankfully because we are creating tests via Python, avoiding "copy-pasta" is easier.

    However creating our own keywords has many purposes beyond that.

    Creating our own keywords are again a suite-level resource to be used across the entire suite of tests.

    However instead of importing, it's a keyword resource
"""

servers = [
    {"name": "DNS Servers", "ips": ["8.8.8.8", "1.1.1.1"]},
    {"name": "NTP Servers", "ips": ["129.6.15.28", "132.163.97.1"]},
]

suite = TestSuite(name="Testing Connectivity to Servers")

suite.resource.imports.library("OperatingSystem")

""" Instead of having all of our steps being defined at the test itself, let's have the connection test be a standard keyword, only needing to pass in the IP

    We'll call this keyword 'Test Connection To'
"""
test_connection_to_kw = suite.resource.keywords.create("Test Connection To")

""" We need to accept an arg to test on, we'll set that to ${ip} """
test_connection_to_kw.args = ["${ip}"]

""" Then we add keywords to the body of the new keywords (keywords all the way down!) to perform the test"""
test_connection_to_kw.body.create_keyword(
    "Run and Return Rc", args=["ping ${ip} -c 1 -W 5"], assign=["${rc}"]
)
test_connection_to_kw.body.create_keyword(
    "Should Be Equal As Integers", args=["${rc}", "0"]
)

for server in servers:
    test = suite.tests.create(f"Testing {server['name']}")

    for ip in server["ips"]:

        """Then testing the connection is as simple as using our defined keyword"""
        test.body.create_keyword("Test Connection To", args=[ip])

result = suite.run(output=f"{OUTPUT_PATH_PREFIX}-output.xml")

ResultWriter(f"{OUTPUT_PATH_PREFIX}-output.xml").write_results(
    report=f"{OUTPUT_PATH_PREFIX}-report.html", log=f"{OUTPUT_PATH_PREFIX}-log.html"
)
