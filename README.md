# ATLAS

ATLAS is the relationship, navigation, and reconstructable-state environment.

ATLAS is a map.

ATLAS is not identity, byte truth, authorization, execution, verification, or sealing.

The core separation is:

\[
\boxed{
\text{ZiD}=\text{persistent identity}
}
\]

\[
\boxed{
\text{CID}=\text{exact bytes}
}
\]

\[
\boxed{
\text{ZDS}=\text{placement/address indexing}
}
\]

\[
\boxed{
\text{ATLAS}=\text{relationships/navigation}
}
\]

\[
\boxed{
\text{RAZAIEL}=\text{authorization}
}
\]

ATLAS links references without impersonating them.

## ATLAS versus Atlas Index

The distinction is deliberate:

\[
\boxed{
\text{Atlas Index}
\rightarrow
\text{ingest / lookup / projection records}
}
\]

\[
\boxed{
\text{ATLAS}
\rightarrow
\text{relationship graph / navigation environment}
}
\]

An Atlas Index ID is a stable lookup key for a projection. It is not the ZiD, not the CID, and not authority.

## Two coordinated faces

### Internal ATLAS

Maps where system objects fit:

- objects and artifacts;
- ZiD identity references;
- CID byte references;
- ZDS placement references;
- project, subsystem, and role;
- lineage and dependencies;
- provenance and verification references;
- control and automation relationships;
- lifecycle state;
- predecessor and successor relationships.

### External ATLAS

Maps relationships among:

- claims;
- sources;
- methods;
- perspectives;
- evidence;
- conflicts;
- annotations.

Views may change while the referenced object remains the same.

## Canonical law

\[
\boxed{
\text{relationship}\neq\text{authority}
}
\]

and

\[
\boxed{
\text{displayed seal}\neq\text{truth}
}
\]

ATLAS may record that an object was authorized, witnessed, verified, or sealed by another subsystem.

ATLAS may not create those facts.

## Reference kernel

This repository includes a deterministic Python reference kernel for:

- Atlas Index ID generation;
- node validation;
- typed relationship edges;
- lineage traversal;
- neighborhood traversal;
- canonical export;
- graph integrity checks.

Status: **v0.1 constitutional + executable reference scaffold**

See SPEC.md, src/atlas.py, schemas/atlas_record.schema.json, tests/test_atlas.py, and tests/CONFORMANCE.md.
