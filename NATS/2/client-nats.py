# publisher.py
import asyncio
import nats
import time
import random

fr = {"Auvergne-Rhone-Alpes": {1: ["Bourg-en-Bresse", "Oyonnax", "Bellegarde-sur-Valserine"], 3: ["Moulins", "Vichy", "Montlucon"], 15: ["Aurillac", "Saint-Flour", "Maurs"], 26: ["Valence", "Montelimar", "Die"], 43: ["Le_Puy-en-Velay", "Monistrol-sur-Loire", "Yssingeaux"], 38: ["Grenoble", "Voiron", "Vienne"], 42: ["Saint-Etienne", "Roanne", "Montbrison"], 74: ["Annecy", "Thonon-les-Bains", "Cluses"], 73: ["Chambery", "Albertville", "Aix-les-Bains"]}, "Bourgogne-Franche-Comte": {21: ["Dijon", "Beaune", "Montbard"], 25: ["Besancon", "Pontarlier", "Valdahon"], 39: ["Lons-le-Saunier", "Dole", "Saint-Claude"], 58: ["Nevers", "Decize", "Clamecy"], 70: ["Vesoul", "Gray", "Luxeuil-les-Bains"], 71: ["Chalon-sur-Saone", "Macon", "Le_Creusot"]}, "Bretagne": {22: ["Saint-Brieuc", "Lannion", "Plouha"], 29: ["Brest", "Quimper", "Concarneau"], 35: ["Rennes", "Saint-Malo", "Fougeres"], 56: ["Vannes", "Lorient", "Auray"]}, "Centre-Val_de_Loire": {18: ["Bourges", "Vierzon", "Saint-Amand-Montrond"], 28: ["Chartres", "Chateaudun", "Dreux"], 36: ["Chateauroux", "Issoudun", "Le_Blanc"], 37: ["Tours", "Amboise", "Joue-les-Tours"], 41: ["Blois", "Vendome", "Romorantin-Lanthenay"], 45: ["Orleans", "Montargis", "Pithiviers"]}, "Grand_Est": {10: ["Troyes", "Bar-sur-Aube", "Romilly-sur-Seine"], 51: ["Reims", "Chalons-en-Champagne", "Epernay"], 52: ["Chaumont", "Langres", "Saint-Dizier"], 54: ["Nancy", "Toul", "Luneville"], 55: ["Bar-le-Duc", "Verdun", "Commercy"], 57: ["Metz", "Thionville", "Sarreguemines"], 67: ["Strasbourg", "Colmar", "Haguenau"], 68: ["Mulhouse", "Altkirch", "Colmar"], 88: ["Epinal", "Saint-Die-des-Vosges", "Raon-lEtape"]}, "Hauts-de-France": {2: ["Amiens", "Abbeville", "Albert"], 59: ["Lille", "Roubaix", "Tourcoing"], 60: ["Beauvais", "Compiegne", "Creil"], 62: ["Arras", "Lens", "Douai"], 80: ["Saint-Quentin", "Soissons", "Laon"], 62: ["Boulogne-sur-Mer", "Calais", "Bethune"]}, "Ile-de-France": {75: ["Paris", "Versailles", "Boulogne-Billancourt"], 77: ["Melun", "Cesson", "Fontainebleau"], 78: ["Versailles", "Saint-Germain-en-Laye", "Mantes-la-Jolie"], 91: ["Evry", "Corbeil-Essonnes", "Massy"], 92: ["Nanterre", "Courbevoie", "Puteaux"], 93: ["Saint-Denis", "Bobigny", "Aubervilliers"], 94: ["Creteil", "Vitry-sur-Seine", "Ivry-sur-Seine"], 95: ["Cergy", "Pontoise", "Argenteuil"]}, "Normandie": {14: ["Caen", "Lisieux", "Vire"], 27: ["Evreux", "Bernay", "Louviers"], 50: ["Cherbourg", "Saint-Lo", "Carentan"], 61: ["Alencon", "Flers", "LAigle"], 76: ["Rouen", "Le_Havre", "Dieppe"]}, "Nouvelle-Aquitaine": {16: ["Angouleme", "Cognac", "Rochefort"], 17: ["La_Rochelle", "Rochefort", "Royan"], 19: ["Brive-la-Gaillarde", "Tulle", "Ussel"], 23: ["Gueret", "La_Souterraine", "Aubusson"], 24: ["Perigueux", "Bergerac", "Sarlat-la-Caneda"], 33: ["Bordeaux", "Mérignac", "Pessac"], 40: ["Mont-de-Marsan", "Dax", "Saint-Sever"], 46: ["Cahors", "Figeac", "Prayssac"], 47: ["Agen", "Marmande", "Villeneuve-sur-Lot"], 64: ["Pau", "Bayonne", "Biarritz"], 86: ["Poitiers", "Chattellerault", "Montmorillon"], 87: ["Limoges", "Saint-Junien", "Isle"]}, "Occitanie": {9: ["Foix", "Pamiers", "Saint-Girons"], 11: ["Carcassonne", "Narbonne", "Limoux"], 30: ["Nimes", "Ales", "Bagnols-sur-Ceze"], 31: ["Toulouse", "Muret", "Colomiers"], 32: ["Auch", "Condom", "Mirande"], 34: ["Montpellier", "Sete", "Lunel"], 46: ["Cahors", "Figeac", "Prayssac"], 48: ["Mende", "Langogne", "Chateau_de_Montfort"], 65: ["Tarbes", "Lourdes", "Bagneres-de-Bigorre"], 66: ["Perpignan", "Cerbere", "Argeles-sur-Mer"], 81: ["Albi", "Carmaux", "Mazamet"], 82: ["Montauban", "Castelsarrasin", "Moissac"], 83: ["Nice", "Cannes", "Antibes"], 84: ["Avignon", "Orange", "Carpentras"]}, "Pays_de_la_Loire": {44: ["Nantes", "Saint-Nazaire", "Angers"], 49: ["Angers", "Saumur", "Cholet"], 53: ["Laval", "Mayenne", "Evron"], 72: ["Le_Mans", "La_Fleche", "Sable-sur-Sarthe"], 85: ["La_Roche-sur-Yon", "Les_Sables-dOlonne", "Fontenay-le-Comte"]}, "Provence-Alpes-Cote_dAzur": {4: ["Digne-les-Bains", "Sisteron", "Mallemoisson"], 5: ["Gap", "Chorges", "Veynes"], 6: ["Nice", "Cannes", "Antibes"], 13: ["Marseille", "Aix-en-Provence", "Arles"], 83: ["Toulon", "Hyres", "Frejus"], 84: ["Avignon", "Carpentras", "Orange"]}}

def choix_ville(fr):
    while True:
        if not fr:
            return None

        region = random.choice(list(fr.keys()))
        if not fr[region]:
            del fr[region]
            continue
        
        departement_num = random.choice(list(fr[region].keys()))
        if not fr[region][departement_num]:
            del fr[region][departement_num]
            if not fr[region]:
                del fr[region]
            continue
        
        ville = random.choice(fr[region][departement_num])
        fr[region][departement_num].remove(ville)
        return f"fr.{region}.{departement_num}.{ville}"

async def publish():
    # Connexion au serveur NATS
    nc = await nats.connect("nats://127.0.0.1:4222")

    # Publication du message "bonjour" sur le sujet "salut"
    while True:
        ville=choix_ville(fr)
        try:
            await nc.publish(ville, f"Coucou {ville.split('.')[-1]}".encode())
            print(f"Message envoyé à {choix_ville(fr)}")
        except AttributeError:
            print(f"Fin de la liste")
            break

    await nc.close()

if __name__ == "__main__":
    total_villes = sum(len(villes) for departements in fr.values() for villes in departements.values())
    print(f"{total_villes} villes en tout")
    time.sleep(3)
    asyncio.run(publish())
    
