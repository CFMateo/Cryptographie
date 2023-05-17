""" Utiliser doctests"""
#! https://github.com/mformenace/Cryptographie/issues/1

# ? Question 1
# ? Question 1

# A = 0, B = 0 --> XOR(A,B) = 0 donc XOR(XOR(A,B),B) = XOR(0,0) = 0
# A = 1, B = 0 --> XOR(A,B) = 1 donc XOR(XOR(A,B),B) = XOR(1,0) = 1
# A = 0, B = 1 --> XOR(A,B) = 1 donc XOR(XOR(A,B),B) = XOR(1,1) = 0
# A = 1, B = 1 --> XOR(A,B) = 0 donc XOR(XOR(A,B),B) = XOR(0,1) = 1
# On observe bien que les valeurs de A sont exactement les mêmes pour XOR(XOR(A,B),B).

# ? Question 2

def convertit_texte_en_binaire(texte):
    """
    Convertit un texte en une chaîne binaire représentant les codes ASCII des caractères.

    Args:
        texte (str): Le texte à convertir.

    Returns:
        str: La chaîne binaire représentant le texte.

    Tests:
    >>> convertit_texte_en_binaire("NSI")
    '010011100101001101001001'
    """
    chaine_binaire = ''
    for el in texte:
        code_ascii = ord(el)
        binaire = bin(code_ascii)[2:]

        while len(binaire) < 8:
            binaire = '0' + binaire

        chaine_binaire += binaire
    return chaine_binaire


# ? Question 3

def convertit_binaire_vers_entier_base_10(chaine_binaire):
    """
    Convertit une chaîne binaire en un entier de base 10.

    Args:
        chaine_binaire (str): La chaîne binaire à convertir.

    Returns:
        int: L'entier de base 10.

    Tests:
    >>> convertit_binaire_vers_entier_base_10("01001110")
    78
    """
    return int(chaine_binaire, 2)


# ? Question 4

def convertit_binaire_en_texte(chaine_binaire):
    """
    Convertit une chaîne binaire représentant des codes ASCII en un texte.

    Args:
        chaine_binaire (str): La chaîne binaire à convertir.

    Returns:
        str: Le texte converti.

    Tests:
    >>> convertit_binaire_en_texte("010011100101001101001001")
    'NSI'
    """
    cb = chaine_binaire
    texte = ''

    while len(cb) > 0:
        texte += chr(convertit_binaire_vers_entier_base_10(cb[:8]))
        cb = cb[8:]

    return texte


# ? Question 5

def xor(a, b):
    """
    Implémentation de l'opération XOR entre deux valeurs.

    Args:
        a (str): La première valeur.
        b (str): La deuxième valeur.

    Returns:
        str: Le résultat de l'opération XOR.

    """
    if a == b:
        return '0'
    return '1'



def chiffre_xor(chaine_binaire, clef_binaire):
    """
    Args:
        chaine_binaire (_type_): _description_ 
        clef_binaire (_type_): _description_

    Test:
    >>> chiffre_xor("SPECIALITE NSI", "TERM")
    '0000011100010101000101110000111000011101000001000001111000000100000000000000000001110010000000110000011100001100'
    """
    chb = convertit_texte_en_binaire(chaine_binaire)
    clb = convertit_texte_en_binaire(clef_binaire)
    chaine_binaire_chiffree = ''

    # extension de la clef pour faire la meme taille que la chaine:
    while len(chb) - len(clb) > 0:
        for i in clb:
            clb += i

    # on ajoute le résultat du xor entre les deux éléments a la chaine finale
    for i in range(len(chb)):
        chaine_binaire_chiffree += xor(chb[i], clb[i])

    return chaine_binaire_chiffree


print(chiffre_xor("SPECIALITE NSI", "TERM"))


# ? Question 6


# ? Question 7 : Prenons a1=5 , b1=3 , a2=7 et b2=5

# M=a1*b1-1=5*3-1= 14 ; e=a2*M+a1=7*14+5= 103 ; d=b2*M+b1= 5*14+3= 73 ; n=(e×d-1)/M=(103*73-1)/14= 537
# La clé publique est (e,n) soit (103,537) et La clef secrète est (d,n) soit (73,537)
# Le code ASCII de la lettre 'a' en minuscule est 97. Comme m < n: on efectue e x m (modulo n): e * 97 % n = 103 * 97 % 537 = 325
# La clef privée est: (73,537), on sait que pour déchiffrer on effectue l'opération d x m (modulo n) = 73*325%537 = 97; On retrouve bien le code ASCII de la lettre 'a'.


# ? Question 8
def genere_clefs_publique_et_privee(a1, b1, a2, b2):
    M = a1 * b1 - 1
    e = a2 * M + a1
    d = b2 * M + b1
    n = (e * d - 1) // M
    return (e, n), (d, n)


def chiffre_message(message, clef):
    """
    chiffre un message m qui est une chaîne de caractères avec la clef,
      en remplaçant chaque caractère par son code ASCII en décimal.
    Pour chiffrer un message représenté par un entier m plus petit que n, on effectue l'opération e x m (modulo n).
    """
    message_chiffre = []
    n = clef[1]
    e = clef[0]
    for caractere in message:
        ascii_code = ord(caractere)
        lettrechiffree = (e*ascii_code) % n
        message_chiffre.append(lettrechiffree)
    return message_chiffre

def dechiffre_message(messageChiffre, clef):
    """
    déchiffre un message m qui est une liste de nombres et renvoie le message 
    déchiffré sous la forme d'une chaîne de caractères.
    Pour déchiffrer un message représenté par un entier m plus petit que n, on effectue l'opération d x m (modulo n)

    Args:
        messageChiffre (list): Le message chiffré sous forme de liste de nombres.
        clef (tuple): La clé de déchiffrement (d, n).

    Returns:
        str: Le message déchiffré.

    """
    message_dechiffre = ""
    d = clef[0]
    n = clef[1]
    for el in messageChiffre:
        lettreDechifree = chr((d * el) % n)
        message_dechiffre += lettreDechifree
    return message_dechiffre



# Exemple avec a1=5, b1=3, a2=7 et b2=5
clef_publique, clef_privee = genere_clefs_publique_et_privee(5, 3, 7, 5)
message = "wop wop "

message_chiffre = chiffre_message(message, clef_publique)
message_dechiffre = dechiffre_message(message_chiffre, clef_privee)

print("Clef publique :", clef_publique)
print("Clef privée :", clef_privee)
print("Message initial :", message)
print("Message chiffré :", message_chiffre)
print("Message déchiffré :", message_dechiffre)


# ? Question 9
# valeur clef publique:(28648, 1004889)

# valeur clef priv: (14557, 1004889)

# [224766, 368006, 81526]
# print(chiffre_message("NSI", (28648, 1004889)))

# message déchifré: print(dechiffre_message([224766, 368006, 81526], (14557, 1004889))) return bien "NSI"


# ? Question 10
def bruteForceKidRSA(e, n):
    """
    Effectue une attaque par force brute pour trouver la clé privée 'd' dans l'algorithme RSA.

    Args:
        e (int): L'exposant de la clé publique.
        n (int): Le module.

    Returns:
        int: La clé privée 'd'.

    """
    d = 0
    # d <= n pourrait ne pas être nécessaire car je pense que le retour se produira toujours avant
    while d <= n:
        print(d)

        if (e * d - 1) % n == 0:
            return d
        d += 1


# ? Question 11
# print(bruteForceKidRSA(53447, 5185112)) donc 323639
print(dechiffre_message([3580949, 2084433, 3687843, 4436101, 4489548, 1710304, 4329207, 4542995, 3901631, 1710304, 4061972, 3687843, 1710304,
      3527502, 4222313, 4436101, 4436101, 1710304, 3687843, 4168866, 1710304, 4168866, 4436101, 3901631, 1710304, 3367161], (323639, 5185112)))
# message: C'EST QUI LE BOSS EN NSI ?



# ? Question 12

# print(bruteForceKidRSA(230884490440319, 194326240259798261076))
# Le programme est extrêmement lent
# ? Question 13

def egcd(a, b):
    """
    Effectue l'algorithme d'Euclide étendu pour calculer le plus grand commun diviseur (PGCD) et les coefficients de Bézout.

    Args:
        a (int): Le premier entier.
        b (int): Le deuxième entier.

    Returns:
        Tuple[int, int, int]: Le PGCD et les coefficients de Bézout (g, x, y) tels que g = PGCD(a, b) et ax + by = g.

    """
    if a == 0:
        return (b, 0, 1)
    else:
        g, y, x = egcd(b % a, a)
        return (g, x - (b // a) * y, y)


def modinv(e, n):
    """
    Calcule l'inverse modulaire de e modulo n.

    Args:
        e (int): L'entier dont on veut calculer l'inverse modulaire.
        n (int): Le modulo.

    Returns:
        Union[int, bool]: L'inverse modulaire de e modulo n si celui-ci existe, False sinon.

    """
    g, x, y = egcd(e, n)
    if g != 1:
        return False
    else:
        return x % n



print(modinv(230884490440319, 194326240259798261076))  # ne
# return  qui est d 158674832848565541575

print(dechiffre_message([16623683311702968, 19625181687427115, 16392798821262649, 16392798821262649, 20548719649188391, 7388303694090208, 17547221273464244, 15931029840382011, 19163412706546477, 7388303694090208, 15238376369061054, 18239874744785201,
      18008990254344882, 19163412706546477, 7388303694090208, 19394297196986796, 19625181687427115, 20548719649188391, 15007491878620735, 19625181687427115, 20317835158748072, 7388303694090208, 7619188184530527], (158674832848565541575,194326240259798261076)))
# ? Question 14


# La taille des clefs courament utilisées par la RSA pour sécuriser des données sur internet sont entre 2048 et 4096 bits
# La nouvelle technologie qui permetrait de casser la RSA en quelques secondes se nomme la cryptographie quantique
'''if __name__ == "__main__":
    import doctest
    doctest.testmod(verbose=True)
'''
