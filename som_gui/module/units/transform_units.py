import json
from dataclasses import dataclass, field
from functools import lru_cache
from typing import Dict, List, Optional
from rdflib import Graph, Namespace, URIRef, Literal
from rdflib.namespace import RDF, SKOS as _SKOS
import tqdm
QUDT = Namespace("http://qudt.org/schema/qudt/")
SKOS = _SKOS  # http://www.w3.org/2004/02/skos/core#
GRAPH = Graph()
GRAPH.parse(r".\QUDT-all-in-one-OWL.ttl")
# ---------- Helpers ----------

@lru_cache(maxsize=4096)
def load_graph(uri: str) -> Graph:
    """Load a QUDT resource (unit or quantitykind) as JSON-LD into an rdflib Graph."""
    return GRAPH

def localname(uri: str) -> str:
    return uri.rstrip("/").split("/")[-1]

def get_pref_label(uri: str) -> Optional[str]:
    print(uri)
    g = load_graph(uri)
    ref = URIRef(uri)
    label = next(g.objects(ref, SKOS.prefLabel), None)
    if isinstance(label, Literal):
        return str(label)
    # fallback: try rdfs:label
    from rdflib.namespace import RDFS
    if label is None:
        return None
    label = [x for x in label if x[2].language == "en"][2]
    return str(label) if isinstance(label, Literal) else None

def get_quantity_kind_uri(unit_uri: str) -> Optional[str]:
    if not unit_uri:
        return None
    g = load_graph(unit_uri)
    uref = URIRef(unit_uri)

    for _, _, qk in g.triples((uref, QUDT.hasQuantityKind, None)):
        return str(qk)
    for _, _, qk in g.triples((uref, QUDT.quantityKind, None)):
        return str(qk)

    # Fallback: Unit node by rdf:type if @id differs
    unit_type = URIRef("http://qudt.org/schema/qudt/Unit")
    for subj in g.subjects(RDF.type, unit_type):
        for _, _, qk in g.triples((subj, QUDT.hasQuantityKind, None)):
            return str(qk)
        for _, _, qk in g.triples((subj, QUDT.quantityKind, None)):
            return str(qk)
    return None

def get_broader(qk_uri: str) -> List[str]:
    """Return zero or more broader QK URIs."""
    g = load_graph(qk_uri)
    qkref = URIRef(qk_uri)
    return [str(b) for b in g.objects(qkref, SKOS.broader)]

def climb_chain(qk_uri: str) -> List[str]:
    """
    Return a chain [qk, parent, parent2, ...] following the first available broader each step,
    stopping on cycles or when broader is absent. If multiple 'broader' exist, we follow each
    in parallel and merge later (tree can have multiple parents → we create forest of roots).
    """
    # Here we capture ALL broader links to build a tree (not just a single chain).
    # We'll return a list of edges for later linking.
    stack = [qk_uri]
    visited = set()
    chain = set()  # collect all QKs encountered
    edges = []     # (child, parent)

    while stack:
        cur = stack.pop()
        if cur in visited:
            continue
        visited.add(cur)
        chain.add(cur)
        parents = get_broader(cur)
        for p in parents:
            edges.append((cur, p))
            if p not in visited:
                stack.append(p)
    # return as list, but also the edges for tree building
    return list(chain), edges

# ---------- Tree model ----------

@dataclass
class TreeNode:
    id: str
    name: str
    label: Optional[str] = None
    units: List[dict] = field(default_factory=list)
    children: Dict[str, "TreeNode"] = field(default_factory=dict)
    parents: set = field(default_factory=set)  # track parents to find roots later

    def to_dict(self) -> dict:
        # Sort children by label/name
        sorted_children = sorted(self.children.values(), key=lambda n: (n.label or n.name or "").lower())
        return {
            "id": self.id,
            "name": self.name,
            "label": self.label,
            "units": self.units,  # units attached at this QK
            "children": [c.to_dict() for c in sorted_children],
        }

# ---------- Build tree from units ----------

def build_qk_forest(units: List[dict]) -> List[dict]:
    nodes: Dict[str, TreeNode] = {}
    edges_all: List[tuple] = []

    def ensure_node(uri: str) -> TreeNode:
        if uri not in nodes:
            nodes[uri] = TreeNode(
                id=uri,
                name=localname(uri),
                label=get_pref_label(uri) or localname(uri),
            )
        return nodes[uri]

    # 1) For each unit, resolve QK and build broader graph
    for u in tqdm.tqdm(units):
        qk_uri = get_quantity_kind_uri(u.get("QudtUri", ""))
        if not qk_uri:
            print(f"Skipping unit {u.get('Code', 'unknown')} without QK URI")
            # Put unmapped units under a synthetic node if desired; here we skip.
            continue

        # ensure leaf node exists and attach unit there
        leaf = ensure_node(qk_uri)
        leaf.units.append(u)

        # walk broader graph (can branch)
        chain_nodes, edges = climb_chain(qk_uri)
        edges_all.extend(edges)
        for uri in chain_nodes:
            ensure_node(uri)

    # 2) Link edges child→parent
    for child_uri, parent_uri in edges_all:
        child = nodes[child_uri]
        parent = nodes[parent_uri]
        parent.children.setdefault(child_uri, child)
        child.parents.add(parent_uri)

    # 3) Find roots (nodes with no parents but that are in the component)
    roots = [n for n in nodes.values() if not n.parents]

    # 4) Serialize forest
    forest = [r.to_dict() for r in sorted(roots, key=lambda n: (n.label or n.name or "").lower())]
    return forest

# ---------- Main ----------

def get_multiplier(unit:dict):
    if not "QudtUri" in unit:
        return 0.
    uri = URIRef(unit["QudtUri"])
    cv = URIRef("http://qudt.org/schema/qudt/conversionMultiplier")
    triples = list(GRAPH.triples((uri, cv,None)))
    if len(triples) == 0:
        return 0.
    try:
        val = float(triples[0][2])
    except:
        val =  0.
    return val

def sort_by_multiplier(data_dict):
    for element in data_dict:
        if element.get("units"):
            element["units"].sort(key=get_multiplier, reverse=True)
        sort_by_multiplier(element["children"])

if __name__ == "__main__":
    INPUT = r"..\..\..\SOMcreator\templates\units_bsdd.json"         # your input units (list of dicts with QudtUri)
    OUTPUT = r"..\..\resources\data\units_internal.json"

    with open(INPUT, "r", encoding="utf-8") as f:
        units = json.load(f)

    for unit in units:
        unit["is_active"]=True
    forest = build_qk_forest(units)
    sort_by_multiplier(forest)
    with open(OUTPUT, "w", encoding="utf-8") as f:
        json.dump(forest, f, indent=2, ensure_ascii=True)

    print(f"Saved: {OUTPUT}")
