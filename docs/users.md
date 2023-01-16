(trace-users)=
# TRACE Users and Roles

We consider the following to be the primary users or roles of TRACE.

* **Research producer (U1)**. The scientist (or team) who conducts research
  using a computational platform/system.
* **System owner (U2)**. The owner of a computational platform or system within which
  computational research is conducted. In general, U2 need not be distinct from
  U1 (for example, if the system is the researcher’s laptop), but for the
  purposes of this project will be expressly assumed to be a third party not
  directly involved in the research conducted by U1. For example: Whole Tale,
  campus research cluster, or journal reproducibility  verification procedures.
* **Research Consumer (U3)**. Has an interest in knowing if the research can be
  trusted and specifically whether and how research artifacts were actually
  used to obtain results. Consumes (reads, reuses) outcomes of research
  (articles, data) and in this model, signals of its transparency and
  reliability (certificates).  
* **Research Intermediaries or Platforms (U4)**. Intermediate between U1 and U3
  and have or support policies concerning the integrity, transparency, and
  reproducibility of computational results. For example: journals, data portals,
  science gateways, working paper archives, statistical agencies, research data
  repositories.  
* **Research Verifier (U5)**. Evaluates computational research artifacts for
  conformance with policies established by U4, potentially including repeating
  computations to verify reported results. In the context of this model, U2, U3,
  U4 could be verifiers. For U3 and U4 acting as verifiers, verification is a
  costly ex-post process of repeating computational analysis. Since U1 and U2
  are the originators of computational analysis, they are generally not in the
  role of U5. Examples: LDI, Odum, or the Certification Agency for Scientific
  Code and Data (cascad).
* **System auditor (U6)**. An expert with respect to research transparency who
  needs to be able to verify the transparency qualities asserted by U2 via a TRACE
  certificate.
 

A central goal of TRACE is to address how system owners (U2) can be efficient
and trusted "verifiers" in the sense of ensuring the transparency of
computational research executed within their system.  This is efficient because
U2 does not need to repeat the computational analysis, reducing the burden on U1
to conform to community or journal policies as well as the burden on U3, U4, and
U5 to assess the integrity of computational artifacts. U2 will be trusted by
adopting the TRACE model, which provides them with the tools to convey that the
original computation was conducted in a repeatable way; that the computational
artifacts used can be packaged or well-described; and that computational results
can be reproduced with a very high likelihood.
