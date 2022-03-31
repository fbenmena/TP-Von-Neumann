# on représente la mémoire à l'aide d'un dictionnaire dont les clés sont les adresses (sur 16 bits)
# et les valeurs sont des entiers (sur 16 bits) représentées par des chaines de caractères qui donnent
# leur valeur en hexadécimal.

memoire = {}
registres = {
    "R1": "0x0000",
    "R2": "0x0000",
    "R3": "0x0000",
    "R4": "0x0000",
    "PC": "0x0000",
    "IR": "0x0000",
    "SP": "0x0000",
}


def initialiser_registres(registres):
    registres = {
        "R1": "0x0000",
        "R2": "0x0000",
        "R3": "0x0000",
        "R4": "0x0000",
        "PC": "0x0000",
        "IR": "0x0000",
        "SP": "0x0000",
    }

def format_hex(entier):
    assert isinstance(entier, int) and entier >= 0 and entier < 2**16
    return "0x" + format(entier, "04x")


def lecture_memoire(memoire, adresse):
    assert isinstance(memoire, dict)
    assert isinstance(adresse, str) and len(adresse) == 6 and adresse.startswith("0x")
    adresse = adresse.lower()
    if adresse in memoire:
        return memoire[adresse]
    else:
        return "0x0000"


def ecriture_memoire(memoire, adresse, valeur):
    assert isinstance(memoire, dict)
    assert isinstance(adresse, str) and len(adresse) == 6 and adresse.startswith("0x")
    assert isinstance(valeur, str) and len(valeur) == 6 and valeur.startswith("0x")
    adresse = adresse.lower()
    valeur = valeur.lower()
    assert format_hex(int(adresse, base=16)) == adresse
    assert format_hex(int(valeur, base=16)) == valeur
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

    if len(op2) == 6 and op2.startswith("0x"):
        adresse = op2
    elif op2.startswith(crochet_gauche) and op2.endswith(crochet_droite):
        adresse_indirecte = op2.replace(crochet_gauche, "").replace(crochet_droite, "").strip()
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

    if len(op2) == 6 and op2.startswith("0x"):
        adresse = op2
    elif op2.startswith(crochet_gauche) and op2.endswith(crochet_droite):
        adresse_indirecte = op2.replace(crochet_gauche, "").replace(crochet_droite, "").strip()
        adresse = lecture_memoire(memoire, adresse_indirecte)
    else:
        assert False

    ecriture_memoire(memoire, adresse, registres[op1])


def executer_instruction_MOVE(operandes, registres):
    assert len(operandes) == 2
    op1, op2 = operandes

    assert op1 in ["R1", "R2", "R3", "R4"]
    if op2 in ["R1", "R2", "R3", "R4"]:
        registres[op1] = registres[op2]
    elif isinstance(op2, str) and len(op2) == 6 and op2.startswith("0x"):
        op2 = op2.lower()
        assert format_hex(int(op2, base=16)) == op2
        registres[op1] = op2


def executer_instruction_ADD(operandes, registres):
    assert len(operandes) == 3
    op1, op2, op3 = operandes

    assert op1 in ["R1", "R2", "R3", "R4"]
    assert op2 in ["R1", "R2", "R3", "R4"]
    assert op3 in ["R1", "R2", "R3", "R4"]
    entier_1 = int(registres[op2], base=16)
    entier_2 = int(registres[op3], base=16)

    retenue = False
    somme = entier_1 + entier_2
    if somme >= 2**16:
        somme = somme - 2**16
        retenue = True

    resultat = format_hex(somme)
    registres[op1] = resultat

    # Il faut également modifier le registre drapeaux si le résultat est nul ou si
    # la retenue est positionnée à `True`.  Il faut également tester si la somme est
    # nulle.


def executer_instruction_SUB(operandes, registres):
    assert len(operandes) == 3
    op1, op2, op3 = operandes

    assert op1 in ["R1", "R2", "R3", "R4"]
    assert op2 in ["R1", "R2", "R3", "R4"]
    assert op3 in ["R1", "R2", "R3", "R4"]
    entier_1 = int(registres[op2], base=16)
    entier_2 = int(registres[op3], base=16)

    negatif = False
    difference = entier_1 - entier_2
    if difference < 0:
        difference = -difference
        negatif = True

    resultat = format_hex(difference)
    registres[op1] = resultat

    # Il faut également modifier le registre drapeaux si le résultat est nul ou si
    # la variable `négatif` est positionnée à `True`.


def executer_instruction_AND(operandes, registres):
    assert len(operandes) == 3
    op1, op2, op3 = operandes

    assert op1 in ["R1", "R2", "R3", "R4"]
    assert op2 in ["R1", "R2", "R3", "R4"]
    assert op3 in ["R1", "R2", "R3", "R4"]
    entier_1 = int(registres[op2], base=16)
    entier_2 = int(registres[op3], base=16)

    et_logique = entier_2 & entier_3
    resultat = format_hex(et_logique)

    # Il faut également modifier le registre drapeaux si le résultat est nul.


def executer_instruction_OR(operandes, registres):
    assert len(operandes) == 3
    op1, op2, op3 = operandes

    assert op1 in ["R1", "R2", "R3", "R4"]
    assert op2 in ["R1", "R2", "R3", "R4"]
    assert op3 in ["R1", "R2", "R3", "R4"]
    entier_1 = int(registres[op2], base=16)
    entier_2 = int(registres[op3], base=16)

    ou_logique = entier_2 | entier_3
    resultat = format_hex(ou_logique)
    registres[op1] = resultat

    # Il faut également modifier le registre drapeaux si le résultat est nul.


def executer_instruction_XOR(operandes, registres):
    assert len(operandes) == 3
    op1, op2, op3 = operandes

    assert op1 in ["R1", "R2", "R3", "R4"]
    assert op2 in ["R1", "R2", "R3", "R4"]
    assert op3 in ["R1", "R2", "R3", "R4"]
    entier_1 = int(registres[op2], base=16)
    entier_2 = int(registres[op3], base=16)

    ou_exclusif = entier_2 ^ entier_3
    resultat = format_hex(ou_exclusif)
    registres[op1] = resultat

    # Il faut également modifier le registre drapeaux si le résultat est nul.


def executer_instruction_NOT(operandes, registres):
    assert len(operandes) == 2
    op1, op2 = operandes

    assert op1 in ["R1", "R2", "R3", "R4"]
    assert op2 in ["R1", "R2", "R3", "R4"]

    entier_1 = int(registres[op2], base=16)
    complement = 2**16 - 1 - entier_1
    resultat = format_hex(complement)
    registres[op1] = resultat

    # Il faut également modifier le registre drapeaux si le résultat est nul.


def executer_instruction_CMP(operandes, registres):
    assert len(operandes) == 2
    op1, op2 = operandes

    if op1 in ["R1", "R2", "R3", "R4"]:
        entier_1 = int(registres[op1], base=16)
    elif isinstance(op1, str) and len(op1) == 6 and op1.startswith("0x"):
        op1 = op1.lower()
        assert format_hex(int(op1, base=16)) == op1
        entier_1 = int(op1, base=16)
    else:
        assert False

    if op2 in ["R1", "R2", "R3", "R4"]:
        entier_2 = int(registres[op2], base=16)
    elif isinstance(op2, str) and len(op2) == 6 and op2.startswith("0x"):
        op2 = op2.lower()
        assert format_hex(int(op2, base=16)) == op2
        entier_2 = int(op2, base=16)
    else:
        assert False

    # Il faut également modifier le registre drapeaux pour tenir compte des informations
    # suivantes: les entiers sont égaux, l'`entier_1` est strictement supérieur à l'`entier_2`
    # ou si, inversement, l'`entier_1` est strictement inférieur à l'`entier_2`.



def executer_instruction_EQ(operandes, memoire, registres):
    assert len(operandes) == 1
    op1 = operandes[0]

    if not(isinstance(op1, str) and len(op1) == 6 and op1.startswith("0x")):
        assert False

    if registres["Drapeau_EQ"]:
        op1 = op1.lower()
        assert format_hex(int(op1, base=16)) == op1
        adressse = registres["SP"]
        adresse_suivante = format_hex(int(adressse, base=16) + 1)
        ecriture_memoire(memoire, adresse_suivante, registres["PC"])
        registres["SP"] = adresse_suivante
        registres["PC"] = op1


def executer_instruction_NE(operandes, memoire, registres):
    assert len(operandes) == 1
    op1 = operandes[0]

    if not(isinstance(op1, str) and len(op1) == 6 and op1.startswith("0x")):
        assert False

    if registres["Drapeau_NE"]:
        op1 = op1.lower()
        assert format_hex(int(op1, base=16)) == op1
        adressse = registres["SP"]
        adresse_suivante = format_hex(int(adressse, base=16) + 1)
        ecriture_memoire(memoire, adresse_suivante, registres["PC"])
        registres["SP"] = adresse_suivante
        registres["PC"] = op1


def executer_instruction_GT(operandes, memoire, registres):
    assert len(operandes) == 1
    op1 = operandes[0]

    if not(isinstance(op1, str) and len(op1) == 6 and op1.startswith("0x")):
        assert False

    if registres["Drapeau_GT"]:
        op1 = op1.lower()
        assert format_hex(int(op1, base=16)) == op1
        adressse = registres["SP"]
        adresse_suivante = format_hex(int(adressse, base=16) + 1)
        ecriture_memoire(memoire, adresse_suivante, registres["PC"])
        registres["SP"] = adresse_suivante
        registres["PC"] = op1


def executer_instruction_LT(operandes, memoire, registres):
    assert len(operandes) == 1
    op1 = operandes[0]

    if not(isinstance(op1, str) and len(op1) == 6 and op1.startswith("0x")):
        assert False

    if registres["Drapeau_LT"]:
        op1 = op1.lower()
        assert format_hex(int(op1, base=16)) == op1
        adressse = registres["SP"]
        adresse_suivante = format_hex(int(adressse, base=16) + 1)
        ecriture_memoire(memoire, adresse_suivante, registres["PC"])
        registres["SP"] = adresse_suivante
        registres["PC"] = op1


def executer_instruction_B(operandes, memoire, registres):
    assert len(operandes) == 1
    op1 = operandes[0]

    if not(isinstance(op1, str) and len(op1) == 6 and op1.startswith("0x")):
        assert False

    op1 = op1.lower()
    assert format_hex(int(op1, base=16)) == op1
    adressse = registres["SP"]
    adresse_suivante = format_hex(int(adressse, base=16) + 1)
    ecriture_memoire(memoire, adresse_suivante, registres["PC"])
    registres["SP"] = adresse_suivante
    registres["PC"] = op1


def executer_instruction_HALT(operandes, memoire, registres):
    assert len(operandes) == 0

    # à terminer...
