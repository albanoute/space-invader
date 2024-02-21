import pyxel
from random import randint

pyxel.init(128,128, title="Space Invader")
pyxel.load('sample.pyxres')

played = False
commandes = False
vaisseau_x, vaisseau_y = 60,60
liste_tirs = []
liste_ennemis = []
liste_explosions = []
liste_vies = []
liste_tirs_ennemis = []
liste_etoile = []
vies = 0
score = 0
bestscore = 0
munitions = 5
proba_tir_ennemis = 200
boost = 0
boost_activated = False

speed_vaisseau = 1.5
speed_ennemis = 1
speed_tirs = 2
speed_vie = 0.75
speed_tirs_ennemis = 2
speed_etoiles = 1.75

def vaisseau_deplacement(x, y):
    if pyxel.btn(pyxel.KEY_RIGHT):
        if x < 120 :
            x += speed_vaisseau
    if pyxel.btn(pyxel.KEY_LEFT):
        if x > 0:
            x -= speed_vaisseau
    if pyxel.btn(pyxel.KEY_DOWN):
        if y < 120:
            y += speed_vaisseau
    if pyxel.btn(pyxel.KEY_UP):
        if y > 0:
            y -= speed_vaisseau
    return (x,y)

def tirs_creation(x, y, liste_tirs, munitions):
    if boost_activated == True:
        if pyxel.frame_count % 3 == 0:
            liste_tirs.append([x+2, y-3])
    elif pyxel.btnr(pyxel.KEY_SPACE) and munitions > 0:
        liste_tirs.append([x+2, y-3])
        munitions -= 1
    return munitions

def tirs_deplacement(liste_tirs):
    for tir in liste_tirs:
        tir[1] -= speed_tirs
        if tir[1] <= - 4:
            liste_tirs.remove(tir)

def ennemis_creation(liste_ennemis):
    if pyxel.frame_count % 45 == 0:
        liste_ennemis.append([randint(0,120), 0])

def ennemis_deplacement(liste_ennemis, vies):
    for ennemi in liste_ennemis:
        ennemi[1] += speed_ennemis
        if ennemi[1] > 130:
            liste_ennemis.remove(ennemi)
            vies -= 1
    return vies

def vaisseau_suppression(vies):
    for ennemi in liste_ennemis:
        if abs(ennemi[0] - vaisseau_x) <= 8 and abs(ennemi[1] - vaisseau_y) <=8:
            liste_ennemis.remove(ennemi)
            liste_explosions.append([ennemi[0] + 4, ennemi[1] + 4, 0])
            vies -= 1
    for tir in liste_tirs_ennemis:
        if abs(tir[0] - vaisseau_x) <= 8 and abs(tir[1] - vaisseau_y) <=8:
            liste_tirs_ennemis.remove(tir)
            liste_explosions.append([tir[0] + 4, tir[1] + 4, 0])
            vies -= 1
    return vies

def ennemis_suppression(liste_ennemis, liste_tirs, score, munitions):
    touche = False
    for ennemi in liste_ennemis:
        for tir in liste_tirs:
            if (tir[0]+3 - ennemi[0] <= 8 or tir[0] - ennemi[0]) <= 8 and (tir[0] - ennemi[0] >= 0 or tir[0]+3 - ennemi[0] >= 0):
                if abs(tir[1] - ennemi[1]) <= 7:
                    liste_tirs.remove(tir)
                    if ennemi in liste_ennemis:
                        liste_ennemis.remove(ennemi)
                    liste_explosions.append([tir[0], ennemi[1] - 1, 0])
                    touche = True
    if touche == True:
        score += 1
        if boost_activated == False:
            munitions += 2
    return score, munitions

def explosions_creation():
    for explosion in liste_explosions:
        explosion[2] += 1
        if explosion[2] == 10:
            liste_explosions.remove(explosion)

def vie_creation(vies, score, liste_vies, proba_tir_ennemis):
    if score % 10 == 0 and score != 0:
        score += 1
        liste_vies.append([randint(0,120), 0])
        if proba_tir_ennemis > 50:
            proba_tir_ennemis -= 20
    return score, proba_tir_ennemis

def vie_deplacement(liste_vies):
    for vie in liste_vies:
        vie[1] += speed_vie
        if vie[1] > 130:
            liste_vies.remove(vie)

def vie_colision(liste_vies, vies):
    for vie in liste_vies:
        if abs(vie[0] - vaisseau_x) <= 8 and abs(vie[1] - vaisseau_y) <=8:
            liste_vies.remove(vie)
            if vies < 3:
                vies += 1
    return vies

def ennemis_tirs_creation(liste_ennemis, liste_tirs_ennemis):
    for ennemi in liste_ennemis:
        if randint(0,proba_tir_ennemis) == 1:
            liste_tirs_ennemis.append([ennemi[0] + 2, ennemi[1] + 3])

def ennemis_tirs_deplacement(liste_tirs_ennemis):
    for tir in liste_tirs_ennemis:
        tir[1] += speed_tirs_ennemis
        if tir[1] >=  140:
            liste_tirs_ennemis.remove(tir)

def tirs_colisions(v):
    for tir_ennemis in liste_tirs_ennemis:
        for tir_vaisseau in liste_tirs:
            if abs(tir_ennemis[0] - tir_vaisseau[0]) <= 4 and abs(tir_ennemis[1] - tir_vaisseau[1]) <=4:
                liste_tirs.remove(tir_vaisseau)
                liste_tirs_ennemis.remove(tir_ennemis)
                liste_explosions.append([tir_ennemis[0] + 2, tir_ennemis[1] + 4, 0])

def etoiles(liste_etoile):
    if pyxel.frame_count % 2 == 0:
        liste_etoile.append([randint(0,126), 0])

def etoile_deplacement(liste_etoile):
    for etoile in liste_etoile:
        etoile[1] += speed_etoiles
        if etoile[1] >=  140:
            liste_etoile.remove(etoile)

def boost_augmentation(boost):
    if (pyxel.frame_count % 3 == 0 or pyxel.frame_count % 3 == 1) and boost_activated == True and boost > 0:
        boost -= 1
    if pyxel.frame_count % 10 == 0 and boost < 100 and boost_activated == False:
        boost += 1
    return boost

def boost_on(speed_vaisseau, boost_activated):
    if boost == 100 and pyxel.btn(pyxel.KEY_B):
        speed_vaisseau = 2.5
        boost_activated = True
    elif boost == 0:
        speed_vaisseau = 1.5
        boost_activated = False
    return speed_vaisseau, boost_activated

def update():
    global vaisseau_x, vaisseau_y, vies, score, liste_tirs, liste_explosions, liste_ennemis, liste_vies, munitions, liste_tirs_ennemis, proba_tir_ennemis, liste_etoile, played, commandes, bestscore, boost, speed_vaisseau, boost_activated

    if vies > 0:
        # LE VAISSEAU
        # On appelle pour deplacer le vaisseau
        vaisseau_x, vaisseau_y = vaisseau_deplacement(vaisseau_x, vaisseau_y)

        # LES TIRS DU VAISSEAU
        # On appelle pour la création de tirs
        munitions = tirs_creation(vaisseau_x, vaisseau_y, liste_tirs, munitions)
        # On fait deplacer les tirs
        tirs_deplacement(liste_tirs)

        # LES ENNEMIS
        # On appelle pour la création des ennemis
        ennemis_creation(liste_ennemis)
        # On fait deplacer les ennemis
        vies = ennemis_deplacement(liste_ennemis, vies)

        # LE JEU
        # Si un ennemi touche le vaisseau
        vies = vaisseau_suppression(vies)
        # Si un tir touche un ennemi
        score, munitions = ennemis_suppression(liste_ennemis, liste_tirs, score, munitions)
        # L'animation des explosions
        explosions_creation()

        # LES VIES
        # Vie creation
        score, proba_tir_ennemis = vie_creation(vies, score, liste_vies, proba_tir_ennemis)
        # Vies deplacement
        vie_deplacement(liste_vies)
        # Si le vaissseau touche une vie
        vies = vie_colision(liste_vies, vies)

        # LES TIRES ENNEMIS
        # tirs creation
        ennemis_tirs_creation(liste_ennemis, liste_tirs_ennemis)
        # les tirs de l'ennemi se deplacent
        ennemis_tirs_deplacement(liste_tirs_ennemis)
        # si les tirs se touchent entre eux
        tirs_colisions(liste_tirs_ennemis)

        # LES ETOILES - DECOR
        # on creer les etoiles
        etoiles(liste_etoile)
        # les etoiles bougent
        etoile_deplacement(liste_etoile)

        # BOOST
        # On augmente le boost 
        boost = boost_augmentation(boost)
        # si le boost est activé
        speed_vaisseau, boost_activated = boost_on(speed_vaisseau, boost_activated)


    else:
        if score > bestscore:
            bestscore = score
            
        if pyxel.btn(pyxel.KEY_RETURN):
            commandes = False
            played = True
            score = 0
            vies = 3
            munitions = 5
            vaisseau_x, vaisseau_y = 60,60
            proba_tir_ennemis = 200
            boost = 0
            boost_activated = False
            liste_ennemis = []
            liste_tirs = []
            liste_explosions = []
            liste_etoile = []
            liste_vies = []
            liste_tirs_ennemis = []

        if pyxel.btn(pyxel.KEY_C):
            commandes = True

        if pyxel.btn(pyxel.KEY_R):
            commandes = False

def draw():
    # On efface tout
    pyxel.cls(0)
    if vies > 0:
        # On fait bouger les etoiles
        for etoile in liste_etoile:
            pyxel.rect(etoile[0], etoile[1], 1, 1, 6)
        # On dessine les tirs
        for tir in liste_tirs:
            pyxel.blt(tir[0], tir[1], 0, 10, 4, 4, 4)
        # On dessine les tirs ennemis
        for tir in liste_tirs_ennemis:
            pyxel.blt(tir[0], tir[1], 0, 10, 8, 4, 4)
        # On dessine le score
        pyxel.text(3, 12, f"SCORE: {score}", 7)
        # On dessine les explosions
        for explosion in liste_explosions:
            pyxel.circb(explosion[0], explosion[1], explosion[2], 8+explosion[2]%3)
        # On dessine le vaisseau
        pyxel.blt(vaisseau_x, vaisseau_y,0, 0, 0, 8, 8)
        # On dessine les ennemis
        for ennemi in liste_ennemis:
            pyxel.blt(ennemi[0], ennemi[1],0,0, 8, 8, 8)
        # On dessine les vies qui tombent
        for vie in liste_vies:
            pyxel.blt(vie[0], vie[1],0, 80, 48, 8, 8)
        # On dessine les vies
        pyxel.blt(5, 0, 0, 96, 48, 8, 8)
        pyxel.blt(15, 0, 0, 96, 48, 8, 8)
        pyxel.blt(25, 0, 0, 96, 48, 8, 8)
        if vies == 3:
            pyxel.blt(5, 0, 0, 80, 48, 8, 8)
            pyxel.blt(15, 0, 0, 80, 48, 8, 8)
            pyxel.blt(25, 0, 0, 80, 48, 8, 8)
        elif vies == 2:
            pyxel.blt(5, 0, 0, 80, 48, 8, 8)
            pyxel.blt(15, 0, 0, 80, 48, 8, 8)
        elif vies ==1 :
            pyxel.blt(5, 0, 0, 80, 48, 8, 8)

        # On dessine le nombre de munitions
        pyxel.blt(123, 5.5, 0, 10, 4, 4, 4)
        pyxel.text(115, 5, f"{munitions}", 7)
        # On dessine le boost
        if boost < 10:
            boost_aff = '  ' + str(boost) + '%'
        elif boost < 100:
            boost_aff = ' ' + str(boost) + '%'
        else:
            boost_aff = str(boost) + '%'
        pyxel.text(111, 13, boost_aff, 7)

    else:
        if commandes == True:
            pyxel.text(45,18, "COMMANDES", 7)
            pyxel.text(7,30, "'ESPACE'  : tirer", 7)
            pyxel.text(7,38, "'FLECHES' : bouger le vaisseau", 7)
            pyxel.text(7,46, "'B' : boost (quand 100%)", 7)
            pyxel.text(7,58, "1 ennemi abbatu = +1 point", 7)
            pyxel.text(7,66, "1 ennemi abbatu = +2 munitions", 7)
            pyxel.text(7,74, "10 points = une vie qui tombe", 7)
            pyxel.text(25,98, "'r' page precedente", 7)

        elif played == False:
            pyxel.text(12,30, "Bienvenue sur Space Invader", 7)
            pyxel.text(7,50, "Votre but est d'eliminer tous", 7)
            pyxel.text(7,58, "les vaisseaux ennemis avant", 7)
            pyxel.text(7,66, "qu'ils ne franchissent le bas", 7)
            pyxel.text(7,74, "de l'ecran.", 7)
            pyxel.text(20,98, "'c' pour les commandes", 7)

        else:
            pyxel.text(45,40, "GAME OVER", 7)
            pyxel.text(45,60, f"SCORE : {score}", 7)
            pyxel.text(39,68, f"BESTSCORE : {bestscore}", 7)
            pyxel.text(20,98, "'c' pour les commandes", 7)
        
        pyxel.text(25,90, "'ENTRER' pour jouer", 7)

pyxel.run(update, draw)