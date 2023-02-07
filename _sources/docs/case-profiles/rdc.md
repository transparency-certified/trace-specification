(caseprofile-rdc)=
# Research Data Centers

Jump to [TRACE in the RDC](caseprofile-trace-in-the-rdc).

[Federal Statistical Research Data
Centers](https://www.census.gov/about/adrm/fsrdc.html) (FSRDC) provide secure
environments to support researchers using restricted access data. FSRDCs are
partnerships between US statistical agencies (e.g., Census Bureau, Bureau of
Labor Statistics, Bureau of Economic Anlaysis, National Center for Science and
Engineering Statistics) and research institutions. This case profile is
focused on the U.S. Census Bureau RDCs.

## Census Bureau RDCs

The following summary is based on the Census Bureau's Center for Economic
Studies (CES) [Researcher
Handbook](https://www.census.gov/content/dam/Census/programs-surveys/sipp/methodology/Researcher_Handbook_20091119.pdf). 

### Inputs
CES microdata is confidential and protected under Title 13 of the U.S. Code.
Researchers must apply for access to RDC data. Available
[data](https://www.census.gov/topics/research/guidance/restricted-use-microdata.html)
includes administrative, demographic, and economic data products such as the
American Community Survey (ACS), American Housing Survey (AHS), Longitudinal
Employer-Household Dynamics (LEHD). Researchers must apply for access to CES
data.

Datasets are currently not assigned a persistent identifier.

### Environment
Researchers access RDC systems via a thin-client (X-Terminal). A limited range
of software is available for researcher use. All data processing is conducted
on central servers running Red Hat Enterprise Linux. The RDC network is isolated
from other networks. Not mentioned in the handbook, the [Integrated Research
Environment](https://www2.census.gov/foia/events/2017-03/2017_03_16/7_Integrated_Research_Environment_IRE.pdf)
based on PBSPro is also available (since ~2017) and a [Cloud Research
Environment](https://www.census.gov/content/dam/Census/library/publications/2022/adrm/2022-CSRM-Annual-Report.pdf) is being prototyped. Both are within the Center for Enterprise Dissemination
(CED)
 
### Outputs and disclosure review

All outputs are subject to review for potential disclosure of confidential
information. If problems are found, researchers are asked to collapse
(combine) certain cells, suppress (replace) information, or reconsider outputs
altogether. Release of "intermediate output" (not included in publication) is
discouraged. CES provides SAS and Stata programs to help with disclosure anlaysis.

### Archiving

Researchers are responsible for ensuring that artifacts are archived by moving
files to a special "archive" directory. CES policy is to archive files for seven
years.


(caseprofile-trace-in-the-rdc)=
## TRACE in the RDC

### Ingest of data
Data ingest should create permanent records of their existence at a point in
time. If preserved (ideal), should have a unique identifier, ideally public. If
not preserved or de-accessioned, a record of the when and why should be kept.

**In a nutshell: Assign DOI to input data**

### TRACE System description
A TRACE System description should be published. The format is yet undefined, but
can be an XML file with style applied (in essence, a webpage that has
structured, machine-readable content). It simply needs to exist. It is expected
that a TRACE System description does not reveal sensitive information. It should
include principles of disclosure review. To back it up, in principle, a duly
authorized person may need to inspect the systems described by the TRACE system
description.

**In a nutshell: Publish a structured webpage, and be ready to back it up.**

### TRACE System itself
A likely version of the "ideal" TRACE system is a queue system with staging,
i.e., the researcher submits a job to the queue, which is staged to a different
server, which does not allow for interaction during the execution of all
programs. In other words, all input data are read-only, all code uses only the
original, read-only input data, all copy is copied from the researcher's space
into a separate area, and all output is captured. Output, code, and indicators
of the input data (hash) are cryptographically signed. 

**In a nutshell: Implement a somewhat fancy PBS Pro queue on Census servers**

This implements a confidential version of a TRO. 

### TRO
A TRO is the object that links the input data, code, and output, subject to all
the processing by the system. The output from the confidential TRO described
above can be submitted directly to DRB-like processes. The DRB typically
modifies output further, through a standardized but manual process. The output
from the DRB (modified code, modified output) is combined with information about
the original input data (identifiers, hash), digitally signed, and published.

**In a nutshell: Implement a variation of the current DRB process with digital
signatures and (delayed) publication (with persistent identifiers)**
