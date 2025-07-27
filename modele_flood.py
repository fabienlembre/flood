import random
from copy import deepcopy

class Case:
    def __init__(self,l,c,couleur:int,etat:bool,matrice)->None:
        self.__l=l
        self.__c=c
        self.__coord=(self.__l,self.__c)#les coordonnées de la case
        self.__couleur=couleur#la couleur de la case sous forme d'un chiffre
        self.__etat=etat# dit si elle est en contact avec le carrée en haut ou non
        self.__dim= (matrice.nb_lig(),matrice.nb_col())
        
    #les accesseurs    
    def coordonnée(self):
        return self.__coord
    def couleur(self)->int:
        return self.__couleur
    def etat(self)->bool:
        return self.__etat
    def dimension(self)->tuple:
        return self.__dim
    
    def voisines(self)->list:
        '''renvoie une liste des coordonnées des cases voisines'''
        liste=[]
        if (self.__l)>0 : #si la case n'est pas sur le bord haut
            liste.append((self.__l-1,self.__c)) #on ajoute la case au dessus
        if (self.__c)<self.__dim[1]-1: #si la case n'est pas sur le bord droit
            liste.append((self.__l,self.__c+1)) #on ajoute la case de droite
        if (self.__l)<self.__dim[0]-1: #si la case n'est pas sur le bord bas
            liste.append((self.__l+1,self.__c)) #on ajoute la case en dessous
        if (self.__c)>0: #si la case n'est pas sur le bord gauche
            liste.append((self.__l,self.__c-1)) #on ajoute la case de gauche
        return liste
               
    def change_couleur(self,c:int):
        #met la case de la couleur c
        self.__couleur=c
        
    def change_etat(self)->None:
        if self.__etat==True:
            self.__etat=False
        else:
            self.__etat=True

class Modele:
    def __init__(self, lig=12, col=12, couleurs=6) -> None:
        '''constructeur qui prend en parametre un nbr de lignes, de colonnes et de couleurs avec des valeurs par défaut'''
        self.__lig=lig
        self.__col=col
        self.__couleurs=couleurs
        self.__score=0
        self.__mat=[[Case(j,i,(random.randint(1,couleurs)),False,self) for i in range(col)] for j in range(lig)]
        self.__depart=deepcopy(self.__mat)
        self.__pile=Pile()
    
    #accesseurs
    def nb_lig(self)-> int:
        return self.__lig
    def nb_col(self)-> int:
        return self.__col
    def nb_couleurs(self)-> int:
        return self.__couleurs
    def mat(self)-> list:
        return self.__mat
    def score(self)-> int:
        return self.__score
    def pile(self):
        return self.__pile

    
    def couleur(self,l : int,c : int) -> int:
        '''renvoie la couleur d'un carré'''
        return self.__mat[l][c].couleur()
    
    def voisines(self,l : int,c : int) -> list:
        '''renvoie liste de voisines'''
        return self.__mat[l][c].voisines()
    
    def etat(self,l : int,c : int) -> bool:
        '''renvoie etat case'''
        return self.__mat[l][c].etat()
    
    def choisit_couleur(self,l: int,c: int)-> None:
        '''Met le premier carré (0,0) à la couleur du carré de coordornées (l,c) et augmente le score
        si ce n'est pas le premier carré '''
        if self.__mat[0][0].couleur()!=self.couleur(l,c):
            self.__mat[0][0].change_couleur(self.couleur(l,c))
            self.__score+=1
            self.__pile.empiler((l,c))

    def choisit_couleur_2(self,couleur:int)-> None:
        '''POUR ETAPE 3 : Met le premier carré (0,0) à la couleur choisi (l,c) et augmente le score
        si ce n'est pas le premier carré '''
        if self.__mat[0][0].couleur()!=couleur:
            self.__mat[0][0].change_couleur(couleur)

    def change_etat_case(self,l:int,c:int):
        '''change l'état de la case (l,c)'''
        self.__mat[l][c].change_etat()
    
    def change_etat_voisines(self,l:int,c:int):
        '''Change l'état (à True) de toutes les cases des chemins partant du coin gauche de la couleur de ce coin'''
        for coord in self.voisines(l,c): #pour chaque case voisine
            if self.couleur(coord[0],coord[1])==self.couleur(l,c) and self.etat(coord[0],coord[1])==False: #verifier qu'on a pas déja changé l'état sinon boucle infini
                self.change_etat_case(coord[0],coord[1]) #changer l'état de la case voisine
                self.change_etat_voisines(coord[0],coord[1]) #changer l'état si nécessaire des voisines de la voisine
    
    def pose_couleur(self,couleur:int):
        '''Diffuse la couleur à toutes les cases en état de l'être et remet toutes les cases à False pour le tour suivant'''
        for l in range(self.__lig):
            for c in range(self.__col): #pour chaque bouton, on regarde son état
                if self.etat(l,c)==True:
                    self.__mat[l][c].change_couleur(couleur) #changer la couleur si la case est à True
                    self.__mat[l][c].change_etat() #remettre les boutons True à False pour le tour suivant


    def reinit(self) -> None:
        '''Met le score à 0 et reinitialise aléatoirement les valeurs de la matrice'''
        self.__score=0
        self.__mat=[[Case(j,i,(random.randint(1,self.__couleurs)),False,self) for i in range(self.__col)] for j in range(self.__lig)]
        self.__depart=deepcopy(self.__mat)
    
    def affiche_ligne_traits(self) -> str: 
        '''affiche une ligne de ’-’ de la bonne dimension'''
        lig="   "
        for i in range(self.__col):
            lig+="+---"
        lig+="+"
        return lig
    
    def affiche_ligne(self,ind : int):
        ''' affiche les valeurs de la ligne ind de la matrice (séparés par des traits)'''
        if ind<10:
            lig=str(ind)+" " #numéro de la ligne si c'est un chiffre 
        else :
            lig=str(ind) #numéro de la ligne si c'est un nombre 
        for i in range(self.__col):
            lig+=" | "+str(self.__mat[ind][i].couleur()) #bordure + valeur carré
        lig+=" | "
        return lig

    def __str__(self) -> str:
        '''pour afficher la matrice sous forme de tableau stylisé 
        à l’aide des 2 fonctions précédentes'''
        plateau='  '
        for i in range(self.__col): #premiere ligne avec les nums de colonnes
            if i<10:
                plateau += '   ' + str(i) #adapte l'espace pris pour un chiffre
            else:
                plateau += '  ' + str(i) #adapte l'espace pris pour un nombre
        plateau+='\n' #retour à la ligne 
        for l in range(self.__lig): #pour chaque ligne de la matrice : bordure + ligne valeurs
            plateau+=self.affiche_ligne_traits()+'\n'
            plateau+=self.affiche_ligne(l)+'\n'
        plateau+=self.affiche_ligne_traits()+'\n'
        return(plateau)
    
    def partie_fini(self)-> None:
        '''vérifie si la partie est finie cad tt les boutons de la même couleur'''
        for i in range(self.__lig):
            for j in range(self.__col):
                if self.__mat[i][j].couleur()!=self.__mat[0][0].couleur():
                    return False
        return True
    
    def nb_coups_max(self)-> int:
        liste_compteur=[float('inf')]
        for i in range(400):
            copie=deepcopy(self) #on crée la copie du Modele
            '''Pour le premier tour, on fait en sorte de prendre une couleur qui est dans les 2 cases collées du coin droit pour améliorer un peu la précision'''
            liste=[]
            copie.change_etat_voisines(0,0)
            for coord in self.voisines(0,0):
                liste.append(copie.couleur(coord[0],coord[1]))
            couleur=random.choice(liste) #choisit un element aléatoire de la liste qui contient les voisins du coin en haut à gauche
            while couleur==copie.mat()[0][0].couleur():
                if liste[0]==couleur and liste[1]==couleur: #si la couleur du coin est la même que ces voisines, on choisit une couleur aléatoire (qui sera revérifié par le while)
                    couleur=random.randint(1,copie.nb_couleurs())
                else :
                    couleur=random.choice(liste) # sinon on rechoisi aléatoirement une couleur dans la liste tant que la couleur est la même que celle du coin
            copie.choisit_couleur_2(couleur)
            copie.pose_couleur(couleur)
            mini=liste_compteur[-1]
            compteur=1 #on initialise le compteur à 1 (premier tour effectué)
            while copie.partie_fini()==False and compteur<mini:
                copie.change_etat_voisines(0,0)
                couleur=random.randint(1,copie.nb_couleurs())
                while couleur==copie.mat()[0][0].couleur():
                    couleur=random.randint(1,copie.nb_couleurs())
                copie.choisit_couleur_2(couleur)
                copie.pose_couleur(couleur)
                compteur+=1
            liste_compteur.append(compteur)
        return liste_compteur[-1]
    
    def jouer(self,l,c)->None:
        self.change_etat_voisines(0,0)
        self.choisit_couleur(l,c)
        self.pose_couleur(self.couleur(0,0))

    def undo(self)->None:
        self.__score=0
        self.__pile.depiler()
        p=Pile()
        while not self.__pile.est_vide():
            p.empiler(self.__pile.depiler())
        self.__mat=deepcopy(self.__depart)
        if __name__== "__main__":
            while not p.est_vide():
                etape=p.depiler()
                self.change_etat_voisines(0,0)
                self.choisit_couleur(etape[0],etape[1])
                self.pose_couleur(self.couleur(0,0))
        return p

class Pile:
    def __init__(self):
        self.__les_elem=[]
        
    def empiler(self,elt):
        self.__les_elem.append(elt)
        
    def est_vide(self):
        return len(self.__les_elem) ==0
    
    def sommet(self):
        assert not self.est_vide()
        return self.__les_elem[-1]
    
    def depiler(self):
        assert not self.est_vide()
        elt=self.__les_elem[-1]
        del(self.__les_elem[-1])
        return elt
    
    
'''Tests'''
if __name__== "__main__":
    mod = Modele()
    '''print(mod)
    mod.jouer(5,5)
    print(mod)
    mod.jouer(10,10)
    print(mod)
    mod.jouer(6,6)
    print(mod)
    mod.undo()
    print(mod)
    mod.jouer(7,7)
    print(mod)
    mod.undo()
    print(mod)'''
    print(mod.nb_coups_max())