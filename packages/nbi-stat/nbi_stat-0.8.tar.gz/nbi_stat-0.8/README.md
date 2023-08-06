# Statistical tools for teaching at NBI 

This package extends some of the existing tools in
[_NumPy_](https://numpy.org) and [_SciPy_](https://scipy.org) with
some useful features designed to make life easier for the students at
the Niels Bohr Institute. 

## Topics

- Reporting scientific results, including proper rounding 
- Tabulation of data useful in Jupyter Notebooks 
- Visualisation of data in 1 and many dimensions 
- Robust calculations of sample means, variances, and covariances, for
  unweighted and weighted samples.  For weighted samples, both
  _frequency_ and _non_-frequency weights are supported. 
- Histogramming 
- Sampling of arbitrary PDFs 
- Curve fitting using 
  - Linear least squares 
  - Non-linear least squares 
  - Maximum likelihood estimates 
    - Extended 
    - Binned 
- Representation of fit confidence contours 
- Hyppthesis testing 
- Confidence intervals 
- Template fitting 
- Simultaneous fitting over regions (channels)
- Likelihood calculations 

## Examples of use 

[This
notebook](https://cholmcc.gitlab.io/nbi-python/statistics/#nbi_stat_exa)
gives examples of use. 

## Book on Statistics with Python 

The book [Statistics Overview - With
Python](https://cholmcc.gitlab.io/nbi-python/statistics/#Statistik)
lays out much of the theoretical foundation for the tools available. 

Some other notes on statistics is available from the same site, including 

- [Principle Component Analysis](https://cholmcc.gitlab.io/nbi-python/statistics/#PCA) as a more robust alternative to boosted decision trees 
- [Bootstrap and Jackknife](https://cholmcc.gitlab.io/nbi-python/statistics/#Boostrap) and why you should be careful with these estimates 
- [Coefficent of determination](https://cholmcc.gitlab.io/nbi-python/statistics/#R2) and why you shouldn't use it 

## Application Programming Interface Documentation 

The API is
[documented](https://cholmcc.gitlab.io/nbi-python/statistics/nbi_stat). 

2019 © _Christian Holm Christensen_
