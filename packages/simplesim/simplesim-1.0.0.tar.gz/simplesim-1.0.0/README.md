![](https://github.com/MeelonUsk/simplesim/workflows/Continuous%20Integration/badge.svg)
[![codecov](https://codecov.io/gh/MeelonUsk/simplesim/branch/master/graph/badge.svg)](https://codecov.io/gh/MeelonUsk/simplesim)

# `simplesim` package
This package is a simple and general framework for creating a simulation
environment. `simplesim` uses the observer design pattern that allows arbitrary
objects to be included into the simulation. At each update, `simplesim` notifies
the observers of the new simulation time. The observers can do what they want
with that information.

`simplesim` is designed to easily be extended. The only requirement is that
custom objects must implement the observer interface defined in the package.  