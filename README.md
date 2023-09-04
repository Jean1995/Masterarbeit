# Master Thesis 

The template used in this thesis has been made by [Maximilian Nöthe](https://github.com/MaxNoe/tudothesis)


# Bugs, issues and errata

* The creation of the two-dimensional logarithmic histogram has a bug when using version 2 of matplotlib (e.g. python2), the bins are going to be disturbed
* The folder "build/numbers" may not be created in some cases and may have to be created manually to make the script work
* Figure 4.3: The plot actually shows the energy loss per distance, not per grammage. Therefore, the values on the y-Axis need to be corrected by the factor of the mass density of air.
* In the deviation of the energy integral, equation (2.10) loses a minus sign in the first step. Furthermore, exp(0)=0 instead of exp(0)=1 is falsely assumed in the third line.
