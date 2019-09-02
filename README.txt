Execution
---------

La commande ci-dessous est la commande à lancer pour commencer les simulations:
-Linux

python3 launcher.py --topo=nsfnet --netType=0.5 --routeType=1 --size=5000

- Windows

python launcher.py --topo=nsfnet --netType=0.5 --routeType=1 --size=5000


Explications
------------

Le paramètre topo peut prendre une des valeurs suivantes : nsfnet, geant2012, coronet_usa
Il s'agit des différentes topologies de réseau utilisables dans nos simulations

Le paramètre netType peut prendre une des valeurs suivantes : 0, 0.5, 1
- 0 signifie réseau WDM sans conversion de longueur d'onde
- 0.5 signifie réseau WDM avec conversion partielle de longueur d'onde
- 1 réseau WDM avec conversion totale de longueur d'onde

Le paramètre routeType peut prendre une des valeurs suivantes : 1, 2, 3
- 1 signifie que la reconfiguration va concerner une paire d'arbres mono-optiques
- 2 signifie que la reconfiguration va concerner une paire d'arbres multi-optiques
- 3 signifie que la reconfiguration va concerner une paire de forêts optiques

Le paramètre size represente le nombre de fois que  l'on doit générer et reconfigurer le routage. Si votre 
machine n'est pas assez puissante prière reduire ce chiffre. 
 
 N.B: La simulation a été paramétré afin de permettre une reutilisation plus facile pour la reconfiguration 
 d'autre type de paire que des paires d'arbres mono-optiques. Vous poouvez aussi utiliser d'autres topologies que ces trois là. 
 Pour ce faire, il suffit d'ajouter  votre topologie dans le dossier nommée topologies
 
 Le fichier flowchart.png illustre le flux d'exécution d'une simulation 
