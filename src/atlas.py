"""ATLAS v0.1 reference kernel.

Relationship and navigation graph only.
No authorization, execution, verification, signing, or sealing capability.
"""

from __future__ import annotations

from dataclasses import dataclass, field, asdict
from hashlib import sha256
import json
from typing import Dict, Iterable, List, Optional, Set, Tuple


RELATION_TYPES = frozenset({
    "depends_on",
    "derived_from",
    "supersedes",
    "previous_version",
    "source_of",
    "indexed_with",
    "placed_by",
    "authorized_by",
    "witnessed_by",
    "verified_by",
    "sealed_by",
    "packaged_by",
    "conflicts_with",
    "supports",
    "annotates",
})

CANONICAL_STATUSES = frozenset({
    "CURRENT",
    "HISTORICAL",
    "SUPERSEDED",
})

ALL_STATUSES = CANONICAL_STATUSES | frozenset({
    "EXPERIMENTAL",
    "PROPOSAL",
    "EVIDENCE",
    "QUARANTINED",
    "HOLD",
    "UNKNOWN",
})

AUTHORITY_STATUSES = frozenset({
    "REFERENCE_ONLY",
    "NONE",
    "UNKNOWN",
})


def normalize_path(path: str) -> str:
    if not isinstance(path, str) or not path.strip():
        raise ValueError("path must be a non-empty string")
    normalized = path.strip().replace("/", "\\")
    while "\\\\" in normalized:
        normalized = normalized.replace("\\\\", "\\")
    return normalized.lower()


def atlas_path_index_id(path: str) -> str:
    key = normalize_path(path)
    digest = sha256(key.encode("utf-8")).hexdigest()[:16].upper()
    return "ZIDX-PATH-" + digest


def atlas_node_index_id(node_id: str) -> str:
    if not isinstance(node_id, str) or not node_id.strip():
        raise ValueError("node_id must be a non-empty string")
    key = node_id.strip()
    digest = sha256(key.encode("utf-8")).hexdigest()[:16].upper()
    return "ZIDX-NODE-" + digest


@dataclass(frozen=True)
class Edge:
    kind: str
    target: str
    evidence_ref: Optional[str] = None

    def __post_init__(self):
        if self.kind not in RELATION_TYPES:
            raise ValueError("unknown relationship type: " + self.kind)
        if not self.target:
            raise ValueError("edge target is required")


@dataclass
class Node:
    node_id: str
    object_class: str
    status: str = "UNKNOWN"
    atlas_index_id: Optional[str] = None
    zid: Optional[str] = None
    cid: Optional[str] = None
    zds_id: Optional[str] = None
    root_id: Optional[str] = None
    zerone_coordinate: Optional[str] = None
    path: Optional[str] = None
    path_key: Optional[str] = None
    authority_status: str = "REFERENCE_ONLY"
    claim_state: Optional[str] = None
    provenance_refs: List[str] = field(default_factory=list)
    relations: List[Edge] = field(default_factory=list)

    def __post_init__(self):
        if not self.node_id:
            raise ValueError("node_id is required")
        if not self.object_class:
            raise ValueError("object_class is required")
        if self.status not in ALL_STATUSES:
            raise ValueError("invalid status: " + self.status)
        if self.authority_status not in AUTHORITY_STATUSES:
            raise ValueError("ATLAS cannot carry an authority-granting status")
        if self.status in CANONICAL_STATUSES and not self.zid:
            raise ValueError("canonical system-object status requires ZiD")

        if self.path is not None:
            self.path_key = normalize_path(self.path)
            expected = atlas_path_index_id(self.path)
            if self.atlas_index_id is None:
                self.atlas_index_id = expected
            elif self.atlas_index_id != expected:
                raise ValueError("atlas_index_id does not match normalized path")
        elif self.atlas_index_id is None:
            self.atlas_index_id = atlas_node_index_id(self.node_id)

    def add_relation(self, kind: str, target: str, evidence_ref: Optional[str] = None):
        edge = Edge(kind=kind, target=target, evidence_ref=evidence_ref)
        if edge not in self.relations:
            self.relations.append(edge)


class Atlas:
    def __init__(self):
        self._nodes: Dict[str, Node] = {}

    def add_node(self, node: Node):
        if node.node_id in self._nodes:
            raise ValueError("duplicate node_id: " + node.node_id)
        self._nodes[node.node_id] = node

    def get(self, node_id: str) -> Node:
        return self._nodes[node_id]

    def add_relation(
        self,
        source: str,
        kind: str,
        target: str,
        evidence_ref: Optional[str] = None,
    ):
        if source not in self._nodes:
            raise KeyError("unknown source node: " + source)
        if target not in self._nodes:
            raise KeyError("unknown target node: " + target)
        self._nodes[source].add_relation(kind, target, evidence_ref)

    def neighbors(
        self,
        node_id: str,
        kinds: Optional[Iterable[str]] = None,
    ) -> Tuple[str, ...]:
        node = self.get(node_id)
        allowed = None if kinds is None else set(kinds)
        out = []
        for edge in node.relations:
            if allowed is None or edge.kind in allowed:
                out.append(edge.target)
        return tuple(out)

    def traverse(
        self,
        start: str,
        kinds: Optional[Iterable[str]] = None,
        max_depth: int = 16,
    ) -> Tuple[str, ...]:
        if max_depth < 0:
            raise ValueError("max_depth must be non-negative")
        if start not in self._nodes:
            raise KeyError("unknown start node: " + start)

        allowed = None if kinds is None else set(kinds)
        seen: Set[str] = {start}
        queue: List[Tuple[str, int]] = [(start, 0)]
        order: List[str] = []

        while queue:
            current, depth = queue.pop(0)
            order.append(current)
            if depth >= max_depth:
                continue
            for edge in self._nodes[current].relations:
                if allowed is not None and edge.kind not in allowed:
                    continue
                if edge.target not in seen:
                    seen.add(edge.target)
                    queue.append((edge.target, depth + 1))

        return tuple(order)

    def lineage(self, node_id: str) -> Tuple[str, ...]:
        lineage_kinds = {
            "previous_version",
            "derived_from",
            "supersedes",
            "source_of",
        }
        return self.traverse(node_id, kinds=lineage_kinds)

    def validate(self) -> Tuple[str, ...]:
        errors = []
        index_ids = {}

        for node_id, node in self._nodes.items():
            if node.atlas_index_id in index_ids:
                errors.append(
                    "duplicate atlas_index_id: "
                    + str(node.atlas_index_id)
                    + " on "
                    + index_ids[node.atlas_index_id]
                    + " and "
                    + node_id
                )
            index_ids[node.atlas_index_id] = node_id

            for edge in node.relations:
                if edge.target not in self._nodes:
                    errors.append(
                        "dangling edge "
                        + node_id
                        + " --"
                        + edge.kind
                        + "--> "
                        + edge.target
                    )

        return tuple(errors)

    def export(self) -> str:
        records = []
        for node_id in sorted(self._nodes):
            node = self._nodes[node_id]
            record = asdict(node)
            record["relations"] = [
                asdict(edge)
                for edge in sorted(
                    node.relations,
                    key=lambda e: (e.kind, e.target, e.evidence_ref or ""),
                )
            ]
            records.append(record)

        return json.dumps(
            {"schema": "ATLAS_GRAPH_V0_1", "nodes": records},
            indent=2,
            sort_keys=True,
        )


def self_check():
    atlas = Atlas()

    a = Node(
        node_id="artifact:v1",
        object_class="artifact",
        status="HISTORICAL",
        zid="ZID:EXAMPLE:ARTIFACT:1:v1",
        cid="sha256:aaa",
        path="C:\\ZERONE\\example\\artifact-v1.bin",
    )
    b = Node(
        node_id="artifact:v2",
        object_class="artifact",
        status="CURRENT",
        zid="ZID:EXAMPLE:ARTIFACT:1:v2",
        cid="sha256:bbb",
        path="C:/ZERONE/example/artifact-v2.bin",
    )
    auth = Node(
        node_id="authority:receipt",
        object_class="authority-reference",
        status="EVIDENCE",
        authority_status="REFERENCE_ONLY",
    )

    atlas.add_node(a)
    atlas.add_node(b)
    atlas.add_node(auth)

    atlas.add_relation("artifact:v2", "previous_version", "artifact:v1")
    atlas.add_relation(
        "artifact:v2",
        "authorized_by",
        "authority:receipt",
        evidence_ref="receipt:example",
    )

    assert atlas.lineage("artifact:v2") == ("artifact:v2", "artifact:v1")
    assert atlas.neighbors("artifact:v2", {"authorized_by"}) == ("authority:receipt",)
    assert atlas.validate() == ()
    assert "ATLAS_GRAPH_V0_1" in atlas.export()

    return True


if __name__ == "__main__":
    self_check()
    print("ATLAS_REFERENCE_PASS")
