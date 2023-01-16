# TRACE Elements

The TRACE project is developing a set of infrastructure elements that can be
employed by system owners to:

1. declare the dimensions of computational transparency supported by their
   platform;
2. certify that a specific computational workflow was executed on the platform; and
3. bundle artifacts along records of their execution and certify them for
   dissemination.

(element-trace-system)=
## Transparency-Certified System (TRACE System)

At the core of the TRACE model is the Transparency-Certified System (TRACE
System).  We consider a TRACE System to be any structured
process that can be used to generate a [TRO](element-tro). This may be a
specific computational platform; a special queue in a job scheduling system; or
a person-centric documented workflow. The purpose of the TRACE System is to
certify that a computational workflow was executed and to convey details about
how the system ensures results transparency.

(element-trace-certificate)=
## TRACE System Certificate

TRACE Systems specify how transparency is supported by their platform via a
TRACE System Certificate.

A TRACE System Certificate is a structured document that describes how TROs are
produced by a TRACE System and how the system ensures results transparency and
reproducibility. TRACE System Certificates are digitally signed by the system
owner and supported by the system owner's reputation. 

(element-tro)=
## Transparency-Certified Research Objects (TRO)

TRACE Systems produce Transparency-Certified Research Objects (TROs) which can
be used for dissemination and review. 

A TRO is an aggregation of computational research artifacts, records of their
execution within a particular system, technical metadata about their contents,
digitally signed by the system within which they are executed. The central
purpose of a TRO is to provide a trustworthy record of computations used to
obtain results, eliminating the need for verification through repeating
computations. TROs are produced by TRACE Systems and may be consumed by other
researchers, replicators, or reviewers. The TRO will be signed by the system
owner using a digital signature. The integrity of the TRO can be verified using
the affixed signature.

