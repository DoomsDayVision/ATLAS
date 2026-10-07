# ATLAS — Conformance / Falsification Tests

An implementation claiming ATLAS conformance must preserve these boundaries.

## Identity and indexing

1. ZiD remains persistent object identity.
2. CID remains exact-byte identity.
3. ZDS remains placement/address indexing.
4. Atlas Index ID remains a projection/index key.
5. No Atlas Index ID may silently become a ZiD.
6. Canonical system-object status requires a ZiD.

## Relationship integrity

7. Relationship edges are typed.
8. A relationship target must resolve or be explicitly represented as unresolved.
9. Predecessor, successor, source, dependency, witness, verification, seal, and authority references remain different relationship meanings.
10. Changing a view must not silently mutate the underlying object.

## Authority boundary

11. ATLAS exposes no permit operation.
12. An authorized_by edge is a reference to an authority record, not an authority grant.
13. ATLAS may not promote REFERENCE_ONLY into AUTHORIZED.
14. Presence in ATLAS must not imply ACTIVE, CURRENT, VERIFIED, DEPLOYED, or AUTHORIZED.

## Evidence boundary

15. A CID or hash does not prove truth.
16. A seal reference does not prove truth.
17. A verification reference does not prove deployment.
18. A receipt reference does not prove the referenced effect actually occurred unless the appropriate witness/evidence relation exists.
19. Missing evidence remains UNKNOWN or absent.

## Navigation

20. Lineage traversal must preserve edge direction and type.
21. Traversal must not invent a missing predecessor or successor.
22. Cycles must not cause infinite traversal.
23. Export must be deterministic for unchanged graph state.

## Core invariant

\[
\boxed{
\text{ATLAS maps what is related}
\neq
\text{ATLAS decides what is permitted}
}
\]

and

\[
\boxed{
\text{Atlas Index feeds ATLAS}
\neq
\text{Atlas Index is ATLAS}.
}
\]
