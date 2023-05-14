""" Utiliser doctests"""

'''
# ? Question 1

# A = 0, B = 0 --> XOR(A,B) = 0 donc XOR(XOR(A,B),B) = XOR(0,0) = 0
# A = 1, B = 0 --> XOR(A,B) = 1 donc XOR(XOR(A,B),B) = XOR(1,0) = 1
# A = 0, B = 1 --> XOR(A,B) = 1 donc XOR(XOR(A,B),B) = XOR(1,1) = 0
# A = 1, B = 1 --> XOR(A,B) = 0 donc XOR(XOR(A,B),B) = XOR(0,1) = 1
# On observe bien que les valeurs de A sont exactement les mêmes pour XOR(XOR(A,B),B).

# ? Question 2


def convertit_texte_en_binaire(texte):
    """
    (talk about ord and bin)
    on doit avoir un octet par defaut, c'est pour cela que je normalise la taille de 'binaire'.

    Args:
        texte (_type_): _description_

    Returns:
        _type_: _description_

    Tests: (add some)

    >>> convertit_texte_en_binaire("NSI")
    '010011100101001101001001'

    """
    chaine_binaire = ''
    for el in texte:
        # iteration dans texte
        code_ascii = ord(el)
        # le slice ci-dessous sert a retirer le préfixe par défaut pour les nombres binaires de python '0b'
        binaire = bin(code_ascii)[2:]

        # normalisation de l'octet en ajoutant des zéros a gauche s'il le faut
        while len(binaire) < 8:
            binaire = '0' + binaire

        # on ajoute le nouvel élément binaire a la chaine
        chaine_binaire += binaire
    return chaine_binaire


# ? Question 3

def convertit_binaire_vers_entier_base_10(chaine_binaire):
    """_summary_

    Args:
        chaine_binaire (_type_): _description_

    Tests:
    >>> convertit_binaire_vers_entier_base_10("01001110")
    78
    """
    return int(chaine_binaire, 2)


# ? Question 4


def convertit_binaire_en_texte(chaine_binaire):
    """_summary_

    Args:
        chaine_binaire (_type_): _description_

    Tests:
    >>> convertit_binaire_en_texte("010011100101001101001001")
    'NSI'
    """
    # on crée une copie afin de ne pas modifier la chaine binaire de base
    cb = chaine_binaire
    texte = ''

    # itération sur les octets
    while len(cb) > 0:
        # on convertit le code ascii (nombre décimal) du premier octet de la chaine en texte puis on l'ajoute a texte.
        texte += chr(convertit_binaire_vers_entier_base_10(cb[:8]))
        # On enlève le premier octet de la chaine de manière a répéter cette opération sur le prochain octet
        cb = cb[8:]

    return texte


# ? Question 5

def xor(a, b):
    """
    Implementation du xor avec des 0 et 1
    Args:
        a (_type_): _description_
        b (_type_): _description_

    Returns:
        _type_: _description_
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
'''

# ? Question 6




# ? Question 7 : Prenons a1=5 , b1=3 , a2=7 et b2=5

# M=a1*b1-1=5*3-1= 14 ; e=a2*M+a1=7*14+5= 103 ; d=b2*M+b1= 5*14+3= 73 ; n=(e×d-1)/M=(103*73-1)/14= 537
# La clé publique est (e,n) soit (103,537) et La clef secrète est (d,n) soit (73,537)
# Le code ASCII de la lettre 'a' en minuscule est 97. Comme m < n: on efectue e x m (modulo n): e * 97 % n = 103 * 97 % 537 = 325
# On a bien m = 325 * 73 % 537 = 97 ; On retrouve bien le code ASCII de la lettre 'a'.


# ? Question 8
def genere_clefs_publique_et_privee(a1, b1, a2, b2):
    M = a1 * b1 - 1
    e = a2 * M + a1
    d = b2 * M + b1
    n = (e * d - 1) // M
    return (n, e), (n, d)

def chiffre_message(m, clef_publique):
    message_chiffre = []
    for caractere in m:
        ascii_code = ord(caractere)
        message_chiffre_temp = pow(ascii_code, clef_publique[1], clef_publique[0])
        message_chiffre.append(message_chiffre_temp)
    return message_chiffre

def dechiffre_message(m, clef_privee):
    message_dechiffre = ""
    for code_ascii in m:
        caractere = chr(pow(code_ascii, clef_privee[1], clef_privee[0]))
        message_dechiffre += caractere
    return message_dechiffre

# Exemple avec a1=5, b1=3, a2=7 et b2=5
clef_publique, clef_privee = genere_clefs_publique_et_privee(5, 3, 7, 5)
message = "a"
message_chiffre = chiffre_message(message, clef_publique)
message_dechiffre = dechiffre_message(message_chiffre, clef_privee)

print("Clef publique :", clef_publique)
print("Clef privée :", clef_privee)
print("Message initial :", message)
print("Message chiffré :", message_chiffre)
print("Message déchiffré :", message_dechiffre)



# ? Question 9



# ? Question 10
# ? Question 11
# ? Question 12
# ? Question 13
# ? Question 14
'''if __name__ == "__main__":
    import doctest
    doctest.testmod(verbose=True)
'''