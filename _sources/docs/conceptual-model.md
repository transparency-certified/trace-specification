(conceptual-model)=
# Conceptual Model (v4)

The TRACE model defines the entities and relationships required to describe and
represent Transparent Research Objects (TROs) and the Transparent Research
Systems (TRSs) that produce them.

This section describes the current revision of TRACE conceptual model in detail.
The model is demonstrated via the
[trace-model](https://github.com/transparency-certified/trace-model) repository
and implemented in the [TRACE Prototype](./trace-prototype) service.

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
* A **TRO** declaration may optionally specify one or more **artifact arrangements**.  An **artifact arrangement** specifies the location of one or more of the artifacts included in the **TRO composition**. Multiple locations for a single artifact may be indicated by including it in multiple arrangements. 
* A **TRO declaration** additionally may specify one or more **research performances**.
A **research performance** may **access** (read data from) one or more **artifact arrangements**, and **contribute** to (write data to) one or more other **artifact arrangements**.
  * Example: The execution of a single program on a set of input files to produce a set of output files can be represented as a single **research performance** (the program execution) that **accesses** (the input files in) one **artifact arrangement** and **contributes** (the output files) to another **artifact arrangement**.
* The trustworthy characteristics of a **research performance** may be enumerated by assigning to it one or more **performance attributes** that indicate the conditions guaranteed by the **TRS** during that performance.  Each **performance attribute** assigned to a **research performance** must be **warranted by** a corresponding **TRS capability** that was declared within the **TRS certificate** at the time the latter was signed.
  * Example:  Assigning the **performance attribute** "internet isolation" to a **research performance** (making the claim that the performance was carried out in isolation from the Internet) also requires specifying the corresponding **TRS capability** that warrants this claim (e.g. "internet isolation capability"), that in turn must be enumerated within the signed **TRS certificate** (along with all the other certified capabilities of the **TRS**). 

## Instance examples

The following examples illustrate different possible configurations of a TRO. 

```{figure} images/trace-instance-1.png
---
name: trace-instance-1
height: 20em
---
A TRO with a payload of two files in a filesystem, along with a TRO declaration in the same directory. Emphasize that the TRO declaration is not part of the payload.
```

```{figure} images/trace-instance-2.png
---
name: trace-instance-2
height: 20em
---
A TRO with a payload of two files stored in a single zip, where the TRO declaration is outside of the zip file.
```

```{figure} images/trace-instance-3.png
---
name: trace-instance-3
height: 20em
---
A TRO with a payload of two files stored in a single zip, where the TRO declaration is inside the same zip file. Emphasize that even though the declaration is in the zip, it is not part of the payload, and does not contribute to the fingerprint.
```

```{figure} images/trace-instance-4.png
---
name: trace-instance-4
height: 20em
---
A TRO with a payload of three files, two small files in a zip file, and a third huge file on a web server (500 GB datafile).
```

```{figure} images/trace-instance-5.png
---
name: trace-instance-5
height: 20em
---
A TRO with a payload of 20 files in a BDBAG. The TRO declaration includes a TRO Artifact Record for each of these 20 data files in the BDBAG, where each record has a file path and a digest.
```

```{figure} images/trace-instance-6.png
---
name: trace-instance-6
height: 20em
---
A TRO with a payload of 20 files in a BDBAG. The TRO declaration contains NO artifact records, but instead refers to the BDBAG manifest.
```

```{figure} images/trace-instance-7.png
---
name: trace-instance-7
height: 20em
---
A TRO with a payload of 21 files, where 20 files in a BDBAG and one huge file on a web server. The TRO declaration refers to the BDBAG manifest, and declares an additional Artifact Record for the 21st file.
```
