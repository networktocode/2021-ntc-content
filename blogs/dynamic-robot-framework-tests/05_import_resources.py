from robot.api import TestSuite, ResultWriter

OUTPUT_PATH_PREFIX = "./output/05-import-resources"

""" Now for some real tests. We are going to continue the connectivity test example.

    Internally RobotFramework consideres libraries and other things neccessary to 'import' to be "resources".

    There is a resource attribute on the suite where we can specify what libraries we want to import.
"""

servers = [
    {"name": "DNS Servers", "ips": ["8.8.8.8", "1.1.1.1"]},
    {"name": "NTP Servers", "ips": ["129.6.15.28", "132.163.97.1"]},
]

suite = TestSuite(name="Testing Connectivity to Servers")


""" To run the ping command we will leverage the 'Run and Return Rc' keyword which requires the 'OperatingSystem' library."""
suite.resource.imports.library("OperatingSystem")

for server in servers:
    test = suite.tests.create(f"Testing {server['name']}")

    for ip in server["ips"]:

        """This is also the first time we have worked with assignments.

        Remember, we are using the robot API to write the tests not run them, just trigger.

        Therefor there is no way for you to get the output of the command in this file. You will have to assign the result to a variable then use RF to evaluate it.

        The lines below are equivalent to:

        ${rc}=      Run and Return Rc  ping 8.8.8.8 -c 1 -W 5
        Should Be Equal As Integers     ${rc} "0"
        """
        test.body.create_keyword(
            "Run and Return Rc", args=[f"ping {ip} -c 1 -W 5"], assign=["${rc}"]
        )
        test.body.create_keyword("Should Be Equal As Integers", args=["${rc}", "0"])

result = suite.run(output=f"{OUTPUT_PATH_PREFIX}-output.xml")

ResultWriter(f"{OUTPUT_PATH_PREFIX}-output.xml").write_results(
    report=f"{OUTPUT_PATH_PREFIX}-report.html", log=f"{OUTPUT_PATH_PREFIX}-log.html"
)
