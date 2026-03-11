import requests
# c'est :r{idrelation} pour avoir le node de la relation avec son nom relater venant de la relation
# Récupérer l'input de l'utilisateur
input = input("Entrez un input du format suivant : mot1 relation mot2\n")

separer = input.split()
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



else:
    print(f"Erreur: l'un des deux mots n'existe pas.")


if len(data.get("relations"))==0:
    print("\n :( \n")

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

        if len(data.get("relations"))!=0:
            print(i.get("name"))
            
        

