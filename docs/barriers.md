# Barriers to Transparency

(barriers-self-certification)=
## "Self-certification" of research artifacts

Most journals have long allowed authors to (implicity or explicitly) assert that
the provided artifacts are sufficient to correctly reproduce results. Many
documented problems with such self-certified packages have led an increasing
number of venues to actively verify such assertions during peer review by 
independently verifying that the code, computing environments, and workflows
described in a publication actually reproduce the results.

With self-certification, there is no guarantee that the provided artifacts are
complete, that they were actually used to obtain reported results, or that they
have not been modified (intentionally or unintentionally).

```{admonition} TRACE Requirement
System owners must be able to certify the integrity of computational results
and data obtained using their systems. Researchers must be able to reliably
share the code, data, and methods used (or information about them) and
demonstrate that these artifacts were used to obtain computational results
within a specific system.
```

(barriers-sensitive-proprietary)=
## Use of sensitive and proprietary data

Research in the social sciences often relies on access to {term}`sensitive <Sensitive data>` 
or {term}`proprietary <Proprietary data>` data that cannot be redistributed
and, in many cases, is only accessible to authorized users on [access-controlled
resources](barriers-large-specialized-compute). This includes data collected by
researchers and stored on secure infrastructure at their institutions;
confidential private-sector, school district, or government administrative data;
as well as data from national statistical agencies. The results of research may
further be subject to {term}`disclosure avoidance <Disclosure avoidance>`
processes.

```{admonition} TRACE Requirement
System owners must enable researchers to reliably demonstrate how data were used
to obtain reported results if the data cannot be shared. 
```

(barriers-streaming-transient-ephemeral)=
## Use of streaming, transient, and ephemeral data

{term}`Streaming <Streaming data>`, {term}`transient <Transient data>`, and
{term}`ephemeral <Ephemeral data>` cannot be preserved for privacy reasons,
terms of use, or because the scale of the data prevents long-term archiving. 
Examples include the GDPR's right to erasure [33] and Twitter terms of use [34].

```{admonition} TRACE Requirement
System owners must enable researchers to reliably demonstrate how data were used
to obtain reported results if the data no longer exist or cannot be preserved.
```

(barriers-large-specialized-compute)=
## Use of very large-scale and specialized computational resources

Many researchers rely on large-scale computational resources provided by campus,
state, or national cyberinfrastructure. These resources are both access
controlled and time constrained, in that they are decommissioned after a period
of time. It is unlikely that research conducted on these systems can be repeated
without access to considerable time, labor, expertise, and technological
resources.

```{admonition} TRACE Requirement
System owners must enable researchers to reliably demonstrate how computations
where executed using large-scale and specialized computational resources.
```


(barriers-additional-barriers)=
## Additional barriers

* Input data cannot be accessed
*Input data is dynamically loaded from external sources and is not retained
*Computational steps are inadequately described
*Insufficient information is provided about the computational environment
*Outputs are not provided
*It is not possible to determine whether the provided code, inputs, or
 environment were actually used to generate reported results*
*Insufficient information about computational resources used (such as cores,
memory, or time)*

