(conceptual-model)=
# Conceptual Model

This section describes the TRACE conceptual model in detail:
* A **Transparent Research Object (TRO)** is a pairing of a **TRO declaration** and a **TRO composition**.
* The **TRO composition** comprises all of the digital artifacts and (potentially unpersisted) bitstreams that the **TRO declaration** describes. 
* The **TRO composition** does *not* include the **TRO declaration** that describes it.
* Any number of **TROs** can share the same **TRO composition**.
* A **TRO declaration** and the **TRO composition** it describes can be stored and shared separately or together, and different components of the TRO composition may be stored separately and shared independently
  * Example: If a **TRO declaration** is stored in a single archive (e.g. zip) file together with other digital artifacts, the TRO composition is not equivalent to the contents of the archive file. The TRO declaration in this case may describe all of the contents of the archive other than the TRO declaration. Or it may describe only some of the contents of the archive; or it even may describe artifacts not included in the archive at all.
* The **TRO composition** referred to by a **TRO declaration** is uniquely
  identified by a **TRO composition fingerprint** (or **composition fingerprint**)
* A **composition fingerprint** is a digest over a concatenation of the sorted digests of the individual digital artifacts and bitstreams comprising the **TRO composition**.
* A **composition fingerprint** is independent of artifact (e.g. file) names and resource paths identifying or locating the artifacts.
* A **TRO declaration** *minimally* includes (expressed in TRACE vocabulary):
  * The *unique ID* and *public key* of the **Trusted Research System (TRS)** that digitally signed the TRO declaration.
  * The **composition fingerprint**.
  * A **TRO declaration timestamp** (or **declaration timestamp**) indicating when the TRO declaration was signed by the TRS. 
  * The URL and public key of the authorized timestamp server that provided the timestamp. 
* A **TRO declaration** optionally (and almost alway) will includes:
  * TRACE-vocabulary expressed claims about the associated **TRS**. Typically this will be a complete copy of the **TRS certificate**.
  * TRACE-vocabulary expressed claims about this specific **TRO**.
  * List of and means to identify each of the  individual digital artifacts and bitstreams comprising the **TRO composition**. E.g., for *each* artifact in the **TRO composition**:
    * Zero or more resource paths (e.g. file names) associated with the artifact.
    * A digest of the bits comprising the artifact.
* A **TRO declaration** on its own *cannot* prove that it (the TRO declaration) was produced by the **TRS** it claims produced and signed it. 
* Instead, this proof is provided with a digital signature of the **TRO declaration** which is delivered as a separate TRS signature file.
* A **TRS signature** is conceptually equivalent to an encrypted digest of the contents of **TRO declaration** (*not* the contents of the **TRO composition**), where the encryption is performed using the private key of the **TRS**. 
* Verifying a **TRS signature** is conceptually equivalent to decrypting the encrypted digest of the **TRO declaration** and confirming that the decrypted digest is in fact the digest of the **TRO declaration**.
* Verifying a **TRS signature** proves (1) that the **TRS signature** was produced by a particular **TRS**, and (2) that the **TRO declaration** is bit-for-bit identical to the **TRO declaration** that the TRS signed.
* Because a **TRO declaration** must include the **composition fingerprint** that identifies the artifacts it describes, the **TRS signature** additionally proves that the **TRS** intended to associate the **TRO declaration** with the **TRO composition** identified by the composition fingerprint. 
* Because the validity of a keypair associated with a **TRS** may be limited in time, either due to scheduled expiration or explicit revocation, the date on  which a **TRS** private key was used to sign a **TRO declaration** must also be established authoritatively.
* A **TRO declaration**, and the associated **TRS signature file**, together must be time-stamped by a **Time Stamping Authority** (**TSA**, see RFA 3161 TSA), such as https://www.freetsa.org, which typically will be managed independently of the TRS.
* A **TRS** generates a signed timestamp for each **TRO** it endorses by sending a digest of the concatenation of the **TRO declaration** and the **TRS signature** to a TSA and stores the response from the TSA in a Trusted Timestamp file that subsequently can be used to verify that the associated **TRO declaration** and **TRS signature files** were not modified since they were timestamped.

