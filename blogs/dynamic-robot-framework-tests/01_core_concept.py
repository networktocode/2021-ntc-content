from robot.api import TestSuite, ResultWriter


"""The below lines would be the equivalent of:

    `01_core_concept.robot`:
    ```robotframework
        *** Test Cases ***
        Taco Time
            Log     "Fish tacos are the best tacos."

    ```

    and then running the command:
    ```
    $> robot --name="My Very Simple Test Suite" 01_core_concept.robot
    ```
"""


""" Establish the test suite we are going to build. """
suite = TestSuite(name="My Very Simple Test Suite")


""" While you can create a TestCase object and then link it to the TestSuite later,
    creating it from the suite itself save time and imports.
"""
test = suite.tests.create("Taco Time")


""" Nothing fancy at this point, we are just going to call the Log keyword.

    You add keywords to a test with the .create_keyword function on the body of the test.

    Remember in RobotFramework you call the keyword with given arguments.

    This would look like:

    Log     "Fish tacos are the best tacos."
"""
test.body.create_keyword("Log", args=["Fish tacos are the best tacos."])


""" Now that we have our test cases added to the suite, we want to run the suite.

    You do not have to specify the output path when running the suite.

    However, not specifying the output will always make it output to './output.xml' and you
    will need this path for the next step, the "ResultWriter". Not assuming the path of this output
    is a better practice.
"""
suite.run(output="./01-core-concept-run-output.xml")


""" While calling `robot` via CLI automatically outputs the XML and human-parsable HTML files,
    suite.run only outputs the XML file.

    The output XML isn't very useful unless you're using a utility like rebot to combine outputs.

    We can use the 'ResultWriter' class to take in the suite run's output and generate the report
    and log HTML files.

    Given no arguments it will generate these HTML files as `report.html` and `log.html`. You can
    override this by specifiying the `report=` and `log=` arguments in `write_results()`.
"""
ResultWriter("./01-core-concept-run-output.xml").write_results()
