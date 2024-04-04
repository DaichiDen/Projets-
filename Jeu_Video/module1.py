# Créé par zapoid, le 14/03/2024 en Python 3.7
class Sommet:
    def __init__(self,nom):
        self.nom=nom
        self.visite=False
A=Sommet('A')
B=Sommet('B')
C=Sommet('C')
D=Sommet('D')
class Arete:
    def __init__(self,s1,s2,poids=1):
       self.s1=s1
       self.s2=s2
       self.poids=poids
A1=Arete(A,B)
A2=Arete(B,C)
A3=Arete(C,D)
A4=Arete(D,A)

class Graph:
    def __init__(self):
        self.lsommet=[]
        self.larete=[]
        self.m_a=[]
        self.l_j={}
    def ajouter_s(self,s):
        self.lsommet.append(s)

    def aj_a(self,s1,s2,poids=1):
        self.larete.append(Arete(s1,s2,poids))

    def matrice(self):
        n=len(self.lsommet)
        m=[[0]*n for i in range(n)]
        for arete in self.larete:
            s1=arete.s1
            s2=arete.s2
            pos_s1=self.lsommet.index(s1)
            pos_s2=self.lsommet.index(s2)
            m[pos_s1][pos_s2]=arete.poids
            m[pos_s2][pos_s1]=arete.poids
        self.m_a=m
    def liste_adj(self):
        dic={}
        for i in self.lsommet:






graph=Graph()
print(graph.lsommet)
graph.ajouter_s(A)
graph.ajouter_s(B)
graph.ajouter_s(C)
graph.ajouter_s(D)
print(graph.lsommet)
print(graph.larete)
graph.aj_a(A,B)
print(graph.larete)

graph.matrice()
print(graph.m_a)





