import json
import unittest

from src.atlas import (
    Atlas,
    Edge,
    Node,
    atlas_node_index_id,
    atlas_path_index_id,
    normalize_path,
)


class AtlasTests(unittest.TestCase):
    def test_path_normalization_is_deterministic(self):
        a = "C:\\ZERONE\\2.0_BODY\\item"
        b = "c:/zerone/2.0_body/item"
        self.assertEqual(normalize_path(a), normalize_path(b))
        self.assertEqual(atlas_path_index_id(a), atlas_path_index_id(b))

    def test_node_id_index_is_deterministic(self):
        self.assertEqual(
            atlas_node_index_id("node:1"),
            atlas_node_index_id("node:1"),
        )
        self.assertNotEqual(
            atlas_node_index_id("node:1"),
            atlas_node_index_id("node:2"),
        )

    def test_canonical_status_requires_zid(self):
        with self.assertRaises(ValueError):
            Node(
                node_id="bad",
                object_class="artifact",
                status="CURRENT",
            )

    def test_atlas_cannot_claim_granting_authority(self):
        with self.assertRaises(ValueError):
            Node(
                node_id="bad-auth",
                object_class="artifact",
                status="EVIDENCE",
                authority_status="AUTHORIZED",
            )

    def test_relationship_vocabulary(self):
        with self.assertRaises(ValueError):
            Edge(kind="magic_authority", target="x")

    def test_graph_navigation(self):
        atlas = Atlas()
        for node_id in ("a", "b", "c"):
            atlas.add_node(
                Node(
                    node_id=node_id,
                    object_class="example",
                    status="EVIDENCE",
                )
            )
        atlas.add_relation("a", "derived_from", "b")
        atlas.add_relation("b", "derived_from", "c")

        self.assertEqual(atlas.traverse("a"), ("a", "b", "c"))
        self.assertEqual(atlas.lineage("a"), ("a", "b", "c"))

    def test_authorized_by_is_reference_only(self):
        atlas = Atlas()
        atlas.add_node(
            Node(
                node_id="action",
                object_class="effect",
                status="EVIDENCE",
            )
        )
        atlas.add_node(
            Node(
                node_id="permit",
                object_class="authority-reference",
                status="EVIDENCE",
                authority_status="REFERENCE_ONLY",
            )
        )
        atlas.add_relation(
            "action",
            "authorized_by",
            "permit",
            evidence_ref="receipt:permit",
        )

        self.assertEqual(
            atlas.neighbors("action", {"authorized_by"}),
            ("permit",),
        )
        self.assertEqual(atlas.get("permit").authority_status, "REFERENCE_ONLY")

    def test_dangling_edges_are_rejected_at_insert(self):
        atlas = Atlas()
        atlas.add_node(
            Node(
                node_id="a",
                object_class="example",
                status="EVIDENCE",
            )
        )
        with self.assertRaises(KeyError):
            atlas.add_relation("a", "depends_on", "missing")

    def test_export_is_stable_json(self):
        atlas = Atlas()
        atlas.add_node(
            Node(
                node_id="b",
                object_class="example",
                status="EVIDENCE",
            )
        )
        atlas.add_node(
            Node(
                node_id="a",
                object_class="example",
                status="EVIDENCE",
            )
        )

        exported = atlas.export()
        parsed = json.loads(exported)
        self.assertEqual(parsed["schema"], "ATLAS_GRAPH_V0_1")
        self.assertEqual(
            [n["node_id"] for n in parsed["nodes"]],
            ["a", "b"],
        )


if __name__ == "__main__":
    unittest.main()
