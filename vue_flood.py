import tkinter
import modele_flood as modele
import ctrl_flood as controleur

class Vue:
    def __init__(self, modele: modele, controleur: controleur) -> None:
        '''constructeur qui prend un modele et un controleur en parametre'''
        self.__modele=modele
        self.__ctrl=controleur
        self.__fenetre = tkinter.Tk() #construit la fenetre principale
        self.__fenetre.title("Flood") #titre de la fenetre 
        #liste de couleurs pour associer à chaque valeur (le blanc ne sera pas utilisé car la valeur min est 1)
        self.__couleurs= ['white', 'blue', 'green', 'yellow', 'orange', 'purple', 'red', 'brown', 'pink', 
                            'gray', 'cyan', 'magenta', 'teal', 'maroon', 'navy', 'olive', 'lime', 'silver', 'gold', 
                            'indigo', 'violet', 'turquoise', 'beige', 'coral', 'ivory', 'khaki', 'lavender', 'mint', 'peach', 'salmon', 'tan']
        self.__liste = [] #liste qui contiendra tt les boutons
        self.__boutons= tkinter.Frame(self.__fenetre) #crée un espace pour les boutons
        for l in range(self.__modele.nb_lig()):
            ligne=[]
            for c in range(self.__modele.nb_col()):
                btn = tkinter.Button(self.__boutons,width =2,command=self.__ctrl.creer_controleur_bouton(l,c))
                ligne.append(btn)
                ligne[-1].grid(row=l,column=c)#on ajoute dans la grille le bouton qui vient d'être ajouté dans la ligne au coordonnée(l,c)
            self.__liste.append(ligne) #on ajoute la ligne dans la liste de lignes de boutons
        self.__boutons.pack(side='left')#on met le bouton à gauche
        self.__menu= tkinter.Frame(self.__fenetre) #création de l'espace de menu
        self.__score = tkinter.Label(self.__menu) #on crée un Label qui affichera le score
        self.__score["fg"]="green"#on met le score en vert
        self.__score.grid(row=1, column=0)#on place le score dans la grille au coordonnée (0.0)
        self.__btn_nouveau= tkinter.Button(self.__menu, text="Nouveau", command= self.__ctrl.nouvelle_partie())  #création bouton nouveau
        self.__btn_nouveau.grid(row=3,column=0)#on place le bouton nouveau dans la grille au coordonnée (2.0)
        self.__btn_quitter= tkinter.Button(self.__menu, text="Au revoir",command = self.__fenetre.destroy)  #création bouton au revoir
        self.__btn_quitter.grid(row=6,column=0)#on place le bouton "au revoir" dans la grille au coordonnée (3.0)
        self.__fin = tkinter.Label(self.__menu,fg="blue")
        self.__fin.grid(row=0,column=0)
        self.__coupmax = tkinter.Label(self.__menu)#on crée un nouveau label dans le menu
        self.max=self.__modele.nb_coups_max()#on retient la valeur du nombre de coup max
        self.__coupmax["text"]="Max : "+str(self.max)#on affiche le nombre max
        self.__coupmax.grid(row=2,column=0)#on ajoute à la 2e ligne
        self.reste=3
        self.__coupreste = tkinter.Label(self.__menu)#on crée un nouveau label dans le menu
        self.__coupreste.grid(row=4,column=0)#on ajoute à la 4e ligne
        self.__reinit_part= tkinter.Button(self.__menu, text="Reinit. Partielle", command= self.__ctrl.reinit_partielle())  #création bouton nouveau
        self.__reinit_part.grid(row=5,column=0)#on ajoute le btn à la 5e ligne
        self.__menu.pack(side='right')#on met le menu à droite

    def reinit_partielle(self):
        self.reste-=1
        self.__coupreste["text"]="Reste : "+str(self.reste)#on affiche le nombre de reste
        for l in range(self.__modele.nb_lig()):
            for c in range(self.__modele.nb_col()):
                self.__liste[l][c]["bg"]=self.__couleurs[self.__modele.couleur(l,c)]#redefinie les couleurs aléatoirement
        if self.reste==0:
            self.__reinit_part["state"]=tkinter.DISABLED

    def reinit(self)->None:
        '''la méthode qui reinitialise la Vue en accord avec le modèle'''
        for l in range(self.__modele.nb_lig()):
            for c in range(self.__modele.nb_col()):
                self.__liste[l][c]["bg"]=self.__couleurs[self.__modele.couleur(l,c)]#redefinie les couleurs aléatoirement
                self.__liste[l][c]["state"]=tkinter.NORMAL#remet les boutons à leur état de base
        self.__score["text"]="Score : "+str(self.__modele.score()) #on (re)met le score à 0
        self.__fin["text"]="" #on enlève le texte de la partie Finie
        self.__score["fg"]="green"#on remet le score en vert
        self.max=self.__modele.nb_coups_max()
        self.__coupmax["text"]="Max : "+str(self.max)#on affiche le nombre max
        self.reste=3
        self.__coupreste["text"]="Reste : "+str(self.reste)#on affiche le nombre de reste
        self.__reinit_part["state"]=tkinter.NORMAL

    def redessine(self,lig: int ,col: int)->None:
        '''cette méthode redessine tous les boutons qd on appuie sur un bouton'''
        self.__modele.change_etat_voisines(0,0) #mettre les boutons qui sont voisins (directs ou indirects) à True
        self.__modele.choisit_couleur(lig,col) #mettre le premier carré de la couleur du bouton choisi et augnenter le score
        self.__modele.pose_couleur(self.__modele.couleur(0,0)) #mettre tous les boutons qui sont à l'état True de la même couleur que le premier
        for l in range(self.__modele.nb_lig()):
            for c in range(self.__modele.nb_col()):
                self.__liste[l][c]["bg"]=self.__couleurs[self.__modele.couleur(l,c)] #on recharge la couleur
        self.__score["text"]="Score : "+str(self.__modele.score())#on recharge le score (+1 ou inchangé)
        if self.__modele.partie_fini()==True: #si la partie est finie
            self.__fin["text"]="Partie Finie !" #on informe le joueur 
            for l in range(self.__modele.nb_lig()):
                for c in range(self.__modele.nb_col()):
                    self.__liste[l][c]["state"]=tkinter.DISABLED #on désactive tt les boutons
        if self.max<self.__modele.score():#on regarde si le score du joueur est plus grand que le max
            self.__score["fg"]="red"#si c'est le cas on met le score en rouge
    
    def demarre(self)->None:
        self.reinit() #appelle la methode reinit pour initialiser les couleurs de fond et le score
        self.__fenetre.mainloop()
        
        