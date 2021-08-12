from robot.api import TestSuite, ResultWriter

""" This example only lightly builds on top of the previous example.
    From here on out we will gloss over the suite running and result writing.
"""

""" Defining a prefix for the output path """
OUTPUT_PATH_PREFIX = "./output/02-organized-output-suite-run"

suite = TestSuite(name="My Very Simple Test Suite")

test = suite.tests.create("Taco Time")

test.body.create_keyword("Log", args=["Fish tacos are the best tacos."])

result = suite.run(output=f"{OUTPUT_PATH_PREFIX}-output.xml")

""" Specifying report= and log= in write_results will generate the HTML files as named instead of report.html and log.html"""
ResultWriter(f"{OUTPUT_PATH_PREFIX}-output.xml").write_results(
    report=f"{OUTPUT_PATH_PREFIX}-report.html", log=f"{OUTPUT_PATH_PREFIX}-log.html"
)
