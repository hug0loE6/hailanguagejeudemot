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
else:
    print(f"Erreur: l'un des deux mots n'existe pas.")