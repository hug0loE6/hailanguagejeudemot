import requests
from concurrent.futures import ThreadPoolExecutor
from relation import RelationNode, CoupleRelation

# =========================
# SESSION (plus rapide)
# =========================
session = requests.Session()

# =========================
# MAPPING DES RELATIONS
# =========================
def createmapping():
    idnom = {}
    nomid = {}
    response = session.get("https://jdm-api.demo.lirmm.fr/v0/relations_types")
    data = response.json()
    for type in data:
        idnom[type.get("name")] = type.get("id")
        nomid[type.get("id")] = type.get("name")
    return idnom, nomid

idParNom, nomParId = createmapping()
allrelationsfound = []

# =========================
# INPUT UTILISATEUR
# =========================

def splitrelation(str):
    str = str.split()
    indexRelation = -1
    for i in range(len(str)):
        if str[i].startswith("r_"):
            indexRelation = i
            break
    w1 = " ".join(str[:indexRelation])
    relation = str[indexRelation]
    w2 = " ".join(str[indexRelation+1:])
    if indexRelation == -1:
        print("Erreur : L'input doit être au format 'mot1 relation mot2'")
        exit()
    return w1, relation, w2

linput = input("Entrez un input du format suivant : mot1 relation mot2\n")
mot1, relation, mot2 = splitrelation(linput)


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
            allrelationsfound.append(RelationNode(i.get("id"), mot1, mot2, i.get("type"), relation))

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
                    rel1 = RelationNode(r2.get("id"), mot1, node_name, r2.get("type"), nomParId.get(r2.get("type")))
                    rel2 = RelationNode(r.get("id"), node_name, mot2, r.get("type"), relation)
                    results.append(CoupleRelation(rel1, rel2))

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

resultatspertinents=[]
for a in allrelationsfound:
    if isinstance(a,RelationNode):
        print(a)
        print("\n")
    else:
        if a.relation1.relation_typename=="r_isa" or a.relation1.relation_typename=="r_hypo" or a.relation1.relation_typename == a.relation2.relation_typename:
            resultatspertinents.append(a)

for a in resultatspertinents:
    print(a)
    print("\n")