from anytree import Node, RenderTree, AsciiStyle, PreOrderIter, PostOrderIter
from anytree.exporter import DotExporter

def prune(tree):
    for node in PostOrderIter(tree):
        node_name = node.name.split(".") #comeca com id

        if (node_name[1] == ':' or node_name[1] == ',' or node_name[1] == '(' or
            node_name[1] == ')' or node_name[1] == '[' or node_name[1] == ']' or
            node_name[1] == ':='):
            node.parent = None
    
    showPruneTree(tree)

def showPruneTree(tree):
    DotExporter(tree).to_picture("pruneAst.png")

# TODO Terminar de podar a árvore