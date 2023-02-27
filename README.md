# Projet Battleship

**Auteurs :** Tran Sylvain, Aoudia Hakim

**Date :** 2020-2021 (L1, semestre 1)

**Objectif :**  
Réaliser le jeu Bataille Navale en python avec la bibliothèque graphique de l'UGE fltk.

**Principe du jeu :**  
C'est un jeu mi-devinette, mi-stratégie, à deux joueurs.  
Le but est de deviner l'emplacement exact des navires de l'adversaire pour les couler avant qu'il ne coule tous les nôtres.
Si lors d'un tir, un navire est touché ou coulé, le joueur qui a tiré peut réitérer un nouveau tir. Sinon, c'est à l'autre de tirer et vice versa.
Le permier qui voit sa flotte détruite perd.

Ici, on laisse aux joueurs (s'ils le souhaitent) la possibilité de placer de façon aléatoire leurs navires sur leur plateau.  
On a également créé un mode de jeu à un joueur où celui-ci joue contre un bot.
Il pourra choisir le niveau de difficulté du bot au début de la partie via un menu.  
**Les 2 niveaux du bot :**  
1. EASY : le bot tire aléatoirement à chaque fois.
2. HARD : le bot est plus malin. Dès qu'il touche un navire, il va viser les cases adjacentes susceptibles de contenir un autre bout du navire.

**Documentation Technique et Utilisateur :**  
Voir le fichier `aoudia_tran_bataille_navale.pdf`