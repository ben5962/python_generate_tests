# coding: utf-8
import astor
import ast
import typing
import pathlib


__all__ = ['produire_tests']


def produire_tests(ch : str):
    m = Module2Arbre(ch)
    with open("test_auto_{}".format(m.nom_fichier), "w") as f:
        f.write(m.produire_test)
    print("avons ecrit fichier test ""test_auto_{}".format(m.nom_fichier))

class Fonction(object):
    def __init__(self, le_noeud :ast.FunctionDef ):
        self.noeud = le_noeud
        self.nom = self.get_nom(self.noeud)
        self.args = [self.get_valeur_arg(arg) for arg in self.get_liste_d_objets_arguments(
            self.get_objet_arguments_de_fonc(self.noeud)
            )]
        self._letexte = ""
        
    def get_nom(self, noeud: ast.FunctionDef):
        """renvoie le nom d un noeud de type fonction"""
        return noeud.name


    def get_objet_arguments_de_fonc(self, noeud: ast.FunctionDef) -> ast.arguments:
        return noeud.args

    def get_liste_d_objets_arguments(self, obj_arg_f : ast.arguments) -> typing.List[ast.arg]:
        return obj_arg_f.args

    def get_valeur_arg(self, obj_arg : ast.arg) -> str:
        return obj_arg.arg

    def produire_test(self):

        def produire_chapeau_test():
            return "\tdef test_{}(self):\n".format(self.nom)
        def produire_valeur_obtenue():
            chaine = "\t\tvaleur_obtenue = {}(".format(self.nom)
            for arg in self.args:
                chaine += "{} = TODO, ".format(arg)
            chaine += ")\n"
            return chaine
        def produire_valeur_attendue():
            return "\t\tvaleur_attendue = TODO\n"
        def produire_comparaison():
            return "\t\tself.assertEquals(valeur_obtenue, valeur_attendue)"
        return produire_chapeau_test() +\
               produire_valeur_obtenue() +\
               produire_valeur_attendue() +\
               produire_comparaison()
    def __repr__(self):
        return "Fonction({})".format(self.nom)

class Module2Arbre(object):
    def __init__(self, le_fichier : pathlib.Path ):
        if isinstance(le_fichier, str):
            le_fichier = pathlib.Path(le_fichier)
        self.nom_fichier = self.get_nom_fichier(le_fichier)
        #self.nom_module = self.get_nom_module(le_fichier)
        self.nom_module = le_fichier.stem
        self.mon_ast = astor.parse_file(self.nom_fichier)
        self.mes_fonctions = self.getFonctions()
        self.produire_test = self.produireTest()

    def get_nom_fichier(self, le_fichier : pathlib.Path) -> str :
        """le nom de fichier se termine par .py. le nom de module, non"""
        def pred_is_not_file(fich : pathlib.Path)-> bool:
            return not fich.is_file()
        if pred_is_not_file(le_fichier):
            raise Exception("je veux un chemin vers un fichier, relatif ou absolu")
        else:
            return le_fichier.name

    def get_nom_module(self, le_fichier : pathlib.Path) -> str :
        """le nom de fichier se termine par .py, le nom de module, non"""
        return le_fichier.stem

      
    def getFonctions(self) -> typing.List[Fonction]:
        liste = []
        for noeud in self.mon_ast.body:
            if isinstance(noeud, ast.FunctionDef):
                ma_fonc = Fonction(noeud)
                liste.append(ma_fonc)
        return liste

    def produireTest(self):
        def supprimer_derniere_virgule(chaine):
            return ''.join(list(chaine)[:-2])
        def produire_entete():
            chaine = "import unittest\nfrom {} import ".format(self.nom_module)
            for f in self.mes_fonctions:
                chaine += "{}, ".format(f.nom)
            chaine = supprimer_derniere_virgule(chaine)
            
            chaine += "\nclass le_test(unittest.TestCase):\n"
            return chaine
                
        def produire_tests_fonctions():
            texte = ""
            for f in self.mes_fonctions:
                texte += f.produire_test()
                texte += "\n"
            return texte
        return produire_entete() + produire_tests_fonctions()
        
            
            
        

def exemple():
    produire_tests("contains_duplicate3.py")

if __name__ == '__main__':
    exemple()
                                                                                                                  

    

        
