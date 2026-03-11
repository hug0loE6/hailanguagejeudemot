import requests
# c'est :r{idrelation} pour avoir le node de la relation avec son nom relater venant de la relation
# Récupérer l'input de l'utilisateur


def createmapping():
    listee = {}
    response = requests.get("https://jdm-api.demo.lirmm.fr/v0/relations_types")
    data = response.json()
    for type in data:
        listee[type.get("name")] = type.get("id")
    return listee

allrelationsfound = []

idParNom = createmapping()

linput = input("Entrez un input du format suivant : mot1 relation mot2\n")

separer = linput.split()
if len(separer) != 3:
    print("Erreur : L'input doit être au format 'mot1 relation mot2'")
    exit()

mot1, relation, mot2 = separer

# URL de l'API
url = f"https://jdm-api.demo.lirmm.fr/v0/relations/from/{mot1}/to/{mot2}"

# Effectuer une requête GET
response = requests.get(url)

# Vérifier que la requête a réussi
if response.status_code == 200:
    # Récupérer les données JSON
    data = response.json()
    print(data)
    print("\n")
    listerelations = data.get("relations")
else:
    print(f"Erreur: l'un des deux mots n'existe pas.")
    exit()

if len(listerelations)==0:
    print("\n Pas de relations directe \n")
else:
    for i in listerelations:
        if i.get("type") == idParNom.get(relation):
            allrelationsfound.append(i.get("id"))

urltransi = f"https://jdm-api.demo.lirmm.fr/v0/relations/from/{mot1}"

response = requests.get(urltransi)

# Vérifier que la requête a réussi
if response.status_code == 200:
    # Récupérer les données JSON
    data2 = response.json()
    print("\n")
    listnode =data2.get("nodes")

    for i in listnode[:]:
        if i.get("type") == 200:
            listnode.remove(i)

    for i in listnode:
        url= f"https://jdm-api.demo.lirmm.fr/v0/relations/from/{i.get('name')}/to/{mot2}"
        
        response2 = requests.get(url)
        data=response2.json()
        listerelations = data.get("relations")

        for r in listerelations:
            if r.get("type") == idParNom.get(relation):
                getrelation = requests.get(f"https://jdm-api.demo.lirmm.fr/v0/relations/from/{mot1}/to/{i.get('name')}").json().get("relations")
                for r2 in getrelation:
                    allrelationsfound.append((r2.get("id"),r.get("id")))

    print(allrelationsfound)
        

