import modele_flood
import vue_flood

class FloodControleur:
    def __init__(self) -> None:
        self.__modele = modele_flood.Modele()#on crée un modele
        self.__vue= vue_flood.Vue(self.__modele,self)#on crée une vue

    def creer_controleur_bouton(self,lig,col)-> None:
        ''' crée le controleur qui redessine la grille qd on appuie sur le bouton (l,c)'''
        def controleur_btn():
            self.__vue.redessine(lig,col)#appel à la méthode redessine pour le bouton aux coordonnées (l,c)
        return controleur_btn
    
    def nouvelle_partie(self)->None:
        ''' cree le controleur qui reinitialise dans modèle et dans vue le score et les couleurs '''
        def controleur_btn():
            self.__modele.reinit()
            self.__vue.reinit()
        return controleur_btn

    def reinit_partielle(self)->None:
        ''' cree le controleur qui reinitialise partiellemnet dans modèle et dans vue '''
        def controleur_btn():
            self.__modele.reinit_partielle()
            self.__vue.reinit_partielle()
        return controleur_btn

    def demarre(self)->None:
        self.__vue.demarre()