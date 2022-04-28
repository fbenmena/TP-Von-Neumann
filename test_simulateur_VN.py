from simulateur_VN import (memoire,
                           registres,
                           initialiser_memoire,
                           lecture_memoire,
                           ecriture_memoire,
                           executer_instruction_LOAD,
                           executer_instruction_STORE,
                           executer_instruction_MOVE,
                           executer_instruction_ADD,
                           executer_instruction_SUB,
                           executer_instruction_ADD_SIGNED,
                           executer_instruction_SUB_SIGNED,
                           executer_instruction_MUL,
                           executer_instruction_AND,
                           executer_instruction_OR,
                           executer_instruction_XOR,
                           executer_instruction_NOT,
                           executer_instruction_CMP,
                           executer_instruction_EQ,
                           executer_instruction_NE,
                           executer_instruction_GT,
                           executer_instruction_LT,
                           executer_instruction_B,
                           executer_instruction_HALT,
                           )


import pytest


def test_memoire_lecture_ecriture():
    ecriture_memoire(memoire, "0x3000", "0xAA00")
    ecriture_memoire(memoire, "0x3001", "0xAABB")
    ecriture_memoire(memoire, "0x3002", "0xAACC")
    assert lecture_memoire(memoire, "0x3000") == "0xaa00" # Subtil!
    assert lecture_memoire(memoire, "0x3001") == "0xaabb" # Subtil!
    assert lecture_memoire(memoire, "0x3002") == "0xaacc" # Subtil!


def test_memoire_initialisation():
    ecriture_memoire(memoire, "0x3000", "0xAA00")
    initialiser_memoire(memoire)
    assert memoire == {}


def test_instruction_LOAD():
    ecriture_memoire(memoire, "0x3000", "0xAA00")
    executer_instruction_LOAD(["R1", "0x3000"], memoire, registres)
    assert registres["R1"] == "0xaa00" # Subtil!

def test_instruction_STORE():
    registres["R1"] = "0xbb00"
    executer_instruction_STORE(["R1", "0x3000"], memoire, registres)
    assert lecture_memoire(memoire, "0x3000") == "0xbb00"


def test_instruction_MOVE():
    registres["R1"] = "0xbb00"
    executer_instruction_MOVE(["R2", "R1"], registres)
    assert registres["R1"] == registres["R2"]


def test_instruction_ADD_cas_1():
    registres["R1"] = "0xbb00"
    registres["R2"] = "0x0001"
    executer_instruction_ADD(["R1", "R1", "R2"], registres)
    assert registres["R1"] == "0xbb01"
    assert registres["DRAPEAU_NUL"] == 0
    assert registres["DRAPEAU_NEG"] == 0
    assert registres["DRAPEAU_DEB"] == 0


def test_instruction_ADD_cas_2():
    registres["R1"] = "0x0000"
    registres["R2"] = "0x0000"
    executer_instruction_ADD(["R1", "R1", "R2"], registres)
    assert registres["R1"] == "0x0000"
    assert registres["DRAPEAU_NUL"] == 1
    assert registres["DRAPEAU_NEG"] == 0
    assert registres["DRAPEAU_DEB"] == 0


def test_instruction_ADD_cas_3():
    registres["R1"] = "0xff00"
    registres["R2"] = "0x0100"
    executer_instruction_ADD(["R1", "R1", "R2"], registres)
    assert registres["R1"] == "0x0000"
    assert registres["DRAPEAU_NUL"] == 1
    assert registres["DRAPEAU_NEG"] == 0
    assert registres["DRAPEAU_DEB"] == 1


def test_instruction_ADD_cas_4():
    registres["R1"] = "0xff00"
    registres["R2"] = "0x0111"
    executer_instruction_ADD(["R1", "R1", "R2"], registres)
    assert registres["R1"] == "0x0011"
    assert registres["DRAPEAU_NUL"] == 0
    assert registres["DRAPEAU_NEG"] == 0
    assert registres["DRAPEAU_DEB"] == 1


def test_instruction_ADD_cas_5():
    registres["R1"] = "0xff00"
    executer_instruction_ADD(["R1", "R1", "0x00ff"], registres)
    assert registres["R1"] == "0xffff"
    assert registres["DRAPEAU_NUL"] == 0
    assert registres["DRAPEAU_NEG"] == 0
    assert registres["DRAPEAU_DEB"] == 0


def test_instruction_SUB_cas_1():
    registres["R1"] = "0xbb00"
    registres["R2"] = "0x0001"
    executer_instruction_SUB(["R1", "R1", "R2"], registres)
    assert registres["R1"] == "0xbaff"
    assert registres["DRAPEAU_NUL"] == 0
    assert registres["DRAPEAU_NEG"] == 0
    assert registres["DRAPEAU_DEB"] == 0


def test_instruction_SUB_cas_2():
    registres["R1"] = "0xbb00"
    registres["R2"] = "0xbb00"
    executer_instruction_SUB(["R1", "R1", "R2"], registres)
    assert registres["R1"] == "0x0000"
    assert registres["DRAPEAU_NUL"] == 1
    assert registres["DRAPEAU_NEG"] == 0
    assert registres["DRAPEAU_DEB"] == 0


def test_instruction_SUB_cas_3():
    registres["R1"] = "0xbb00"
    registres["R2"] = "0xbb01"
    executer_instruction_SUB(["R1", "R1", "R2"], registres)
    assert registres["R1"] == "0x0001"
    assert registres["DRAPEAU_NUL"] == 0
    assert registres["DRAPEAU_NEG"] == 1
    assert registres["DRAPEAU_DEB"] == 0


def test_instruction_SUB_cas_4():
    registres["R1"] = "0xbb00"
    executer_instruction_SUB(["R1", "R1", "0x0001"], registres)
    assert registres["R1"] == "0xbaff"
    assert registres["DRAPEAU_NUL"] == 0
    assert registres["DRAPEAU_NEG"] == 0
    assert registres["DRAPEAU_DEB"] == 0


def test_instruction_ADD_SIGNED_cas_1():
    registres["R1"] = "0x0064"  # En décimal signé, cet entier est égal à: 6*16 + 4 = 100
    registres["R2"] = "0xff9c"  # En décimal signé, cet entier est négatif, sa valeur est obtenue par la
                                # méthode du complément à 2**16, cela donne 65436 - 2**16 = -100.
    executer_instruction_ADD_SIGNED(["R1", "R1", "R2"], registres)
    assert registres["R1"] == "0x0000" # En décimal signé, cet entier est égal à 0.
    assert registres["DRAPEAU_NUL"] == 1
    assert registres["DRAPEAU_NEG"] == 0
    assert registres["DRAPEAU_DEB"] == 0


def test_instruction_ADD_SIGNED_cas_2():
    registres["R1"] = "0x0065"  # En décimal signé, cet entier est égal à: 6*16 + 5 = 101
    registres["R2"] = "0xff9c"  # En décimal signé, cet entier est négatif, sa valeur est obtenue par la
                                # méthode du complément à 2**16, cela donne 65436 - 2**16 = -100.
    executer_instruction_ADD_SIGNED(["R1", "R1", "R2"], registres)
    assert registres["R1"] == "0x0001" # En décimal signé, cet entier est égal à +1.
    assert registres["DRAPEAU_NUL"] == 0
    assert registres["DRAPEAU_NEG"] == 0
    assert registres["DRAPEAU_DEB"] == 0


def test_instruction_ADD_SIGNED_cas_3():
    registres["R1"] = "0x0063"  # En décimal signé, cet entier est égal à: 6*16 + 3 = 99
    registres["R2"] = "0xff9c"  # En décimal signé, cet entier est négatif, sa valeur est obtenue par la
                                # méthode du complément à 2**16, cela donne 65436 - 2**16 = -100.
    executer_instruction_ADD_SIGNED(["R1", "R1", "R2"], registres)
    assert registres["R1"] == "0xffff" # En décimal signé, cet entier est égal à -1.
    assert registres["DRAPEAU_NUL"] == 0
    assert registres["DRAPEAU_NEG"] == 1
    assert registres["DRAPEAU_DEB"] == 0


def test_instruction_ADD_SIGNED_cas_4():
    registres["R1"] = "0x7fff"  # En décimal signé, cet entier est égal à:
                                # 7*16**3 + 15*16**2 + 15*16 + 15 = 32767
    registres["R2"] = "0x7fff"  # En décimal signé, cet entier est égal à: 32767
    executer_instruction_ADD_SIGNED(["R1", "R1", "R2"], registres)
    assert registres["R1"] == "0xfffe" # En décimal signé, cet entier est égal à -2.
    assert registres["DRAPEAU_NUL"] == 0
    assert registres["DRAPEAU_NEG"] == 1
    assert registres["DRAPEAU_DEB"] == 1


def test_instruction_ADD_SIGNED_cas_5():
    registres["R1"] = "0xffff"  # En décimal signé, cet entier est égal à: (2**16 - 1) - 2**16 = -1.
    registres["R2"] = "0xffff"  # En décimal signé, cet entier est égal à: (2**16 - 1) - 2**16 = -1.
    executer_instruction_ADD_SIGNED(["R1", "R1", "R2"], registres)
    assert registres["R1"] == "0xfffe" # En décimal signé, cet entier est égal à -2.
    assert registres["DRAPEAU_NUL"] == 0
    assert registres["DRAPEAU_NEG"] == 1
    assert registres["DRAPEAU_DEB"] == 0


def test_instruction_ADD_SIGNED_cas_6():
    registres["R1"] = "0x7fff"  # En décimal signé, cet entier est égal à: 2**15 - 1 = 32767.
    registres["R2"] = "0x7fff"  # En décimal signé, cet entier est égal à: 2**15 - 1 = 32767.
    executer_instruction_ADD_SIGNED(["R1", "R1", "R2"], registres)
    assert registres["R1"] == "0xfffe" # En décimal signé, cet entier est égal à -2.
    assert registres["DRAPEAU_NUL"] == 0
    assert registres["DRAPEAU_NEG"] == 1
    assert registres["DRAPEAU_DEB"] == 1

def test_instruction_MUL_cas_1():
    registres["R1"] = "0x0000"
    registres["R2"] = "0x0001"
    executer_instruction_MUL(["R1", "R1", "R2"], registres)
    assert registres["R1"] =="0x0000"
    assert registres["DRAPEAU_NUL"] == 1
    assert registres["DRAPEAU_NEG"] == 0
    assert registres["DRAPEAU_DEB"] == 0

def test_instruction_MUL_cas_2():
    registres["R1"] = "0x2710"
    registres["R2"] = "0x04d2"
    executer_instruction_MUL(["R1", "R1", "R2"], registres)
    assert registres["R1"] =="0x4b20"
    assert registres["DRAPEAU_NUL"] == 0
    assert registres["DRAPEAU_NEG"] == 0
    assert registres["DRAPEAU_DEB"] == 1

def test_instruction_SUB_SIGNED_cas_1():
    registres["R1"] = "0x0064"  # En décimal signé, cet entier est égal à: 6*16 + 4 = 100
    registres["R2"] = "0xff9c"  # En décimal signé, cet entier est négatif, sa valeur est obtenue par la
                                # méthode du complément à 2**16, cela donne 65436 - 2**16 = -100.
    executer_instruction_SUB_SIGNED(["R1", "R1", "R2"], registres)
    assert registres["R1"] == "0x00c8" # En décimal signé, cet entier est égal à 200.
    assert registres["DRAPEAU_NUL"] == 0
    assert registres["DRAPEAU_NEG"] == 0
    assert registres["DRAPEAU_DEB"] == 0


def test_instruction_SUB_SIGNED_cas_2():
    registres["R1"] = "0x0065"  # En décimal signé, cet entier est égal à: 6*16 + 5 = 101
    registres["R2"] = "0x0064"  # En décimal signé, cet entier est égal à: 6*16 + 4 = 100
    executer_instruction_SUB_SIGNED(["R1", "R1", "R2"], registres)
    assert registres["R1"] == "0x0001" # En décimal signé, cet entier est égal à 1.
    assert registres["DRAPEAU_NUL"] == 0
    assert registres["DRAPEAU_NEG"] == 0
    assert registres["DRAPEAU_DEB"] == 0


def test_instruction_SUB_SIGNED_cas_3():
    registres["R1"] = "0x0064"  # En décimal signé, cet entier est égal à: 6*16 + 4 = 100
    registres["R2"] = "0x0065"  # En décimal signé, cet entier est égal à: 6*16 + 5 = 101
    executer_instruction_SUB_SIGNED(["R1", "R1", "R2"], registres)
    assert registres["R1"] == "0xffff" # En décimal signé, cet entier est égal à -1.
    assert registres["DRAPEAU_NUL"] == 0
    assert registres["DRAPEAU_NEG"] == 1
    assert registres["DRAPEAU_DEB"] == 0


def test_instruction_SUB_SIGNED_cas_4():
    registres["R1"] = "0x7fff"  # En décimal signé, cet entier est égal à: 32767
    registres["R2"] = "0xffff"  # En décimal signé, cet entier est égal à: -1
    executer_instruction_SUB_SIGNED(["R1", "R1", "R2"], registres)
    assert registres["R1"] == "0x8000" # En décimal signé, cet entier est égal à -32768.
    assert registres["DRAPEAU_NUL"] == 0
    assert registres["DRAPEAU_NEG"] == 1
    assert registres["DRAPEAU_DEB"] == 1


def test_instruction_SUB_SIGNED_cas_5():
    registres["R1"] = "0xf000"  # En décimal signé, cet entier est égal à: -4096
    registres["R2"] = "0x7999"  # En décimal signé, cet entier est égal à: 31129
    executer_instruction_SUB_SIGNED(["R1", "R1", "R2"], registres)
    assert registres["R1"] == "0x7667" # En décimal signé, cet entier est égal à 30311.
    assert registres["DRAPEAU_NUL"] == 0
    assert registres["DRAPEAU_NEG"] == 0
    assert registres["DRAPEAU_DEB"] == 1


def test_instruction_SUB_SIGNED_cas_6():
    registres["R1"] = "0xf000"  # En décimal signé, cet entier est égal à: -4096
    registres["R2"] = "0xf000"  # En décimal signé, cet entier est égal à: -4096
    executer_instruction_SUB_SIGNED(["R1", "R1", "R2"], registres)
    assert registres["R1"] == "0x0000" # En décimal signé, cet entier est égal à 0.
    assert registres["DRAPEAU_NUL"] == 1
    assert registres["DRAPEAU_NEG"] == 0
    assert registres["DRAPEAU_DEB"] == 0


def test_instruction_AND_cas_1():
    registres["R1"] = "0xbb00"         # en binaire "1011101100000000"
    registres["R2"] = "0x12ab"         # en binaire "0001001010101011"
    executer_instruction_AND(["R1", "R1", "R2"], registres)
    assert registres["R1"] == "0x1200" # en binaire "0001001000000000"


def test_instruction_AND_cas_2():
    registres["R1"] = "0xbb00"         # en binaire "1011101100000000"
    registres["R2"] = "0x44ab"         # en binaire "0100010010101011"
    executer_instruction_AND(["R1", "R1", "R2"], registres)
    assert registres["R1"] == "0x0000" # en binaire "0000000000000000"


def test_instruction_AND_cas_3():
    registres["R1"] = "0xff00"         # en binaire "1111111100000000"
    op3             = "0x010f"         # en binaire "0000000100001111"
    executer_instruction_AND(["R1", "R1", op3], registres)
    assert registres["R1"] == "0x0100" # en binaire "0000000100000000"


def test_instruction_OR_cas_1():
    registres["R1"] = "0xbb00"         # en binaire "1011101100000000"
    registres["R2"] = "0x12ab"         # en binaire "0001001010101011"
    executer_instruction_OR(["R1", "R1", "R2"], registres)
    assert registres["R1"] == "0xbbab" # en binaire "1011101110101011"


def test_instruction_OR_cas_2():
    registres["R1"] = "0xbb00"         # en binaire "1011101100000000"
    registres["R2"] = "0x44ff"         # en binaire "0100010011111111"
    executer_instruction_OR(["R1", "R1", "R2"], registres)
    assert registres["R1"] == "0xffff" # en binaire "1111111111111111"


def test_instruction_XOR_cas_1():
    registres["R1"] = "0xbb00"         # en binaire "1011101100000000"
    registres["R2"] = "0x12ab"         # en binaire "0001001010101011"
    executer_instruction_XOR(["R1", "R1", "R2"], registres)
    assert registres["R1"] == "0xa9ab" # en binaire "1010100110101011"


def test_instruction_XOR_cas_2():
    registres["R1"] = "0xbb00"         # en binaire "1011101100000000"
    registres["R2"] = "0x44ff"         # en binaire "0100010011111111"
    executer_instruction_XOR(["R1", "R1", "R2"], registres)
    assert registres["R1"] == "0xffff" # en binaire "1111111111111111"


def test_instruction_NOT_cas_1():
    registres["R1"] = "0xbb00"         # en binaire "1011101100000000"
    executer_instruction_NOT(["R1", "R1"], registres)
    assert registres["R1"] == "0x44ff" # en binaire "0100010011111111"


def test_instruction_NOT_cas_2():
    registres["R1"] = "0xffff"         # en binaire "1111111111111111"
    executer_instruction_NOT(["R1", "R1"], registres)
    assert registres["R1"] == "0x0000" # en binaire "0000000000000000"


def test_instruction_CMP_cas_1():
    registres["R1"] = "0xbb00"
    registres["R2"] = "0xbb00"
    executer_instruction_CMP(["R1", "R2"], registres)
    assert registres["DRAPEAU_CMP"] == "EQ"


def test_instruction_CMP_cas_2():
    registres["R1"] = "0xaaff"
    registres["R2"] = "0xbb00"
    executer_instruction_CMP(["R1", "R2"], registres)
    assert registres["DRAPEAU_CMP"] == "LT"


def test_instruction_CMP_cas_3():
    registres["R1"] = "0xaaff"
    registres["R2"] = "0xbb00"
    executer_instruction_CMP(["R1", "R2"], registres)
    assert registres["DRAPEAU_CMP"] == "LT"


def test_instruction_EQ_cas_1():
    registres["R1"] = "0xbb00"
    registres["R2"] = "0xbb00"
    registres["PC"] = "0x0001"
    registres["SP"] = "0xff00"
    executer_instruction_CMP(["R1", "R2"], registres)
    executer_instruction_EQ(["0x23aa"], memoire, registres)
    assert registres["PC"] == "0x23aa"
    assert registres["SP"] == "0xff01"
    assert lecture_memoire(memoire, registres["SP"]) == "0x0001"


def test_instruction_EQ_cas_2():
    registres["R1"] = "0xbb00"
    registres["R2"] = "0xbb01"
    registres["PC"] = "0x0001"
    registres["SP"] = "0xff00"
    executer_instruction_CMP(["R1", "R2"], registres)
    executer_instruction_EQ(["0x23aa"], memoire, registres)
    assert registres["PC"] == "0x0001"
    assert registres["SP"] == "0xff00"


def test_instruction_NE_cas_1():
    registres["R1"] = "0xbb00"
    registres["R2"] = "0xbb01"
    registres["PC"] = "0x0001"
    registres["SP"] = "0xff00"
    executer_instruction_CMP(["R1", "R2"], registres)
    executer_instruction_NE(["0x23aa"], memoire, registres)
    assert registres["PC"] == "0x23aa"
    assert registres["SP"] == "0xff01"
    assert lecture_memoire(memoire, registres["SP"]) == "0x0001"


def test_instruction_NE_cas_2():
    registres["R1"] = "0xbb00"
    registres["R2"] = "0xbb00"
    registres["PC"] = "0x0001"
    registres["SP"] = "0xff00"
    executer_instruction_CMP(["R1", "R2"], registres)
    executer_instruction_NE(["0x23aa"], memoire, registres)
    assert registres["PC"] == "0x0001"
    assert registres["SP"] == "0xff00"


def test_instruction_GT_cas_1():
    registres["R1"] = "0xbb01"
    registres["R2"] = "0xbb00"
    registres["PC"] = "0x0001"
    registres["SP"] = "0xff00"
    executer_instruction_CMP(["R1", "R2"], registres)
    executer_instruction_GT(["0x23aa"], memoire, registres)
    assert registres["PC"] == "0x23aa"
    assert registres["SP"] == "0xff01"
    assert lecture_memoire(memoire, registres["SP"]) == "0x0001"


def test_instruction_GT_cas_2():
    registres["R1"] = "0xbb00"
    registres["R2"] = "0xbb00"
    registres["PC"] = "0x0001"
    registres["SP"] = "0xff00"
    executer_instruction_CMP(["R1", "R2"], registres)
    executer_instruction_GT(["0x23aa"], memoire, registres)
    assert registres["PC"] == "0x0001"
    assert registres["SP"] == "0xff00"


def test_instruction_LT_cas_1():
    registres["R1"] = "0xbb00"
    registres["R2"] = "0xbb01"
    registres["PC"] = "0x0001"
    registres["SP"] = "0xff00"
    executer_instruction_CMP(["R1", "R2"], registres)
    executer_instruction_LT(["0x23aa"], memoire, registres)
    assert registres["PC"] == "0x23aa"
    assert registres["SP"] == "0xff01"
    assert lecture_memoire(memoire, registres["SP"]) == "0x0001"


def test_instruction_LT_cas_2():
    registres["R1"] = "0xbb00"
    registres["R2"] = "0xbb00"
    registres["PC"] = "0x0001"
    registres["SP"] = "0xff00"
    executer_instruction_CMP(["R1", "R2"], registres)
    executer_instruction_LT(["0x23aa"], memoire, registres)
    assert registres["PC"] == "0x0001"
    assert registres["SP"] == "0xff00"


def test_instruction_B():
    registres["PC"] = "0x0001"
    registres["SP"] = "0xff00"
    executer_instruction_B(["0x23aa"], memoire, registres)
    assert registres["PC"] == "0x23aa"
    assert registres["SP"] == "0xff01"


def test_instruction_HALT():
    registres["PC"] = "0x0001"
    registres["SP"] = "0xff00"
    executer_instruction_B(["0x23aa"], memoire, registres)
    assert registres["PC"] == "0x23aa"
    assert registres["SP"] == "0xff01"
    executer_instruction_HALT([], memoire, registres)
    assert registres["PC"] == "0x0001"
    assert registres["SP"] == "0xff00"
