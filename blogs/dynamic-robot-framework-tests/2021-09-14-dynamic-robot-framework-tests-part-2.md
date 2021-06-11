---
layout: post
title: "Dynamic Robot Framework Tests - Part 2"
tags: blog
author: Bryan Culver
---

In the previous part we got our test suite set up and running. We even saw how to generate a test that is random, without having to write a lot of string handling in Robot Framework.

In this part we will start writing dynamic tests. (We will also ditch the taco example for something more relevant!)


## 04 - Dynamic Tests from Data

Let's start with creating dynamic tests from data:

`04_dynamic_tests.py`:
```python
from robot.api import TestSuite, ResultWriter

OUTPUT_PATH_PREFIX = "./output/04-dynamic-tests"

servers = [
    {"name": "DNS Servers", "ips": ["8.8.8.8", "1.1.1.1"]},
    {"name": "NTP Servers", "ips": ["129.6.15.28", "132.163.97.1"]},
]

suite = TestSuite(name="Testing Connectivity to Servers")

for server in servers:
    test = suite.tests.create(f"Testing {server['name']}")

    for ip in server["ips"]:
        test.body.create_keyword("Log", args=[f"Need to test connectivity to {ip}."])

result = suite.run(output=f"{OUTPUT_PATH_PREFIX}-output.xml")

ResultWriter(f"{OUTPUT_PATH_PREFIX}-output.xml").write_results(
    report=f"{OUTPUT_PATH_PREFIX}-report.html", log=f"{OUTPUT_PATH_PREFIX}-log.html"
)

```

In this example we have a provided list of servers we want to test to and a given set of IPs in the `servers` variable:

```python
servers = [
    {"name": "DNS Servers", "ips": ["8.8.8.8", "1.1.1.1"]},
    {"name": "NTP Servers", "ips": ["129.6.15.28", "132.163.97.1"]},
]
```

This data can be sourced from say a nearby YAML or JSON file or via an API call. But for now we will keep the example code simple and say this is a solved problem.

Let's say we want output test summary to be pass/fail based on the server category, "DNS Servers" and "NTP Servers". We will then loop over the server dictionaries and create a test for each:

```python
for server in servers:
    test = suite.tests.create(f"Testing {server['name']}")
    # ...
```

Then we can add the keywords for each IP to be the "assertions" of the test:

```python
    for ip in server["ips"]:
        test.body.create_keyword("Log", args=[f"Need to test connectivity to {ip}."])
```

Again we are using the `Log` keyword for this example. However our tests are being dynamically generated. Our total tests are not fixed. If we want to add new server categories to tests, all that is necessary is for us to provide additional data.

If all tests pass we should see `2 test, 2 passed, 0 failed` in our output.

What if you wanted each IP to be registered as its own test?

We could change our loops to the following:

```python
for server in servers:
    for ip in server["ips"]:
        test = suite.tests.create(f"Testing {server['name']} - {ip}")
        test.body.create_keyword("Log", args=[f"Need to test connectivity to {ip}."])
```

This would create a unique test for each IP.

If all tests pass we should see `4 test, 4 passed, 0 failed` in our output.

## 05 - Import Resources

Now that we are generating tests from data, let's do actual testing. To do this in our current example, we'll use the `ping` utility to try reaching these servers.

To do that we will need to import the `OperatingSystem` library in Robot Framework. We will also need to work with assignments to capture the output of the `ping` command and determine if the run was successful.


`05_import_resources.py`:
```python
from robot.api import TestSuite, ResultWriter

OUTPUT_PATH_PREFIX = "./output/05-import-resources"

servers = [
    {"name": "DNS Servers", "ips": ["8.8.8.8", "1.1.1.1"]},
    {"name": "NTP Servers", "ips": ["129.6.15.28", "132.163.97.1"]},
]

suite = TestSuite(name="Testing Connectivity to Servers")

suite.resource.imports.library("OperatingSystem")

for server in servers:
    test = suite.tests.create(f"Testing {server['name']}")

    for ip in server["ips"]:

        test.body.create_keyword(
            "Run and Return Rc", args=[f"ping {ip} -c 1 -W 5"], assign=["${rc}"]
        )
        test.body.create_keyword("Should Be Equal As Integers", args=["${rc}", "0"])

result = suite.run(output=f"{OUTPUT_PATH_PREFIX}-output.xml")

ResultWriter(f"{OUTPUT_PATH_PREFIX}-output.xml").write_results(
    report=f"{OUTPUT_PATH_PREFIX}-report.html", log=f"{OUTPUT_PATH_PREFIX}-log.html"
)
```

This looks a bit different from our previous example, but only a few lines have been modified or added.

Let's first look at the import:

```python
suite.resource.imports.library("OperatingSystem")
```

Robot Framework registers libraries and defined keywords as resources for the tests. If the library is imported from somewhere it's an imported resource.

This would normally be seen as:

```robot
*** Settings ***
Library           OperatingSystem
```

Now that we have `OperatingSystem` imported we can use the `Run and Return Rc` keyword to run the `ping` command. We'll also learn how to use assignments.

```python
test.body.create_keyword(
            "Run and Return Rc", args=[f"ping {ip} -c 1 -W 5"], assign=["${rc}"]
        )
```

Again we create keywords like normal, along with specifing the command we want to run as an argument. We need to specify the assignment variable with the `assign=` argument. The value you supply should follow normal Robot Framework convention.

This would normally be seen as (if `ip` was specified as `8.8.8.8`):

```robot
${rc}=   Run and Return Rc   "ping 8.8.8.8 -c 1 -W 5"
```

Once we have run the `ping` test and captured the return code, we can evaluate it to ensure it's returned `0`.

```python
test.body.create_keyword("Should Be Equal As Integers", args=["${rc}", "0"])
```

This is equivalent to:

```robot
Should Be Equal As Integers  ${rc}  "0"
```

A pretty common equivalancy test.

Let's run it and see the output:

```shell
$> python 05_import_resources.py

==============================================================================
Testing Connectivity to Servers                                               
==============================================================================
Testing DNS Servers                                                   | PASS |
------------------------------------------------------------------------------
Testing NTP Servers                                                   | FAIL |
1 != 0
------------------------------------------------------------------------------
Testing Connectivity to Servers                                       | FAIL |
2 tests, 1 passed, 1 failed
==============================================================================
```

Dratz! Our NTP servers don't like to be pinged, but our DNS servers returned results therefor we pass those tests! Again because our tests are defined at the category level and not the IP level we are running two tests, each having two assertions.

## 06 - Create Keywords

Now in the example above we likely don't need to register our own keyword. Since we are creating the tests with Python it's easy to create factories to generate the necessary keywords.

But let's say for example we want to collapse the `Run and Return Rc` and `Should Be Equal As Integers` keywords into a single one, called `Test Connection To`.

`06_create_keyword.py`:
```python
from robot.api import TestSuite, ResultWriter

OUTPUT_PATH_PREFIX = "./output/06-create-keyword"

servers = [
    {"name": "DNS Servers", "ips": ["8.8.8.8", "1.1.1.1"]},
    {"name": "NTP Servers", "ips": ["129.6.15.28", "132.163.97.1"]},
]

suite = TestSuite(name="Testing Connectivity to Servers")

suite.resource.imports.library("OperatingSystem")

test_connection_to_kw = suite.resource.keywords.create("Test Connection To")
test_connection_to_kw.args = ["${ip}"]
test_connection_to_kw.body.create_keyword(
    "Run and Return Rc", args=["ping ${ip} -c 1 -W 5"], assign=["${rc}"]
)
test_connection_to_kw.body.create_keyword(
    "Should Be Equal As Integers", args=["${rc}", "0"]
)

for server in servers:
    test = suite.tests.create(f"Testing {server['name']}")

    for ip in server["ips"]:
        test.body.create_keyword("Test Connection To", args=[ip])

result = suite.run(output=f"{OUTPUT_PATH_PREFIX}-output.xml")

ResultWriter(f"{OUTPUT_PATH_PREFIX}-output.xml").write_results(
    report=f"{OUTPUT_PATH_PREFIX}-report.html", log=f"{OUTPUT_PATH_PREFIX}-log.html"
)
```

Again, user defined keywords are resources for tests, like library imports. Instead of importing them though, we will create them:

```python
test_connection_to_kw = suite.resource.keywords.create("Test Connection To")
```

Because we need to add keywords and args to this new keyword, we are going to simplify the use by capturing the created object (a `UserKeyword`) and assigning it to `test_connection_to_kw`.

We will need to receive the IP to ping as an argument. Like `args` being a keyword argument for calling/using exisitng keywords, it's an attribute of the `UserKeyword` object for us define.

```python
test_connection_to_kw.args = ["${ip}"]
```

Again we use the syntax we are used to for defining variables in Robot Framework.

Next a similar method of adding the command run and assertion keywords to our test is used to add them to our new keyword:

```python
test_connection_to_kw.body.create_keyword(
    "Run and Return Rc", args=["ping ${ip} -c 1 -W 5"], assign=["${rc}"]
)
test_connection_to_kw.body.create_keyword(
    "Should Be Equal As Integers", args=["${rc}", "0"]
)
```

Instead of calling `.body.create_keyword(...)` on our test, we are calling it on our `UserKeyword` object.

That's all we need to do to define the keyword. Now it's time to use it!

```python
test.body.create_keyword("Test Connection To", args=[ip])
```

Our tests now call a single keyword instead of two. This will simplify matters if we decide to change how we generate the tests. And again because we are using native Python we can create a factory that generators our keywords (maybe even making those dynamic too!) on the fly.

Our output in our HTML will be marginally different with this structure because it will make reference to the new keyword instead of example five which called the commands directly. Functionally it's identical though:

```bash
$> python 06_create_keyword.py 
==============================================================================
Testing Connectivity to Servers                                               
==============================================================================
Testing DNS Servers                                                   | PASS |
------------------------------------------------------------------------------
Testing NTP Servers                                                   | FAIL |
1 != 0
------------------------------------------------------------------------------
Testing Connectivity to Servers                                       | FAIL |
2 tests, 1 passed, 1 failed
==============================================================================
```

Bummer! Our NTP servers still don't like to be pinged. Oh well!

I hope you enjoyed this two part series on generating dynamic Robot Framework test cases by calling the API directly!

Again, feel free to drop messages in the comments if you have questions. As well, all source code from both parts can be [found on GitHub](#TODO UPDATE THIS LINK).
