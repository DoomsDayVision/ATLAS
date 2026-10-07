# ATLAS — Formal Specification

## 1. Graph model

ATLAS is a typed directed multigraph

\[
\mathcal A=(V,E,\tau_V,\tau_E,\rho).
\]

Where:

- \(V\) is the set of referenced objects;
- \(E\subseteq V\times V\times K\) is the set of typed relationships;
- \(\tau_V\) assigns object classes;
- \(\tau_E\) assigns relationship classes;
- \(\rho\) stores external references such as ZiD, CID, ZDS, authority, witness, verification, seal, and package references.

ATLAS records relationships among externally identified facts. It does not mint those external facts.

## 2. Identity separation

For an Atlas node \(v\),

\[
v=
(z,c,d,a,\ell,s,r)
\]

may reference:

- \(z\): ZiD;
- \(c\): CID;
- \(d\): ZDS placement;
- \(a\): Atlas Index ID;
- \(\ell\): lifecycle / claim state;
- \(s\): source and provenance references;
- \(r\): relationships.

These identifiers are not interchangeable.

\[
\boxed{
\mathrm{ZiD}\neq\mathrm{CID}\neq\mathrm{ZDS}\neq\mathrm{AtlasIndexID}
}
\]

## 3. Canonical-node rule

A canonical system-object node requires a non-empty ZiD.

An observation or external claim may be represented without pretending it has become a canonical system object, but its status must identify that distinction.

Presence in ATLAS does not make an object canonical, active, verified, or authorized.

## 4. Atlas Index ID

For path-addressed projections, define

\[
k=\operatorname{normalize}(path)
\]

and

\[
\boxed{
\operatorname{AtlasIndexID}(k)
=
\text{ZIDX-PATH-}
+
\operatorname{HEX}_{16}(\operatorname{SHA256}(k))
}
\]

where the first sixteen hexadecimal characters are upper-case.

This ID belongs to the indexing projection. It is not persistent object identity.

## 5. Relationship types

The reference vocabulary includes:

\[
\begin{aligned}
&\text{depends\_on},\\
&\text{derived\_from},\\
&\text{supersedes},\\
&\text{previous\_version},\\
&\text{source\_of},\\
&\text{indexed\_with},\\
&\text{placed\_by},\\
&\text{authorized\_by},\\
&\text{witnessed\_by},\\
&\text{verified\_by},\\
&\text{sealed\_by},\\
&\text{packaged\_by},\\
&\text{conflicts\_with},\\
&\text{supports},\\
&\text{annotates}.
\end{aligned}
\]

Relationship names describe edges. They do not transfer powers.

For example,

\[
A\xrightarrow{\text{authorized\_by}}R
\]

means ATLAS records an authorization reference to \(R\). It does not mean ATLAS performed authorization.

## 6. Non-collapse laws

ATLAS preserves:

\[
\boxed{\text{path}\neq\text{identity}}
\]

\[
\boxed{\text{hash}\neq\text{truth}}
\]

\[
\boxed{\text{relationship}\neq\text{authority}}
\]

\[
\boxed{\text{authorization reference}\neq\text{execution}}
\]

\[
\boxed{\text{verification reference}\neq\text{deployment}}
\]

\[
\boxed{\text{seal reference}\neq\text{runtime permission}}
\]

\[
\boxed{\text{current state}\neq\text{genealogy}}
\]

## 7. Reconstructable navigation

Given any node \(v\), ATLAS should permit traversal toward applicable answers for:

- What is this?
- Where is it placed?
- What exact bytes are referenced?
- What is its predecessor?
- What superseded it?
- What does it depend on?
- What source produced it?
- What authorization record applies?
- What witnessed it?
- What independently verified it?
- What sealed it?
- What package preserved it?

ATLAS answers by following typed references.

It must not fabricate a missing reference.

## 8. Internal and external views

ATLAS supports projections

\[
\pi_i:\mathcal A\to\mathcal V_i
\]

for different views.

A projection may hide or emphasize relationships, but must not mutate the underlying object merely because the view changed.

\[
\boxed{
v_{\text{internal}}
\equiv
v_{\text{external}}
}
\]

when both views refer to the same underlying identified object.

## 9. Evidence return

A completed evidence path may append new references into ATLAS:

\[
\text{Effect}
\rightarrow
\text{Receipt}
\rightarrow
\text{Witness}
\rightarrow
\text{DVWM}^3
\rightarrow
\text{RAIN}
\rightarrow
\text{Z267}
\rightarrow
\text{CHAD}
\rightarrow
\text{ATLAS update}.
\]

The ATLAS update records the relationships. It does not retroactively create the evidence.

## 10. Authority boundary

ATLAS has no permit operation.

\[
\boxed{
\operatorname{Authorize}\notin\operatorname{Capabilities}(\mathrm{ATLAS})
}
\]

The strongest authority statement ATLAS may make is a reference statement:

\[
\text{node}\xrightarrow{\text{authorized\_by}}\text{authority record}.
\]

The validity and current applicability of that authority remain external to ATLAS.

## 11. Unknown preservation

Missing information remains missing.

ATLAS must never infer:

- VERIFIED from a hash;
- AUTHORIZED from a relationship name;
- CURRENT from presence;
- ACTIVE from indexing;
- TRUTH from a seal;
- SUCCESSOR from naming similarity.

UNKNOWN remains a valid state.
