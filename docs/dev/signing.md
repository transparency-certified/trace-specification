(signing)=
# Signing

Signing TROs in TRACE can be implemented using any digital signature mechanism.
The basic requirements for signing TROs are integrity (the TRO is what it is),
non-repudiability (the signer cannot deny that they signed it). The signature
mechanism determines how TROs are verified and TRACE is concerned with verifying
the signature at the time of TRO creation even if the signing key/certificate
has expired or been revoked/invalidated.  We have considered initially using
[GPG](signing-gpg) with possible future support for [X.509
certificates](signing-x509). 

A key difference between these two approaches is the underlying trust model.
In public key infrastructure (PKI), trust models define how the authenticity of
the binding between a key and its owner is determined. GPG implements a
decentralized trust model called the web of trust (WOT) and X.509 implements a
centralized trust model based on a heirarchy of certificate authorities (CA). In the
WOT model, the authenticity of keys is determined by a network of individuals who 
endorse or sign the key. In the CA model, a centralized authority is responsible for 
vetting identities. 

We can envision TRACE working in either way. Producers and consumers of TROs can
form a WOT, endorsing each others' keys. Similarly, producers and consumers of
TROs can rely on third-party CAs. Both GPG and X.509 technologies are mature,
well-documented, and ubiquitous. 

## GPG/WOT v. X.509/CA

* X.509 can be used to verify an organization or individual. GPG is intended to
  verify an individual and is bound only to an email address.
* GPG trust levels are private, specific to the individual, and often hard to
  understand. Similarly with GPG validity.
* Once sent to a keyserver, GPG keys can never been deleted but can be revoked.
* GPG keyrings can be maintained by individuals or shared.
* Keys may be revoked, compromised, or expire

(signing-gpg)=
## GnuPG (GPG)

GNU Privacy Guard (GPG) is an open-source implementation of the OpenPGP
standard ([RFC 4880](https://www.ietf.org/rfc/rfc4880.txt)). PGP is intended to
provide data integrity services via encryption, compression, and digital
signatures. For the purpose of TRACE, we are interested in the GPG digital
signature and key management capabilities.

Use case: A TRACE system owner generates a GPG key that represents the identity
of the TRACE system. A given system may have only one signing key. The system
owner distributes their signing key by publishing to a public keyserver (or
possibly a shared keyring maintained by the TRACE community). Other stakeholders
in the TRACE community validate the system owner's key via the WOT model by
signing the key. The system owner's key can be used to validate TROs signed
using the specific key.


(signing-x509)=
## X.509

X.509 is a standard defining the format of public key certificates used in a
variety of encryption and digital signature applications. X.509 certificates are
commonly used for encryption of client-server communications (e.g., TLS/SSL,
HTTPS) and electronic signatures (code signing, email signing, document
signing). The X.509 standard includes the ability to specify the purpose of a
certificate and that certificates must not be used for any other purpose than
those specified (e.g., server authentication, client authentication, code
signing, email protection, and timestamping).

There are two types of certificates: certificate authority (CA) or end-entity. A
CA certificate may be an intermediate or root certificate and can be used to
issue other certificates. End-entity certificates must either be self-signed or
signed by a CA. Certificates may identify individuals, organizations, or
domains. A TRACE System would use an end-entity certificate.

X.509 defines certificate revocation lists to distribute information about
certificates deemed invalid by a signing authority. This may include
intermediate certificates. The CILogon service provides free "end entity
certificates" based on individual user authentiaction. These can be used only
for SSL client authentication and S/MIME signing/encryption.

Code Signing certificates are typically used to assert the identity of a party
responsible for the creation of executable code and are therefore not applicable
to the TRACE system, since the TRACE system is responsible only for a record of
the execution of code created by an author. Code Signing certificates are not
free due to the process required to ensure an individual or organization's
identity. For academic software, code signing certificates are often issued only
at the institutional level. 

## Other considerations

* Attached v detached signatures: Signatures may be either attached or detached.
  For zip archives, attached signatures can be embedded in comment blocks or
  included metadata files. For detached signatures, the signature file must be 
  distributed with the TRO.
* Certificate validation and timestamping: TRACE validation is concerned with
  whether the signature was valid at the time of signing.
* Multiple signatures: Systems like Cosign support multiple signatures.
* Certificate compromise, expiration, revocation

## Worth noting

* GitHub allows users to [sign
  commits](https://docs.github.com/en/authentication/managing-commit-signature-verification/signing-commits) 
  using GPG, SSH, or S/MIME. 
* Java's jarsigner was a common approach to signing zip archives using X.509
  certificates.
* Debian developers must identify themselves by providing an OpenGPG key that is
  signed by at least two existing members of the project
  ([DebianKeyring](https://wiki.debian.org/DebianKeyring)).
* Android's original apksigner was an extension of jarsigner ([Code Signing Android and iOS
  Applications](https://www.theseus.fi/bitstream/handle/10024/155717/horn_klaus.pdf))
* [Cosign](https://github.com/sigstore/cosign) can sign any artifact pushed to
  an OCI registry and supports multiple signatures.
* [SecureApt](https://wiki.debian.org/SecureApt) and other package managers
  distribute keyrings.
