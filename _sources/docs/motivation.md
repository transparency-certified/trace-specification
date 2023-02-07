# Motivation

*How can we trust the integrity of results from research that relies on
computations without repeating them?*

Research communities across the sciences face a conundrum: to ensure the
transparency and reproducibility of computational results, they require that
authors share the data, code, and methods used to obtain them. However, without
verification by repeating the computations, there is no guarantee that the
author-provided artifacts are complete or can actually be used to reproduced
results.

Particularly problematic are studies that employ [sensitive or proprietary
data](barriers-sensitive-proprietary) for which access and reuse are restricted; 
[streaming, transient, or ephemeral data](barriers-streaming-transient-ephemeral)
that cannot be used to verify reproducibility due to their dynamic nature; or 
[very large-scale or specialized computational
resources](barriers-large-specialized-compute) available only to authorized
users. In these cases, verification by repeating computations may not be
possible.

TRACE presents a solution to this problem: certify the successful
<u>*original*</u> execution of the computational workflow that produced the
reported findings *in situ*. We call this **certified transparency**&mdash;a
trustworthy record of computations signed by the systems within which they were
performed.
