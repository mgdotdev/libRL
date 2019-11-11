# Contributing

## Coding Style
The libRL library follows
[PEP8](https://www.python.org/dev/peps/pep-0008/) to a general degree,
though some exceptions are made when it comes to known error handling.

Docstrings should follow
[reStructuredText style](http://docutils.sourceforge.net/docs/ref/rst/restructuredtext.html)
in a similar structure to the docstrings currently present in libRL so
to maintain homogeneity in the sphinx website. 

## PR Submission
Features should be developed in a branch with a descriptive name and the
pull request (PR) submitted into a `develop` branch. In order to be
merged a PR must be approved by one authorized user and the build must
pass.

A passing build requires the following:

* All tests pass
* Every line of code is executed by a test (100% coverage)