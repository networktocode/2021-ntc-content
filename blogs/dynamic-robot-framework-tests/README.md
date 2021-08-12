# Dynamic Robot Framework Tests (Part 1 & 2)

Author: Bryan Culver <bryan.culver@networktocode.com>

This is the example project supporting the two-part series on creating dynamic Robot Framework tests.

## Setting Up / Running

If you have [Poetry](https://python-poetry.org) installed you can run in this directory:

```shell
$> poetry install 
```

This project has one requirement and that is `robotframework`, version `4.X`, so you can install it with `pip` or any other package manager you may be more comfortable using.


To run any of the `.py` examples, it is as simple as:

```shell
$> python 01_core_concept.py
```


To run the `.robot` example, you can call it by:

```shell
$> robot 01_core_concept.robot
```