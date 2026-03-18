import requests
from concurrent.futures import ThreadPoolExecutor

# =========================
# SESSION (plus rapide)
# =========================
session = requests.Session()

# =========================
# MAPPING DES RELATIONS
# =========================
def createmapping():
    listee = {}
    response = session.get("https://jdm-api.demo.lirmm.fr/v0/relations_types")
    data = response.json()
    for type in data:
        listee[type.get("name")] = type.get("id")
    return listee

idParNom = createmapping()
allrelationsfound = []

# =========================
# INPUT UTILISATEUR
# =========================
linput = input("Entrez un input du format suivant : mot1 relation mot2\n")
separer = linput.split()

if len(separer) != 3:
    print("Erreur : L'input doit être au format 'mot1 relation mot2'")
    exit()

mot1, relation, mot2 = separer

# =========================
# RELATIONS DIRECTES
# =========================
url = f"https://jdm-api.demo.lirmm.fr/v0/relations/from/{mot1}/to/{mot2}"
response = session.get(url)

if response.status_code != 200:
    print("Erreur: l'un des deux mots n'existe pas.")
    exit()

data = response.json()
listerelations = data.get("relations", [])

if len(listerelations) == 0:
    print("\nPas de relations directe\n")
else:
    for i in listerelations:
        if i.get("type") == idParNom.get(relation):
            allrelationsfound.append(i.get("id"))

# =========================
# RECUPERATION DES NODES INTERMEDIAIRES
# =========================
urltransi = f"https://jdm-api.demo.lirmm.fr/v0/relations/from/{mot1}"
response = session.get(urltransi)

if response.status_code != 200:
    print("Erreur récupération des noeuds")
    exit()

data2 = response.json()
listnode = data2.get("nodes", [])

listnode = [i for i in listnode if i.get("type") != 200]

# =========================
# FONCTION PARALLELE
# =========================
def process_node(node):
    node_name = node.get("name")

    try:
        # relation node -> mot2
        url = f"https://jdm-api.demo.lirmm.fr/v0/relations/from/{node_name}/to/{mot2}"
        response = session.get(url)

        if response.status_code != 200:
            return []

        data = response.json()
        listerelations = data.get("relations", [])

        results = []

        for r in listerelations:
            if r.get("type") == idParNom.get(relation):

                # relation mot1 -> node
                url2 = f"https://jdm-api.demo.lirmm.fr/v0/relations/from/{mot1}/to/{node_name}"
                response2 = session.get(url2)

                if response2.status_code != 200:
                    continue

                getrelation = response2.json().get("relations", [])

                for r2 in getrelation:
                    results.append((r2.get("id"), r.get("id")))

        return results

    except:
        return []

# =========================
# EXECUTION PARALLELE
# =========================
with ThreadPoolExecutor(max_workers=10) as executor:
    results = list(executor.map(process_node, listnode))

# =========================
# FLATTEN RESULTATS
# =========================
for res in results:
    allrelationsfound.extend(res)

# =========================
# RESULTAT FINAL
# =========================
print("\nRésultats trouvés :")
print(allrelationsfound)