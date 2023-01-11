# Glossary

A glossary of common terms used in the TRACE project.

```{glossary}

Reproducibility
    Obtaining consistent results using the same input data, computational steps,
    methods, and code, and conditions of analysis [16].

Transparency
    The reporting of materials and methods in a manner that provides enough
    information for others to independently assess and/or reproduce findings
    (adapted from FASEB [29]). Research object (RO): Standards-based method of
    bundling and describing research artifacts, typically via linked-data
    technologies [31]. 

Computational artifacts
    Inputs, code, outputs, documentation and relevant details of the computational
    environment required to ensure the transparency and reproducibility of results
    obtained through computational means.

Input
    any file, database, or stream that is used by a computational workflow (or
    workflow step) to obtain reported results. Examples include data and
    configuration files.

Code
    Scripts and/or source code that are not part of an installed software package
    and used to execute steps of a computational workflow used to obtain reported
    results. This includes code for data preparation, analysis, modeling, plotting,
    etc., and is considered separate from the operating system or any installed
    software packages (see environment below). 

Output
    Information created by a computational workflow (or workflow step) used to
    obtain reported results. Examples of outputs include: cleaned or otherwise
    pre-processed datafiles used for analysis; analytical or simulation results;
    tables, figures, and numerical results; log files and other program outputs,
    messages, and errors (e.g., stderr, stdout, log files).

Environment
    The specific set of operating system and dependent software versions used to
    execute a computational workflow used to obtain reported results. The
    computational environment may be described as a list of operating system and
    software versions or as a virtual machine or container image.

Documentation
    Materials providing additional information required to reproduce reported
    results including step-by-step instructions for obtaining or accessing data;
    setting up or accessing the environment; and running the complete computational
    workflow.

TRACE workflow
    The complete sequence of steps taken to create and release a TRO from
    author-provided artifacts. TRACE workflows may be manual or automated and may
    include actions such as disclosure avoidance measures.

Sensitive data
    Information that may be regulated by law due to possible risk of harm due to
    their disclosure. 

Proprietary data
    Information for which the rights of ownership are restricted so that the
    ability to freely distribute the data is limited. (USGS)

Transient data
    Information that is not persisted.

Ephemeral data
    Information that change rapidly over time and may be lost if not collected
    immediately.

Streaming data
    Information that is generated continuously, generally in large volumes, and
    must be processed sequentially and incrementally over time (adapted from 
    https://aws.amazon.com/streaming-data/). Examples include information from
    social networks, financial trading floors, and telemetry from connected
    devices.

Disclosure avoidance
    Methods of protecting confidentiality that may require modification of data. 
    (https://www.census.gov/topics/research/disclosure-avoidance.html)
    

```
