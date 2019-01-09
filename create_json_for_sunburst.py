import json
import xlrd
from toolz import unique


pc = []
# On remplit ici le nom de la root
# pc.append([-1, 0 ,"Catalogue de services IMA", 1000])
# Append de test pour comprendre la logique des id de chaque item
# pc.append([0,1, "Plateforme Auto", 1000])
# pc.append([0,2, "Plateforme habitation", 1000])
# pc.append([0,3, "Plateforme PSBV", 1000])
# pc.append([1, 2, "Dépannage", 1000])
# pc.append([1, 3, "Remorquage", 1000])
# pc.append([2 ,4, "plombier", 1000])
# pc.append([2 ,5, "menuisier" ,1000])
# pc.append([1 ,5, "epave", 1000])
# pc.append([5, 6, "BetweennessCentrality", 1000])
# pc.append([5, 7, "LinkDistance",1000])



# Fonction trouvée sur https://stackoverflow.com/questions/7523920/converting-a-parent-child-relationship-into-json-in-python/7524133
def listToDict(input):
    root = {}
    lookup = {}
    for parent_id, id, name, attr in input:
        if parent_id == -1: 
            root['name'] = name
            lookup[id] = root
        else:
            node = {'name': name}
            lookup[parent_id].setdefault('children', []).append(node)
            lookup[id] = node
    return root

def make_tree(pc_list):
    results = {}
    for record in pc_list:
        parent_id = record[0]
        id = record[1]

        if id in results:
            node = results[id]
        else:
            node = results[id] = {}

        node['name'] = record[2]
        node['size'] = record[3]
        if parent_id != id:
            if parent_id in results:
                parent = results[parent_id]
            else:
                parent = results[parent_id] = {}
            if 'children' in parent:                
                parent['children'].append(node)
            else:
                parent['children'] = [node]        

    # assuming we wanted node id #0 as the top of the tree          
    return results[0] 

def row_from_excel(pc):
    wb = xlrd.open_workbook('21122018_Catalogue Services_Groupe IMA_WIP2.xlsx')
    sh = wb.sheet_by_name('BDD services IMA')

    # On déclare les listes des différents items selon leur familles
    liste_plateforme = []
    liste_gammes = []
    liste_offres = []
    liste_services = []

    # sh.nrows = nombre total de row dans le doc
    # sh.row_values(rownum) = donne les infos de la row sous la forme d'une list

    for rownum in range(sh.nrows):
        # On ajoute à la liste correspondante l'item en question une fois seulement
        # Exemple pour liste plateforme on aura ['PSBV', 'HABITATION', 'AUTO']
        if sh.row_values(rownum)[0] not in liste_plateforme:
            liste_plateforme.append(sh.row_values(rownum)[0])
        if sh.row_values(rownum)[1] not in liste_gammes:
            liste_gammes.append(sh.row_values(rownum)[1])
        if sh.row_values(rownum)[2] not in liste_offres:
            liste_offres.append(sh.row_values(rownum)[2])
        if sh.row_values(rownum)[3] not in liste_services:
            liste_services.append(sh.row_values(rownum)[3])

    for rownum in range(sh.nrows):
        # On récupére le nom des univers, gammes, offres et services
        service = sh.row_values(rownum)[3]
        offre = sh.row_values(rownum)[2]
        gamme = sh.row_values(rownum)[1]
        univers = sh.row_values(rownum)[0]

        # On récupére la taille de la liste de chaque famille
        indice_service = liste_services.index(sh.row_values(rownum)[3])
        indice_offre = liste_offres.index(sh.row_values(rownum)[2])
        indice_gamme = liste_gammes.index(sh.row_values(rownum)[1])
        indice_univers = liste_plateforme.index(sh.row_values(rownum)[0])

        # On append au dict la root du json 
        pc.append([-1, 0 ,"Catalogue de services IMA", 80]) 

        # On append au dict la liste des univers
        # Nb pour que la fonction de transformation en json fonction inel faut que chaque indice soit différent
        # On ajoute donc 1 à l'indice qui commence par 0 car 0 est déjà utilisé comme indice par le root
        # Donc les indices suivants seront 1, 2 et 3
        pc.append([0, indice_univers + 1, univers, 40])

        # On reprend comme indice parent l'indice précédent et l'indice de l'élément en cours devient l'indice courant + la len de la famille précédente
        pc.append([indice_univers + 1 , indice_gamme+len(liste_plateforme)+1, gamme, 20])
        pc.append([indice_gamme+len(liste_plateforme)+1, indice_offre+len(liste_gammes), offre, 10])
        pc.append([indice_offre +len(liste_gammes), indice_service+len(liste_offres), service,5])

    # Comme on a des doublons dans le dict on rend unique chaque élément
    res = map(list, unique(map(tuple, pc)))
    # On retourne le résultat
    return res

result = make_tree(row_from_excel(pc))
print (result)
print (json.dumps(result, indent=4))

f= open("data_for_sunburst.py","w+")

f.write("data_sunburst = " + str(json.dumps(result, indent=4)))

f.close()

