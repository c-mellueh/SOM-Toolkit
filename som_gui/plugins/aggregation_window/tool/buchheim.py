from __future__ import annotations
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from som_gui.plugins.aggregation_window.module.node import ui as node_ui

from som_gui.plugins.aggregation_window import tool as aw_tool
class Buchheim:

    @classmethod
    def buchheim(cls,v:node_ui.NodeProxy):
        tree = cls.firstwalk(v)
        cls.second_walk(tree)
        return tree
    
    @classmethod
    def firstwalk(cls,v:node_ui.NodeProxy):
        pass
    
    @classmethod
    def second_walk(cls,):
        pass




    #NodeProxy getter functions

    @classmethod
    def children(v:node_ui.NodeProxy)-> list[node_ui.NodeProxy]:
        return aw_tool.Node.get_child_nodes(v)

    @classmethod
    def parent(v:node_ui.NodeProxy)-> node_ui.NodeProxy:
        return aw_tool.Node.get_parent_node(v)
    
    @classmethod
    def left(cls, v:node_ui.NodeProxy):
        return cls.thread(v) or len(cls.children(v)) and cls.children(v)[0]

    @classmethod
    def right(cls, v:node_ui.NodeProxy):
        children = aw_tool.Node.get_child_nodes(v)
        return cls.thread(v) or len(cls.children(v)) and cls.children(v)[-1]

    @classmethod
    def thread(cls, v:node_ui.NodeProxy):
        return v.thread
    
    @classmethod
    def lbrother(cls, v:node_ui.NodeProxy):
        n = None
        parent = cls.parent(v)
        if parent:
            for node in cls.children(parent):
                if node == v: return n
                else:            n = node
        return n
    
    @classmethod
    def get_lmost_sibling(cls, v:node_ui.NodeProxy) -> node_ui.NodeProxy:
        if not v._lmost_sibling and cls.parent(v) and v != cls.children(cls.parent(v))[0]:
            v._lmost_sibling = cls.children(cls.parent(v))[0]
        return v._lmost_sibling