import plotly.express as px
import pandas as pd
import pprint
import statistics
from datetime import datetime
from collections import defaultdict

#Fonction pour l'affichage du dataframe Panda
def set_pandas_display_options() -> None:
    display = pd.options.display
    display.max_columns = 100
    display.max_rows = 100
    display.max_colwidth = 199
    display.width = None

#Fonction pour eviter les divisions par 0
def division_sure(numerateur, denominateur):
    """
    Effectue une division en évitant la division par zéro.
    Retourne None si le dénominateur est nul.
    """
    try:
        # Vérification explicite
        if denominateur == 0:
            print("Erreur : division par zéro interdite.")
            return None
        
        # Division normale
        return numerateur / denominateur
    
    except TypeError:
        print("Erreur : les deux valeurs doivent être des nombres.")
        return None


df_donnees = pd.read_csv('https://docs.google.com/spreadsheets/d/e/2PACX-1vSC4KusfFzvOsr8WJRgozzsCxrELW4G4PopUkiDbvrrV2lg0S19-zeryp02MC9WYSVBuzGCUtn8ucZW/pub?output=csv')

#je rajoute  une colonne CA_Genere, qui sera plus simple à manipuler pour les calculs et stats
# Vérification que les colonnes existent et contiennent des valeurs numériques
if all(col in df_donnees.columns for col in ['prix', 'qte']):
    try:
        # Création d'une nouvelle colonne 'CA_Genere' = prix * qte
        df_donnees['CA_Genere'] = df_donnees['prix'] * df_donnees['qte']
        
    except Exception as e:
        print(f"Erreur lors du calcul : {e}")
else:
    print("Colonnes manquantes dans le DataFrame.")

#print(df_donnees)

figure = px.pie(df_donnees, values='qte', names='region', title='quantité vendue par région')

#Affichage
set_pandas_display_options()

# Group by 'Category' and calculate count and mean
stats_par_produit = df_donnees.groupby('produit').agg(
    Moyenne=('CA_Genere', 'mean'),     # Average value in each group
    Mediane=('CA_Genere', 'median')
).reset_index()

print("Ci-dessous, tableau des stats Panda: nombre de ventes et CA moyen généré par produit")
print(stats_par_produit,"\n\n")


df_stats_par_volume = df_donnees.groupby('produit').agg(
    EcartType=('qte', 'std'),
    Variance=('qte', 'var')
).reset_index()

print("Ci-dessous, tableau statistique pour le volume de ventes par produit issu de Panda"+ "\n")
print(df_stats_par_volume,"\n\n")


## Creation de fonction sans Panda
# Function 1: produit le plus vendu
# Function 2: produit le moins vendu
### Mediane=  valeur qui divise un ensemble de données ordonnées en deux parties égales. 
# Pour la calculer, il faut d'abord trier les données de la plus petite à la plus grande. 
# Si le nombre de valeurs est impair, la médiane est la valeur du milieu. Si le nombre de valeurs est pair, la médiane est la moyenne des deux valeurs centrales. En d'autres termes, il y a autant de valeurs inférieures à la médiane 
###
### Variance
# la variance est une mesure de la dispersion des valeurs d'un échantillon ou d'une variable aléatoire.
#
### Ecart-type
#L'écart type, noté généralement par la lettre grecque σ (sigma), est défini comme la racine carrée de la variance.
# Il mesure à quel point les valeurs d'un échantillon ou d'une population sont dispersées autour de la moyenne.


# Conversion du dataframe en liste
l_donnees = df_donnees.values.tolist()

d_parproduit_CAgenere_unitairement={}
d_parproduit_ventes_qte={}


for date, produit,prix,qte, region, total  in     l_donnees :
    d_parproduit_CAgenere_unitairement.setdefault(produit, []).append(total)
    d_parproduit_ventes_qte.setdefault(produit, []).append(qte)

#print(d_parproduit_CAgenere_unitairement)
#print(d_parproduit_ventes_qte)

d_volume_des_ventes= defaultdict(list)

print('\nCheck des stats précédentes\n')

for key, values in d_parproduit_CAgenere_unitairement.items() :
    d_volume_des_ventes[key] = sum(d_parproduit_ventes_qte[key])

    print('Le CA généré par le produit', key, '=', sum(values) , '€')
    print('Le nombre de ventes pour le produit', key, '=', sum(d_parproduit_ventes_qte[key]) )

    print('La vente moyenne pour le produit ', key, '=',  division_sure(sum(values), sum(d_parproduit_ventes_qte[key])), '€'  )

    print('La mediane pour le CA généré du produit ', key, '=', statistics.median( values )  )
    
    print("L'ecart-type  pour le volume des ventes du produit ", key, '=', statistics.stdev( d_parproduit_ventes_qte[key] ) )
    
    print('La variance  pour le volume des ventes du produit ', key, '=', statistics.variance( d_parproduit_ventes_qte[key] ) ) 

    print('\n')

#Code pour trouver le produit le moins vendu ou le plus vendu en volumes de vente
#print((d_volume_des_ventes))
# Trouve le minimum en comparant le 2nd element

min_ventes = min([(k,v) for k,v in d_volume_des_ventes.items()], key=lambda t: t[1])
print('Le produit le moins vendu est: ', min_ventes)

max_ventes = max([(k,v) for k,v in d_volume_des_ventes.items()], key=lambda t: t[1])
print('Le produit le plus vendu est: ', max_ventes)


# Graphiques avec Plotly

figure1 = px.bar(df_donnees, x='produit', y='qte', color="date", title='Quantités / Ventes par produit')
figure1.show()

figure2 = px.bar(df_donnees, x='produit', y='CA_Genere', color="date", title='CA par produit')
figure2.show()

  
