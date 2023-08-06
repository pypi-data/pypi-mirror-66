[![Build Status](https://travis-ci.org/datadriventests/ddt.svg)](https://travis-ci.org/datadriventests/ddt)
[![codecov.io](https://codecov.io/github/datadriventests/ddt/coverage.svg?branch=master)](https://codecov.io/github/datadriventests/ddt)
<br />
[![Version](https://img.shields.io/pypi/v/ddt.svg)](https://pypi.python.org/pypi/ddt2)
[![Downloads](https://img.shields.io/pypi/dm/ddt.svg)](https://pypi.python.org/pypi/ddt2)

DDT2 (Data-Driven Tests) allows you to multiply one test case
by running it with different test data, and make it appear as
multiple test cases.

# Installation


```pip install ddt2```

Check out [the documentation](http://ddt2.readthedocs.org/) for more details.

See [Contributing](CONTRIBUTING.md) if you plan to contribute to `ddt`,
and [License](LICENSE.md) if you plan to use it.

I Modify ddt to ddt2 for i want to get some features, and not all functions of ddt can be uesed
1. use version as ddt, and add the forth part as my modification, but add 10 to major verion, such as 1.3.0-> 11.3.0.1
1. get the determined name of test case
1. support for __var__  to generate case 
1. support for __i__ to have index
1. parameter in a test function should not have i
1. add function decorators autoindex
1. @data_file add xlsx support, for example @data_file("a.xlsx", sheet="Sheet2"), if this feature used, openpyxl must be installed



  
