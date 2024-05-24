pypyBABA est une suite d'application web permettant de dimensionner rapidement et facilement les éléments courants de béton armé selon l'Eurocode 2.

Vous pouvez tester l'application ici : https://pypyBABA.fr

Comme vous pouvez le voir, le projet n'est en fait pas limité à l'eurocode 2. Il est presque toujours nécessaire d'appliquer les autres parties de l'Eurocode (EC 0, 1, 5, 6, 7, 8).

<!-- Elle utilise :
- HTML CSS pour l'interface web
- Java Script pour transmettre les données d'entrée saisie sur la page web vers les modules Python
- Python pour la réalisation des calcul à l'Eurocode 2
- Pyscript pour renvoyer les résultats sur l'interface web -->

# Architecture du projet
Le projet est articulé autour de quatre groupes de dossier :
1. L'interface web composée des dossiers :
    - /html : chaque fichier html correspond à une application de calcul
    - /img : contient le fond d'écran
    - /css : un fichier pour la mise en forme générale du site  
</br>

2. Récupération des données d'entrée, lancement des calculs et affichage des résultats :
    - /pyscript : script python
    - /toml : configuration de pyscript 
</br>

3. Les modules de calcul béton armé :
    - /pyeurocode2 : contient les modules de calcul
</br>

4. La documentation des applications
    - /pdf : PDF téléchargeable décrivant le fonctionnement de chaque application

# Bibliographie

# Feuille de route
## Matériaux béton armé
- [ ] Caractéristique des bétons
- [ ] Caractéristique des aciers de béton armé

## Dispositions constructives
- [ ] Calcul de l'enrobage nominal
- [ ] Longueur d'ancrage et de recouvrement des barres
- [ ] Longueur d'ancrage et de recouvrement des treillis soudés

## Analyse structurale
- [ ] Portée de calcul des poutres et dalles

## Les sollicitations
### Traction simple
- [ ] Tirant

### Compression simple
- [ ] Poteau rectangulaire
- [ ] Poteau ciculaire

### Flexion simple
- [ ] Section rectangulaire
- [ ] Section en Té

### Effort tranchant
- [ ] Poutre rectangulaire
- [ ] Jonction table - hourdi

### Flexion composée
- [ ] Section rectangulaire
- [ ] Section circulaire

### Flexion déviée
- [ ] Section rectangulaire

### Maîtrise de la fissuration
- [ ] Calcul des ouvertures de fissure

## Les éléments courants de béton armé
### Semelle filante
- [ ] Sous charge centrée
- [ ] Sous charge excentrée

### Semelle isolée
- [ ] Sous charge centrée
- [ ] Sous charge excentrée
- [ ] Poinçonnement

### Longrine de redressement
- [ ] Longrine de redressement

### Poteau selon la méthode du guide d'application de l'Eurocode
- [ ] Poteau rectangulaire
- [ ] Poteau ciculaire

### Voile
- [ ] Voile sous charge centrée
- [ ] Voile de contreventement

### Poutre
- [ ] Pourcentage minimal et maximal d'armatures
- [ ] Poutre continue sous charge modérée
- [ ] Poutre continue sous charge élevée
- [ ] Bielle d'appui
- [ ] Ancrage des appuis
- [ ] Ouvertures dans les poutres

### Corbeau
- [ ] Corbeau

### Poutre voile
- [ ] Poutre voile uniformément chargée sur 2 appuis
- [ ] Poutre voile en console
- [ ] Voile drapeau

### Dalle
- [ ] Pourcentage minimal et maximal d'armatures
- [ ] Dalle uniformément chargée sur 4 appuis articulés
- [ ] Dalle uniformément chargée sur 3 appuis articulés + 1 bord libre
- [ ] Poinçonnement

### Système Bielle-Tirant
- [ ] Noeud
- [ ] Bielle