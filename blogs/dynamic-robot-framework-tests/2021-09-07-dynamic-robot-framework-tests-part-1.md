---
layout: post
title: "Dynamic Robot Framework Tests - Part 1"
tags: blog
author: Bryan Culver
---

## 00 - Introduction

Robot Framework is a useful testing tool that generates a great human-readable report of your tests. Additionally, their domain-specific language (DSL) is one that can be written by both engineers and non-engineers alike.

However one complexity to using Robot Framework is there is not any way currently to generate your test cases dyamically. Frequently people drop into Python code or scripts to do more custom tests of their code or infrastructure. Using templating tools like Jinja can also help create a more varied test suite between runs. For a lot of use cases these can be sufficient, although both can quickly become tedious to update or obscure what all is being tested.

Thankfully since Robot Framework's DSL must be parsed, they expose a full API to directly trigger this parsing through the `robot.api` modules.

I will be covering these concepts in a layered approach, consisting of two major parts. Part 1 (this post) will cover getting our tests running without using any `.robot` files or `robot` CLI commands. I will explain what each line means so that you can know where to augment for your use case. By the end of Part 1 you should be able to generate dynamic test contents. In Part 2, I will build upon these foundations and generate an dynamic test suite, including generating our own keywords.

The source code for the examples in each section of these posts can be found on our GitHub: #TODO ADD LINK HERE#

Before getting started, be sure to install the `robotframework` package via your package manager of choice. In the example repo above we use [Poetry](https://python-poetry.org), however you can use `pip` if you'd like.

Additionally, we are using version `4.x` of Robot Framework which made some API changes so if you're using `3.x` some of the syntax below will be different. Most IDEs should provide some hinting for the version you are using, but to note the biggest change is the migration to creating keywords on `.body` of the test versus it being an attribute on the keyword added.

If you are using `3.x` and are having significant challenges writing your own tests, feel free to open issues on the example repo above.

Let's get started with setting up our test suite and getting it to run:

## 01 - Core Concept

Let's review a trivial example of a Robot Framework test suite:

`01_core_concept.robot`:
```robot
*** Test Cases ***
Taco Time
    Log     "Fish tacos are the best tacos."
```

Yes, I hold strong opinions about my tacos. This isn't even a test, since the `Log` keyword almost never causes tests to fail. Bear with me as we will build upon this foundation and doing anything with imports requires other foundations to be in place when writing them in Python.

So how would we write this in Python?

`01_core_concept.py`:
```python
from robot.api import TestSuite, ResultWriter

suite = TestSuite(name="My Very Simple Test Suite")

test = suite.tests.create("Taco Time")

test.body.create_keyword("Log", args=["Fish tacos are the best tacos."])

suite.run(output="./01-core-concept-run-output.xml")

ResultWriter("./01-core-concept-run-output.xml").write_results()
```

Hmmm... three lines to six? Why would we do this? For tests as simple as this, I would suggest you write `.robot` files. However once we get to the dynamic parts, your tempalting engine or other Python code may add an order of magnitude of complexity than writing them natively.

Let's review each line and discuss what each line does.

```python
from robot.api import TestSuite, ResultWriter
```

If you've written Python before you will know what this line does, but we will need the `TestSuite` and `ResultWriter` to define our tests and generate our output HTML files respecitveley.

```python
suite = TestSuite(name="My Very Simple Test Suite")
```

Here we establish the test suite that we are going to run. Writing native DSL this is automatically created by creating the `.robot` file. The name of the suite is based on the file name or can be overriden via command line.

```python
test = suite.tests.create("Taco Time")
```

This is equilvent of the `Taco Time` line under the `*** Tests ***` section in our native DSL example.

Here we define our first test. By assigning our `.create` calls to a variable, it provides an easy way to attach keywords and tests to our parent objects.

```python
test.body.create_keyword("Log", args=["Fish tacos are the best tacos."])
```

Finally! Let's create some kewords in our test! This can quickly feel more intuitive than the native DSL, which require tabs or multiple spaces to separate arugments and keywords.

This is equilvelent to:
```
   Log     "Fish tacos are the best tacos."
```

We will get to assigments in a further section.

Our test is written, let's run it:

```python
suite.run(output="./01-core-concept-run-output.xml")
```

Normally when you call `robot` it's running both the test and result generation in one. In Python we must do these separately, but this allows us to skip the HTML generation should we want to run a tool like `rebot` on a large test suite without passing additional arguments.

Robot Framework outputs the results of the test first in an XML file (by default `output.xml`) then parses that XML file into the human-readable HTML report and log files.

Calling `suite.run` is what executes the tests, so it will have to be one of the last functions you call.

Also, we should specify the output path of the XML in this step as we will need it in the next step, the ResultWriter:

```python
ResultWriter("./01-core-concept-run-output.xml").write_results()
```

Here we point the ResultWriter at the previous suite run's output file and trigger the `write_results` function. This will output the log and report files to the current directory as `log.html` and `report.html` respectively, as you would expect from calling `robot`.

If you saved this file as `01_core_concept.py` like our example, you would call `python 01_core_concept.py`. You should see:

```sh
$> python 01_core_concept.py

==============================================================================
My Very Simple Test Suite                                                     
==============================================================================
Taco Time                                                             | PASS |
------------------------------------------------------------------------------
My Very Simple Test Suite                                             | PASS |
1 test, 1 passed, 0 failed
==============================================================================
Output:  /path/to/current/directory/01-core-concept-run-output.xml
```

As well as your desired output HTML files should be present.

Awesome! Now that we have the setup out of the way, let's continue with making more dynamic tests. But before we do that, we should avoid stepping on other tests output and results.

## 02 - Sidebar: Organized Output

Let's review the above Python file with a slightly more organized output:

`02_organized_output.py`:
```python
from robot.api import TestSuite, ResultWriter

OUTPUT_PATH_PREFIX = "./output/02-organized-output-suite-run"

suite = TestSuite(name="My Very Simple Test Suite")

test = suite.tests.create("Taco Time")

test.body.create_keyword("Log", args=["Fish tacos are the best tacos."])

result = suite.run(output=f"{OUTPUT_PATH_PREFIX}-output.xml")

ResultWriter(f"{OUTPUT_PATH_PREFIX}-output.xml").write_results(
    report=f"{OUTPUT_PATH_PREFIX}-report.html", log=f"{OUTPUT_PATH_PREFIX}-log.html"
)
```

There are a few lines that have been modified that you will see unchanged in the rest of the tutorial:

```python
OUTPUT_PATH_PREFIX = "./output/02-organized-output-suite-run"
```

Here we just define a constant to prefix all outputs with a directory and filename prefix.

```python
result = suite.run(output=f"{OUTPUT_PATH_PREFIX}-output.xml")
```

Here we generate the output XML file name using f-strings and our prefix.

```python
ResultWriter(f"{OUTPUT_PATH_PREFIX}-output.xml").write_results(
    report=f"{OUTPUT_PATH_PREFIX}-report.html", log=f"{OUTPUT_PATH_PREFIX}-log.html"
)
```

Here we use the same templated XML filename and specify the report and log paths using the same prefix, instead of using the default `report.html` and `log.html` paths.


These changes will make it easier for you to run the example code and any future tests you write.

Let's write a more dynamic test:

## 03 - Dynamic Test Arguments

Maybe you want to randomize your favorite tacos that you log?

We'll begin with the full file and then dive into the changes.

`03_dynamic_test_args.py`:
```python
from robot.api import TestSuite, ResultWriter
from random import choice

OUTPUT_PATH_PREFIX = "./output/03-dynamic-test-args"

taco_types = ["Fish", "Chicken", "Vegetarian"]
best_taco = choice(taco_types)

suite = TestSuite(name="My Very Simple Test Suite")

test = suite.tests.create("Taco Time")

test.body.create_keyword("Log", args=[f"{best_taco} tacos are the best tacos."])

result = suite.run(output=f"{OUTPUT_PATH_PREFIX}-output.xml")

ResultWriter(f"{OUTPUT_PATH_PREFIX}-output.xml").write_results(
    report=f"{OUTPUT_PATH_PREFIX}-report.html", log=f"{OUTPUT_PATH_PREFIX}-log.html"
)
```

We import the `choice` function from the `random` module so we can grab a random entry from our `taco_types` list.

Then in instead of our args being a static string, it's a f-string. Since this string is rendered as it's writing the test, to the test runner it's the same normal string as it would expect. Except now it's a different between each test run.


Hopefully this will start getting you to think about how you can start writing more dynamic tests, since this reduces a sigificant head-ache and weight from doing string handling inside the Robot Framework test itself.


In the next part we will cover creating multiple tests derrived from data, importing libraries, and creating our own keywords, using native Python `robot.api` calls.
