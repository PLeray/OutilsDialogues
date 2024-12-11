from graphviz import Digraph

# Création du graphe hiérarchique
dot = Digraph()
dot.node("A", "Parent")
dot.node("B", "Fils 1")
dot.node("C", "Fils 2")
dot.node("D", "Petit-fils")

dot.edges([("A", "B"), ("A", "C"), ("B", "D")])

# Affichage
dot.render('arbre', format='png', view=True)
