from robot.api import TestSuite, ResultWriter
from random import choice

OUTPUT_PATH_PREFIX = "./output/03-dynamic-test-args"

taco_types = ["Fish", "Chicken", "Vegetarian"]
best_taco = choice(taco_types)

suite = TestSuite(name="My Very Simple Test Suite")

test = suite.tests.create("Taco Time")

""" Because we are using native Python to construct the tests you can dynamically generate testing details.

    While this example is trivial, any args or even the keyword itself can be dynamically generated at script runtime.
"""
test.body.create_keyword("Log", args=[f"{best_taco} tacos are the best tacos."])

result = suite.run(output=f"{OUTPUT_PATH_PREFIX}-output.xml")

ResultWriter(f"{OUTPUT_PATH_PREFIX}-output.xml").write_results(
    report=f"{OUTPUT_PATH_PREFIX}-report.html", log=f"{OUTPUT_PATH_PREFIX}-log.html"
)
