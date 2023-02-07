(trace-users)=
# Personas in TRACE

* **Author/Researcher**. A researcher creates the original (quantitative)
  resaerch, selecting data to analyze and creating software or code to conduct 
  the analysis. The research benefits from the TRACE system since they do not
  need to understand the transparency characteristics of the platform they are
  using and are assured compliance with transparency and reproducibility
  policies.             
* **TRACE Producer**. A TRACE producer is involved in provisioning data and
  computational resources for researchers. On behalf of the researcher, the
  TRACE producer verifies that the computations underlying the researcher's
  analysis are reliably performed, without the researcher intervening in the
  creation of final output products. A TRACE producer may be involved in the
  original computation (the final "production" run") or after the researcher has
  made a replication package available (for exampe, to a journal). Our primary 
  focus is the feasibility of the first scenario, but the second scenario is 
  fully consistent with this approach.
* **TRACE consumer**. A TRACE consumer is an individual or organization
  wishing to query the authenticity and reliability of the research stemming
  from a replication package. In particular, the TRACE consumer wishes to identify
  if the researcher may have manipulated the output results, whether the original
  data, if it cannot be published, was actually used. In doing so, the TRACE
  consumer will wish to ascertain aspects of the Trusted Research Object (TRO),
  such as its integrity, and aspects of the system which produced the TRO.


# Examples of personas (hypothetical)

* Census Bureau/Statistics Canada/German IAB/Bank of Portugal might act as TRACE
  producer for researchers in the (FS)RDC. Journals, other researchers, and the
  public are TRACE consumers, wishing to assess the veracity of the research
  produced using data that cannot be accessed easily or at all.
* A journal data editor might also act as TRACE producer of articles conditionally
  accepted, submitted by authors. 
* A university IT infrastructure, or a national IT infrastructure (XSEDE) might
  serve as a TRACE producer for its researchers, for instance, when data can be
  stored on campus infrastructure subject to NDA, making available a special job
  queue on their high-performance compute clusters.
* A platform such as Whole Tale or CodeOcean might act as a TRACE producer for
  users.
* A journal data editor or peer reviewer might act as a TRACE consumer,
  assessing the conformance of research conducted on a TRACE system to 
  transparency and reproducibility policies.
* Other researchers, replicators, and the broader scientific community  are also
  TRACE consumers.
