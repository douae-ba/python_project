from Bibliotheque import Bibliotheque
import matplotlib.pyplot as plt
import csv
from datetime import datetime,timedelta
def diagramme_genre(biblio:Bibliotheque):
    genre_c={}
    for info in biblio.livres.values():
        genre=info["livre"].genre
        stock=info["stock"]
        if genre in genre_c:
            genre_c[genre]+=stock
        else:
            genre_c[genre]=stock
    labels=list(genre_c.keys())
    sizes=list(genre_c.values())
    plt.figure(figsize=(8,8))
    plt.pie(sizes,labels=labels,autopct='%1.1f%%',startangle=90)
    plt.title("Répartition du livre par genre")
    plt.axis("equal")
    plt.savefig("assets/stats_genres.png")
    plt.show()
    
def top_diagramme(biblio:Bibliotheque):
    top={}
    for membre in biblio.membres.values():
        for livre in membre.livres_empruntes:
            auteur=livre.auteur
            if auteur in top:
                top[auteur]+=1
            else:
                top[auteur]=1
    top_10=sorted(top.items(),key=lambda x:x[1], reverse=True)[:10]
    auteurs=[a[0] for a in top_10]
    nb_emprunts=[a[1] for a in top_10]
    plt.figure(figsize=(10,6))
    plt.bar(auteurs,nb_emprunts,color='skyblue')
    plt.xticks(rotation=45, ha='right')
    plt.xlabel('Auteurs')
    plt.ylabel("Nombre d'emprunts")
    plt.title("top 10 auteurs ")
    plt.savefig("assets/stats_auteurs.png")
    plt.show()
    
def courbe_activite():
    today=datetime.today().date()
    date_range=[today - timedelta(days=i) for i in range(29,-1,-1)]
    activite={date:0 for date in date_range}
    with open("data/historique.csv","r") as f:
        reader=csv.reader(f,delimiter=';')
        for row in reader:
            date_str, _, _, action =row
            if action.strip()=="emprunt":
                date_obj=datetime.strptime(date_str,"%Y-%m-%d").date()
                if date_obj in activite: 
                    activite[date_obj]+=1
    dates=list(activite.keys())
    emprunts=list(activite.values())
    plt.figure(figsize=(10,5))
    plt.plot(dates,emprunts,marker='o', linestyle='-',color='blue')
    plt.title("activité des empruns (30 derniers jours)")
    plt.xlabel("Date")
    plt.ylabel("Nombre d'emprunts")
    plt.xticks(rotation=45)
    plt.grid(True)
    plt.show()



