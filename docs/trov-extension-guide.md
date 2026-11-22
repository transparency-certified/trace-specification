# TROV Extension Guide
<span class="draft-badge">
  TROV 0.1 DRAFT</span>

*This document is a draft and subject to revision.
Please [submit feedback or report issues](https://github.com/transparency-certified/trace-specification/issues/new?title=trov-extension-guide.md:%20).*

How to extend the TRACE model with institution-specific terms in TRO declarations using your own namespace, so that custom terms coexist with TROV terms without conflict.

| Section | Description |
|---------|-------------|
| [Using Your Own Namespace](#using-your-own-namespace) | Choosing a namespace, adding it to the `@context`, and using and declaring custom terms |
| [How TRO Validation Handles Extensions](#how-tro-validation-handles-extensions) | How a TRO declaration is validated while allowing extensions |
| [Extending TROV with Custom Types](#extending-trov-with-custom-types) | Defining custom capability and performance attribute types |
| [Aligning with Future Versions](#aligning-custom-terms-with-future-trov-versions) | Alignment when a custom term is later standardized in TROV |

---

(using-your-own-namespace)=
## Using Your Own Namespace

### 1. Choose a namespace and prefix

Pick a namespace URI under an Internet domain you own. The URI is the durable identifier for your terms. The prefix is just a shorthand used within a given TRO declaration:

```json
"mytrs": "https://example.org/mytrs#"
```

Use a prefix that is short, lowercase, and recognizable to your team.

### 2. Add the prefix to your `@context`

The `@context` block in a TRO declaration maps prefixes to namespace URIs. Add your prefix alongside the standard prefixes:

```json
"@context": {
    "rdf":    "http://www.w3.org/1999/02/22-rdf-syntax-ns#",
    "rdfs":   "http://www.w3.org/2000/01/rdf-schema#",
    "trov":   "https://w3id.org/trace/trov/0.1#",
    "schema": "https://schema.org/",
    "mytrs":  "https://example.org/mytrs#",
    "@base":  "https://example.org/tro/3f2a9c/"
}
```

### 3. Use prefixed property names for your metadata

Wherever you add custom metadata, use your prefix:

```json
{
    "@id": "https://example.org/",
    "@type": "trov:TrustedResearchSystem",
    "schema:name": "My Research System",
    "trov:hasCapability": [ ... ],
    "mytrs:version": "0.0.1",
    "mytrs:architecture": "x86_64",
    "mytrs:kernelVersion": "6.14.0-37-generic",
    "mytrs:imageRepoDigests": ["dataeditors/stata18_5-mp@sha256:3699b018..."]
}
```

These steps are sufficient for plain data properties. If your custom terms extend TROV classes, as new capability or performance attribute types do, they also need declarations so that validators can recognize them, as described in step 4 below.

### 4. Declare custom types that extend TROV classes

If your TRS introduces custom capability or performance attribute types, declare each one in a `trov:customTerm` array in the TRS declaration, as explained more fully in [Extending TROV with Custom Types](#extending-trov-with-custom-types). This tells validators that the custom type is a legitimate value for the property and allows it to participate in warrant chains:

```json
"trov:customTerm": [
    {
        "@id": "mytrs:CanProvideAuditLogging",
        "rdfs:subClassOf": { "@id": "trov:TRSCapabilityType" }
    }
]
```

For background on how warrant chains work, see [Warrant Chains](tro-declaration-format.md#the-warrant-chain).

---

(how-tro-validation-handles-extensions)=
## How TRO Validation Handles Extensions

A TRO declaration is validated at several levels: as JSON, as JSON-LD, as a correct use of TROV, and as a graph of linked elements, using means such as JSON Schema and SHACL shapes. At every level, validation checks that each term is defined by TROV, declared in your own namespace, or provided by another declared vocabulary:

- **`trov:` terms** are confirmed to be terms TROV defines, and used as TRACE requires; `trov:` terms that TROV does not define are rejected.
- **Terms in your own namespace**, with a prefix defined in the `@context`, are permitted; custom capability and attribute types must also be declared as described in [step 4](#using-your-own-namespace).
- **Terms from other vocabularies**, such as `rdf:`, `rdfs:`, `schema:` or `dcterms:`, are permitted, with each prefix defined in the `@context` and mapped to the vocabulary's standard namespace.
- **Unprefixed terms**, other than JSON-LD keywords, are rejected.

---

(extending-trov-with-custom-types)=
## Extending TROV with Custom Types

The TROV vocabulary predefines capability and performance attribute types. Adopters whose TRS uses types TROV does not yet define can declare custom types in their own namespace.

### Which custom terms need declarations?

Custom capability and performance attribute types need declarations connecting them to the TROV classes they extend. They are used as the `@type` of capabilities and performance attributes, and without the declarations, validators cannot confirm that they are legitimate types for those elements.

Custom terms that are plain data properties, additional metadata on an element, need only your own prefix (e.g. `mytrs:`), with no declaration in the TRO declaration. JSON consumers use them directly, and RDF consumers treat them as ordinary triples. Defining them in a vocabulary file at your namespace URI is still good practice.

For example, `mytrs:architecture` is a plain string property in the TRS declaration. It doesn't extend any TROV class and needs no declaration. But `mytrs:CanProvideAuditLogging`, used as the `@type` of a capability, needs to be declared as a kind of `trov:TRSCapabilityType` so that validators can recognize it.

### Declaring custom types in the declaration

To make a TRO declaration self-contained for validation, declare your custom types in the TRS's `trov:customTerm` property, one entry per type, each stating which TROV class the type extends:

```json
{
    "@id": "https://example.org/",
    "@type": "trov:TrustedResearchSystem",
    "schema:name": "My Research System",
    "trov:customTerm": [
        {
            "@id": "mytrs:CanProvideAuditLogging",
            "rdfs:subClassOf": { "@id": "trov:TRSCapabilityType" }
        },
        {
            "@id": "mytrs:AuditLogging",
            "rdfs:subClassOf": { "@id": "trov:TRPAttributeType" }
        }
    ],
    "trov:hasCapability": [ ... ]
}
```

You may also publish these declarations in a vocabulary file at your namespace URI, but TRACE requires them in the TRS declaration of every TRO declaration that uses them.

### Using custom types in a TRO declaration

Once declared, custom types are used exactly like the predefined ones, and take part in warrant chains through `trov:warrantedBy`:

```json
"@context": {
    "trov":  "https://w3id.org/trace/trov/0.1#",
    "rdfs":  "http://www.w3.org/2000/01/rdf-schema#",
    "mytrs": "https://example.org/mytrs#"
},
...
"trov:hasCapability": [
    {
        "@id": "https://example.org/capability/internet-isolation",
        "@type": "trov:CanProvideInternetIsolation"
    },
    {
        "@id": "https://example.org/capability/audit-logging",
        "@type": "mytrs:CanProvideAuditLogging"
    }
],
...
"trov:hasPerformanceAttribute": [
    {
        "@id": "trp/0/attribute/0",
        "@type": "trov:InternetIsolation",
        "trov:warrantedBy": { "@id": "https://example.org/capability/internet-isolation" }
    },
    {
        "@id": "trp/0/attribute/1",
        "@type": "mytrs:AuditLogging",
        "trov:warrantedBy": { "@id": "https://example.org/capability/audit-logging" }
    }
]
```

---

(aligning-custom-terms-with-future-trov-versions)=
## Aligning Custom Terms with Future TROV Versions

If a concept you defined in your namespace is later standardized as a `trov:` term (for example, if a future version of TROV adds `trov:cpuArchitecture`, and this term fully captures the concept represented by your custom `mytrs:architecture` term), consider using the standard term in new declarations. Existing TRO declarations employing the custom term remain valid.

---

## History

| Date | Change |
|------|--------|
| 2026-11-20 | Limited custom types to capability and performance attribute types. |
| 2026-03-26 | Added `trov:customTerm` and embedded type declarations for custom capabilities, attributes, and signing mechanisms. |
| 2026-02-23 | Initial publication. |

