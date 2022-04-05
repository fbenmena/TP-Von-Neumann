# On représente la mémoire à l'aide d'un dictionnaire dont les clés sont les adresses (sur 16 bits)
# et les valeurs sont des entiers (sur 16 bits) représentées par des chaines de caractères qui donnent
# leur valeur en hexadécimal.

TAILLE_ARCHITECTURE = 2**16

memoire = {}

registres = {
    "R1": "0x0000",
    "R2": "0x0000",
    "R3": "0x0000",
    "R4": "0x0000",
    "PC": "0x0000",    # Le registre ordinal PC, qui contient l'adresse de la prochaine instruction à exécuter.
    "IR": "0x0000",    # Le registre d'instruction qui contient le code binaire de l'instruction en cours d'exécution.
    "SP": "0x0000",    # Le registre qui contient l'adresse du la pile.
    "DRAPEAU_NUL" : 0, # Le dernier calcul a produit un résultat nul.
    "DRAPEAU_NEG" : 0, # Le dernier calcul a produit un résultat négatif (strictement).
    "DRAPEAU_DEB" : 0, # Le dernier calcul a produit un résultat avec débordement (overflow).
    "DRAPEAU_CMP" : 0, # Le dernier calcul a consisté en une comparaison.
}


def initialiser_memoire(memoire):
    memoire.clear()


def initialiser_drapeaux(registres):
    registres["DRAPEAU_NUL"] = 0
    registres["DRAPEAU_NEG"] = 0
    registres["DRAPEAU_DEB"] = 0
    registres["DRAPEAU_CMP"] = 0


def initialiser_registres(registres):
    registres["R1"] = "0x0000"
    registres["R2"] = "0x0000"
    registres["R3"] = "0x0000"
    registres["R4"] = "0x0000"
    registres["PC"] = "0x0000"
    registres["IR"] = "0x0000"
    registres["SP"] = "0x0000"
    initialiser_drapeaux(registres)


def format_hex(entier):
    assert isinstance(entier, int) and entier >= 0 and entier < TAILLE_ARCHITECTURE
    return "0x" + format(entier, "04x")


def convertir_en_entier(chaine):
    assert isinstance(chaine, str) and (3 <= len(chaine) <= 6) and chaine.startswith("0x")
    chaine = chaine.lower()
    assert all(caractere in "0123456789abcdef" for caractere in chaine[2:])
    return int(chaine, base=16)


def lecture_memoire(memoire, adresse):
    assert isinstance(memoire, dict)
    # On doit s'assurer que le format de l'adresse est "normalisé".
    adresse = format_hex(convertir_en_entier(adresse))

    if adresse in memoire:
        return memoire[adresse]
    else:
        return "0x0000"


def ecriture_memoire(memoire, adresse, valeur):
    assert isinstance(memoire, dict)
    # On doit s'assurer que le format de l'adresse est "normalisé".
    adresse = format_hex(convertir_en_entier(adresse))

    # On doit s'assurer que le format de la valeur est "normalisé".
    valeur = format_hex(convertir_en_entier(valeur))

    memoire[adresse] = valeur


def affiche_memoire(memoire, limite=32):
    compteur = 0
    for adresse, valeur in memoire.items():
        compteur = compteur + 1
        if compteur <= limite:
            print(adresse, ":", valeur)


def dechiffrer_instruction(instruction):
    assert isinstance(instruction, str)
    mnemoniques = ["LOAD", "STORE", "MOVE", "ADD", "SUB", "AND", "OR", "XOR", "NOT",
                   "CMP", "EQ", "NE", "GT", "LT", "B", "HALT"]

    mnemonique_instruction = ""
    for m in mnemoniques:
        if instruction.startswith(m):
            mnemonique_instruction = m
    assert len(m) > 0

    operandes = instruction.replace(mnemonique_instruction, "")
    operandes = [op.strip() for op in operandes.split(",")]
    return mnemonique_instruction, operandes


def executer_instruction(mnemonique_instruction, operandes):
    if mnemonique_instruction == "LOAD":
        executer_instruction_LOAD(operandes, memoire, registres)
    elif mnemonique_instruction == "STORE":
        executer_instruction_STORE(operandes, memoire, registres)
    elif mnemonique_instruction == "MOVE":
        executer_instruction_MOVE(operandes, registres)
    elif mnemonique_instruction == "ADD":
        executer_instruction_ADD(operandes, registres)
    elif mnemonique_instruction == "SUB":
        executer_instruction_SUB(operandes, registres)
    elif mnemonique_instruction == "AND":
        executer_instruction_AND(operandes, registres)
    elif mnemonique_instruction == "OR":
        executer_instruction_OR(operandes, registres)
    elif mnemonique_instruction == "XOR":
        executer_instruction_XOR(operandes, registres)
    elif mnemonique_instruction == "NOT":
        executer_instruction_NOT(operandes, registres)
    elif mnemonique_instruction == "CMP":
        executer_instruction_CMP(operandes, registres)
    elif mnemonique_instruction == "EQ":
        executer_instruction_EQ(operandes, registres)
    elif mnemonique_instruction == "NE":
        executer_instruction_NE(operandes, registres)
    elif mnemonique_instruction == "GT":
        executer_instruction_GT(operandes, registres)
    elif mnemonique_instruction == "LT":
        executer_instruction_LT(operandes, registres)
    elif mnemonique_instruction == "B":
        executer_instruction_B(operandes, registres)
    elif mnemonique_instruction == "HALT":
        executer_instruction_HALT(operandes, registres)
    else:
        assert False


def executer_instruction_LOAD(operandes, memoire, registres):
    assert len(operandes) == 2
    op1, op2 = operandes

    assert op1 in ["R1", "R2", "R3", "R4"]
    assert isinstance(op2, str)
    crochet_gauche, crochet_droite = "[", "]"

    if (3 <= len(op2) <= 6) and op2.startswith("0x"):
        adresse = format_hex(convertir_en_entier(op2))

    elif op2.startswith(crochet_gauche) and op2.endswith(crochet_droite):
        op2 = op2.replace(crochet_gauche, "").replace(crochet_droite, "").strip()
        adresse_indirecte = format_hex(convertir_en_entier(op2))
        adresse = lecture_memoire(memoire, adresse_indirecte)

    else:
        assert False

    registres[op1] = lecture_memoire(memoire, adresse)


def executer_instruction_STORE(operandes, memoire, registres):
    assert len(operandes) == 2
    op1, op2 = operandes

    assert op1 in ["R1", "R2", "R3", "R4"]
    assert isinstance(op2, str)
    crochet_gauche, crochet_droite = "[", "]"

    if (3 <= len(op2) <= 6) and op2.startswith("0x"):
        adresse = format_hex(convertir_en_entier(op2))

    elif op2.startswith(crochet_gauche) and op2.endswith(crochet_droite):
        op2 = op2.replace(crochet_gauche, "").replace(crochet_droite, "").strip()
        adresse_indirecte = format_hex(convertir_en_entier(op2))
        adresse = lecture_memoire(memoire, adresse_indirecte)

    else:
        assert False

    ecriture_memoire(memoire, adresse, registres[op1])


def executer_instruction_MOVE(operandes, registres):
    assert len(operandes) == 2
    op1, op2 = operandes

    assert op1 in ["R1", "R2", "R3", "R4"] and isinstance(op2, str)

    if op2 in ["R1", "R2", "R3", "R4"]:
        registres[op1] = registres[op2]

    elif (3 <= len(op2) <= 6) and op2.startswith("0x"):
        op2 = format_hex(convertir_en_entier(op2))
        registres[op1] = op2

    else:
        assert False


def executer_instruction_ADD(operandes, registres):
    assert len(operandes) == 3
    op1, op2, op3 = operandes

    assert op1 in ["R1", "R2", "R3", "R4"]
    assert op2 in ["R1", "R2", "R3", "R4"]
    assert op3 in ["R1", "R2", "R3", "R4"]
    entier_1 = convertir_en_entier(registres[op2])
    entier_2 = convertir_en_entier(registres[op3])

    retenue = False
    somme = entier_1 + entier_2
    if somme >= TAILLE_ARCHITECTURE:
        somme = somme - TAILLE_ARCHITECTURE
        retenue = True

    resultat = format_hex(somme)
    registres[op1] = resultat

    initialiser_drapeaux(registres)
    if resultat == "0x0000":
        registres["DRAPEAU_NUL"] = 1
    if retenue == True:
        registres["DRAPEAU_DEB"] = 1


def executer_instruction_SUB(operandes, registres):
    assert len(operandes) == 3
    op1, op2, op3 = operandes

    assert op1 in ["R1", "R2", "R3", "R4"]
    assert op2 in ["R1", "R2", "R3", "R4"]
    assert op3 in ["R1", "R2", "R3", "R4"]
    entier_1 = convertir_en_entier(registres[op2])
    entier_2 = convertir_en_entier(registres[op3])

    negatif = False
    difference = entier_1 - entier_2
    if difference < 0:
        difference = -difference
        negatif = True

    resultat = format_hex(difference)
    registres[op1] = resultat

    initialiser_drapeaux(registres)
    if resultat == "0x0000":
        registres["DRAPEAU_NUL"] = 1
    if negatif == True:
        registres["DRAPEAU_NEG"] = 1


def executer_instruction_AND(operandes, registres):
    assert len(operandes) == 3
    op1, op2, op3 = operandes

    assert op1 in ["R1", "R2", "R3", "R4"]
    assert op2 in ["R1", "R2", "R3", "R4"]
    assert op3 in ["R1", "R2", "R3", "R4"]
    entier_1 = convertir_en_entier(registres[op2])
    entier_2 = convertir_en_entier(registres[op3])

    et_logique = entier_1 & entier_2
    resultat = format_hex(et_logique)
    registres[op1] = resultat


def executer_instruction_OR(operandes, registres):
    assert len(operandes) == 3
    op1, op2, op3 = operandes

    assert op1 in ["R1", "R2", "R3", "R4"]
    assert op2 in ["R1", "R2", "R3", "R4"]
    assert op3 in ["R1", "R2", "R3", "R4"]
    entier_1 = convertir_en_entier(registres[op2])
    entier_2 = convertir_en_entier(registres[op3])

    ou_logique = entier_1 | entier_2
    resultat = format_hex(ou_logique)
    registres[op1] = resultat


def executer_instruction_XOR(operandes, registres):
    assert len(operandes) == 3
    op1, op2, op3 = operandes

    assert op1 in ["R1", "R2", "R3", "R4"]
    assert op2 in ["R1", "R2", "R3", "R4"]
    assert op3 in ["R1", "R2", "R3", "R4"]
    entier_1 = convertir_en_entier(registres[op2])
    entier_2 = convertir_en_entier(registres[op3])

    ou_exclusif = entier_1 ^ entier_2
    resultat = format_hex(ou_exclusif)
    registres[op1] = resultat


def executer_instruction_NOT(operandes, registres):
    assert len(operandes) == 2
    op1, op2 = operandes

    assert op1 in ["R1", "R2", "R3", "R4"]
    assert op2 in ["R1", "R2", "R3", "R4"]
    entier_1 = convertir_en_entier(registres[op2])

    complement = TAILLE_ARCHITECTURE - 1 - entier_1
    resultat = format_hex(complement)
    registres[op1] = resultat


def executer_instruction_CMP(operandes, registres):
    assert len(operandes) == 2
    op1, op2 = operandes

    if op1 in ["R1", "R2", "R3", "R4"]:
        entier_1 = convertir_en_entier(registres[op1])
    elif isinstance(op1, str) and (3 <= len(op1) <= 6) and op1.startswith("0x"):
        entier_1 = convertir_en_entier(op1)
    else:
        assert False

    if op2 in ["R1", "R2", "R3", "R4"]:
        entier_2 = convertir_en_entier(registres[op2])
    elif isinstance(op2, str) and (3 <= len(op2) <= 6) and op2.startswith("0x"):
        entier_2 = convertir_en_entier(op2)
    else:
        assert False

    initialiser_drapeaux(registres)
    if entier_1 == entier_2:
        registres["DRAPEAU_CMP"] = "EQ"
    elif entier_1 < entier_2:
        registres["DRAPEAU_CMP"] = "LT"
    else:
        registres["DRAPEAU_CMP"] = "GT"


def executer_instruction_EQ(operandes, memoire, registres):
    assert len(operandes) == 1
    op1 = operandes[0]

    if not(isinstance(op1, str) and (3 <= len(op1) <= 6) and op1.startswith("0x")):
        assert False

    if registres["DRAPEAU_CMP"] == "EQ":
        adresse_saut = format_hex(convertir_en_entier(op1))
        adresse_pile = format_hex(int(registres["SP"], base=16) + 1)
        ecriture_memoire(memoire, adresse_pile, registres["PC"])
        registres["SP"] = adresse_pile
        registres["PC"] = adresse_saut


def executer_instruction_NE(operandes, memoire, registres):
    assert len(operandes) == 1
    op1 = operandes[0]

    if not(isinstance(op1, str) and (3 <= len(op1) <= 6) and op1.startswith("0x")):
        assert False

    if (registres["DRAPEAU_CMP"] == "LT") or (registres["DRAPEAU_CMP"] == "GT"):
        adresse_saut = format_hex(convertir_en_entier(op1))
        adresse_pile = format_hex(int(registres["SP"], base=16) + 1)
        ecriture_memoire(memoire, adresse_pile, registres["PC"])
        registres["SP"] = adresse_pile
        registres["PC"] = adresse_saut


def executer_instruction_GT(operandes, memoire, registres):
    assert len(operandes) == 1
    op1 = operandes[0]

    if not(isinstance(op1, str) and (3 <= len(op1) <= 6) and op1.startswith("0x")):
        assert False

    if registres["DRAPEAU_CMP"] == "GT":
        adresse_saut = format_hex(convertir_en_entier(op1))
        adresse_pile = format_hex(int(registres["SP"], base=16) + 1)
        ecriture_memoire(memoire, adresse_pile, registres["PC"])
        registres["SP"] = adresse_pile
        registres["PC"] = adresse_saut


def executer_instruction_LT(operandes, memoire, registres):
    assert len(operandes) == 1
    op1 = operandes[0]

    if not(isinstance(op1, str) and (3 <= len(op1) <= 6) and op1.startswith("0x")):
        assert False

    if registres["DRAPEAU_CMP"] == "LT":
        adresse_saut = format_hex(convertir_en_entier(op1))
        adresse_pile = format_hex(int(registres["SP"], base=16) + 1)
        ecriture_memoire(memoire, adresse_pile, registres["PC"])
        registres["SP"] = adresse_pile
        registres["PC"] = adresse_saut


def executer_instruction_B(operandes, memoire, registres):
    assert len(operandes) == 1
    op1 = operandes[0]

    adresse_saut = format_hex(convertir_en_entier(op1))
    adresse_pile = format_hex(int(registres["SP"], base=16) + 1)
    ecriture_memoire(memoire, adresse_pile, registres["PC"])
    registres["SP"] = adresse_pile
    registres["PC"] = adresse_saut


def executer_instruction_HALT(operandes, memoire, registres):
    assert len(operandes) == 0
    adresse_pile = int(registres["SP"], base=16)
    assert adresse_pile > 0

    registres["PC"] = lecture_memoire(memoire, registres["SP"])
    registres["SP"] = format_hex(adresse_pile - 1)
