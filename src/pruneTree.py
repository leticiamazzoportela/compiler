from anytree import Node, RenderTree, AsciiStyle, PreOrderIter, PostOrderIter
from anytree.exporter import DotExporter

def prune(tree):
    for node in PostOrderIter(tree):
        node_name = node.name.split('.') #comeca com id
        no = node.parent

        if (node_name[1] == ':' or node_name[1] == ',' or node_name[1] == '(' or
            node_name[1] == ')' or node_name[1] == '[' or node_name[1] == ']' or
            node_name[1] == ':='):
            node.parent = None
    
    for node in PostOrderIter(tree):
        node_name = node.name.split('.') #comeca com id
        no = node.parent

        if node.parent != None:
            father = node.parent.name.split('.')

            if node_name[1] == father[1]:
                node.parent = no.parent
                if len(no.children) > 0:
                    no.children[0].parent = node
                no.parent = None           

    showPruneTree(tree)

def showPruneTree(tree):
    DotExporter(tree).to_picture("pruneAst.png")