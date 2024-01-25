(caseprofile-rdc)=
# Federal Research Data Centers

Jump to [TRACE in the FSRDC](caseprofile-trace-in-the-rdc).

[Federal Statistical Research Data
Centers](https://www.census.gov/about/adrm/fsrdc.html) (FSRDC) provide secure
environments to support researchers using restricted access data. FSRDCs are
partnerships between US statistical agencies (e.g., U.S. Census Bureau, Bureau of
Labor Statistics, Bureau of Economic Anlaysis, National Center for Science and
Engineering Statistics) and research institutions. 
The following summary is based on the FSRDC's [Researcher
Handbook](https://psurdc.psu.edu/sites/rdc/files/2021-07/Researcher_Handbook_1208020.pdf). 
We use the example of Census Bureau data, but the case applies more generally.

### Inputs

Census Bureau data accessible via the FSRDC is confidential and protected under Title 13 of the U.S. Code.
Researchers must apply for access to data covered under Title 13. Available
[data](https://www.census.gov/topics/research/guidance/restricted-use-microdata.html)
includes administrative, demographic, and economic data products such as the
American Community Survey (ACS), American Housing Survey (AHS), Longitudinal
Employer-Household Dynamics (LEHD). 

Datasets are currently not assigned a persistent public identifier, though a Census Bureau internal database tracks data made available through the FSRDCs.

### Environment

Researchers access FSRDC systems via a remote desktop interface (Citrix-based), which in turn connects to the internal compute cluster via a software thin-client (NX). The Linux compute cluster is known as the [Integrated Research
Environment](https://www2.census.gov/foia/events/2017-03/2017_03_16/7_Integrated_Research_Environment_IRE.pdf). 
A controlled list
of software is available for researcher use. Jobs are scheduled using PBSPro. Nearly all data processing is conducted
on the IRE, and this case will concentrate on that modal access scenario. The FSRDC network is isolated
from other networks. 

Other environments not considered in this case are a prototype [Cloud Research
Environment](https://www.census.gov/content/dam/Census/library/publications/2022/adrm/2022-CSRM-Annual-Report.pdf) and custom Windows access for specific software.
 
### Outputs and disclosure review

All outputs are subject to review for potential disclosure of confidential
information. This disclosure review is conducted by the agency providing the data, *i.e.*, the Census Bureau's Disclosure Review Board (DRB) reviews output that is based on Census Bureau data, the Bureau of Labor Statistics reviews output that is produced from BLS data, etc.  
To prepare disclosable output,  researchers are asked modify data by applying various disclosure avoidance techniques, such as collapsing
(combine) certain cells, suppressing or replacing information, or adding noise. Some output may not be disclosable. Release of "intermediate output" (not included in publication) is
discouraged. The FSRDC system provides SAS and Stata programs to help with disclosure anlaysis.

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

A TRACE System description should be published. The content should conform to the [TRACE System](element-trace-system), and could be made human-readable as a  webpage that has
structured, machine-readable content. It is expected
that a TRACE System description does not reveal sensitive information. It should
include principles of disclosure review. In principle, a duly
authorized person may need to inspect the systems described by the TRACE system
description.

**In a nutshell: Publish a structured webpage, and be ready to provide evidence of audit or inspection.**

### TRACE System itself

A likely version of the "ideal" TRACE system is a queue system with staging,
i.e., the researcher submits a job to a special queue that "stages" (copies) to a different
file system or server, to ensure that no user interaction is possible during the execution of all
programs. In other words, all input data are read-only, all code uses only the
original, read-only input data, all copy is copied from the researcher's space
into a separate area, and all output is captured. Output, code, and indicators
of the input data (hash) are cryptographically signed. 

**In a nutshell: Implement a somewhat fancy PBSPro queue on Census servers**

The TRO produced by this TRS would *a priori* be confidential, since it contains raw output that has not yet been vetted by the Census Bureau's DRB. 

### TRO

A TRO is the object that links the input data, code, and output, subject to all
the processing by the system. The output from the confidential TRO described
above can be submitted directly to the DRB processes. The DRB may
modify output further, through a standardized (possibly manual) process. The output
from the DRB (modified code, modified output) is combined with information about
the original input data (identifiers, hash), digitally signed, and published.

**In a nutshell: Implement a variation of the current DRB process with digital signatures and (delayed) publication (with persistent identifiers)**
