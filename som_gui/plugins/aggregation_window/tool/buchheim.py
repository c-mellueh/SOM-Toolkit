from __future__ import annotations
from typing import TYPE_CHECKING
from PySide6.QtCore import QPointF
import som_gui

if TYPE_CHECKING:
    from som_gui.plugins.aggregation_window.module.node import ui as node_ui
    from som_gui.plugins.aggregation_window.module.buchheim.prop import (
        BuchheimProperties,
    )
from som_gui.plugins.aggregation_window import tool as aw_tool

X_MARGIN = 20
Y_MARGIN = 40

class Buchheim:
    @classmethod
    def get_properties(cls) -> BuchheimProperties:
        return som_gui.BuchheimProperties

    @classmethod
    def intialize(cls, v: node_ui.NodeProxy, depth=0, number: int = 1):
        v.thread = None
        v._lmost_sibling = None
        v.mod = 0
        v.change= 0
        v.shift = 0
        v.ancestor = v
        v.number = None
        cls.get_properties().position_dict[v] = [-1.0, depth]
        v.number = number
        for index, w in enumerate(cls.children(v)):
            cls.intialize(w, depth + 1, index + 1)

    @classmethod
    def buchheim(cls, v: node_ui.NodeProxy):
        tree = cls.firstwalk(v)
        cls.second_walk(tree)
        return tree


    @classmethod
    def firstwalk(cls, v: node_ui.NodeProxy,distance = 300.):
        if len(cls.children(v)) == 0: #no children exist
            if cls.get_lmost_sibling(v): #if sibling exist move next to sibling with X_MARGIN
                lbrother = cls.lbrother(v)
                cls.set_x(v, cls.x(lbrother) + cls.wid)
            else:
                cls.set_x(v, 0.0)

        else:
            default_ancestor = cls.children(v)[0]#elektrotechnik
            for w in cls.children(v):
                cls.firstwalk(w)
                default_ancestor = cls.apportion(w, default_ancestor, distance)
            cls.execute_shifts(v)
            c1  = cls.x(cls.children(v)[0])
            c2 = cls.x(cls.children(v)[-1])
            midpoint = ( c1+ c2) / 2

            w = cls.lbrother(v)
            if w:
                cls.set_x(v, cls.x(w) + distance)
                v.mod = cls.x(v) - midpoint
            else:
                cls.set_x(v, midpoint)
        return v

    @classmethod
    def second_walk(cls, v: node_ui.NodeProxy, m=0, depth=0):
        if v.aggregation.object.name == "Manometer":
            print("HIER")
        cls.set_x(v, cls.x(v) + m)
        cls.set_y(v, depth)
        for w in cls.children(v):
            cls.second_walk(w, m + v.mod, depth + 1)

    @classmethod
    def apportion(
        cls, v: node_ui.NodeProxy, default_ancestor: node_ui.NodeProxy, distance: float
    ):
        w = cls.lbrother(v)
        if w is None:
            return default_ancestor
        # in buchheim notation:
        # i == inner; o == outer; r == right; l == left; r = +; l = -
        vir = vor = v
        vil = w
        vol = cls.get_lmost_sibling(v)
        sir = sor = v.mod
        sil = vil.mod
        sol = vol.mod
        while cls.right(vil) and cls.left(vir):
            vil = cls.right(vil)
            vir = cls.left(vir)
            vol = cls.left(vol)
            vor = cls.right(vor)
            vor.ancestor = v
            shift = cls.x(vil) + sil - (cls.x(vir) + sir) + distance
            if shift > 0:
                cls.move_subtree(cls.ancestor(vil, v, default_ancestor), v, shift)
                sir = sir + shift
                sor = sor + shift
            sil += vil.mod
            sir += vir.mod
            sol += vol.mod
            sor += vor.mod
        if cls.right(vil) and not cls.right(vor):
            vor.thread = cls.right(vil)
            vor.mod += sil - sor
        if cls.left(vir) and not cls.left(vol):
            vol.thread = cls.left(vir)
            vol.mod += sir - sol
            default_ancestor = v
        return default_ancestor

    @classmethod
    def execute_shifts(cls, v: node_ui.NodeProxy):
        return
        shift = change = 0
        for w in reversed(cls.children(v)):
            cls.set_x(w, cls.x(w) + shift)
            w.mod += shift
            change += w.change
            shift += w.shift + change

    @classmethod
    def move_subtree(cls, wl: node_ui.NodeProxy, wr: node_ui.NodeProxy, shift: float):
        subtrees = wr.number - wl.number
        wr.change -= shift / subtrees
        wr.shift += shift
        wl.change += shift / subtrees
        cls.set_x(wr, cls.x(wr) + shift)
        wr.mod += shift

    @classmethod
    def ancestor(
        cls,
        vil: node_ui.NodeProxy,
        v: node_ui.NodeProxy,
        default_ancestor: node_ui.NodeProxy,
    ):
        if vil.ancestor in cls.children(v):
            return vil.ancestor
        else:
            return default_ancestor

    # NodeProxy getter functions

    @classmethod
    def children(cls, v: node_ui.NodeProxy) -> list[node_ui.NodeProxy]:
        return sorted(aw_tool.Node.get_child_nodes(v), key=lambda n: n.x())

    @classmethod
    def parent(cls, v: node_ui.NodeProxy) -> node_ui.NodeProxy:
        return aw_tool.Node.get_parent_node(v)

    @classmethod
    def left(cls, v: node_ui.NodeProxy):
        return v.thread or len(cls.children(v)) and cls.children(v)[0]

    @classmethod
    def right(cls, v: node_ui.NodeProxy):
        return v.thread or len(cls.children(v)) and cls.children(v)[-1]

    @classmethod
    def lbrother(cls, v: node_ui.NodeProxy):
        n = None
        parent = cls.parent(v)
        if parent:
            for node in cls.children(parent):
                if node == v:
                    return n
                else:
                    n = node
        return n

    @classmethod
    def get_lmost_sibling(cls, v: node_ui.NodeProxy) -> node_ui.NodeProxy:
        if (
            not v._lmost_sibling
            and cls.parent(v)
            and v != cls.children(cls.parent(v))[0]
        ):
            v._lmost_sibling = cls.children(cls.parent(v))[0]
        return v._lmost_sibling

    @classmethod
    def x(cls, v: node_ui.NodeProxy):
        return cls.get_properties().position_dict[v][0]

    @classmethod
    def y(cls, v: node_ui.NodeProxy):
        return cls.get_properties().position_dict[v][1]

    @classmethod
    def set_x(cls, v: node_ui.NodeProxy, x: float):
        cls.get_properties().position_dict[v][0] = x

    @classmethod
    def set_y(cls, v: node_ui.NodeProxy, y: float):
        cls.get_properties().position_dict[v][1] = y

    @classmethod
    def pos(cls, v: node_ui.NodeProxy):
        return cls.get_properties().position_dict[v]

    @classmethod
    def width(cls, v: node_ui.NodeProxy):
        return v.geometry().width()

    @classmethod
    def height(cls, v: node_ui.NodeProxy):
        return aw_tool.Node.get_frame_geometry(v).height()
