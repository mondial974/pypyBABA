   
def printentete():
    print("="*77)
    print(f'{"DESIGNATION":45} {"SYMBOLE":<10} {"VALEUR":^10} {" "} {"UNITE":^10}')
    print("="*77)

def printligne(designation, symbole, unite, valeur):
    print(f'    {designation:45} {symbole:<15} {valeur:>10} {"   "} {unite:<10}')
        
def printsep():
    print("-"*77)

def printfintab():
    print("="*77)

def printverification():
    print("Vérifications :")
    print("---------------")

def printVERIFIE(message):
    print("    VERIFIE : ", message)

def printNONVERIFIE(message):
    print("NON VERIFIE : ", message)
    
def printMESSAGE(message):
    print("              ", message)  


def printfile(texte, f):
    print(texte, file=f)

def printentetefile(f):
    print("="*77, file=f)
    print(f'{"DESIGNATION":45} {"SYMBOLE":<10} {"VALEUR":^10} {" "} {"UNITE":^10}', file=f)
    printfile("="*77, f)

def printlignefile(designation, symbole, unite, valeur, file):
    print(f'{designation:45} {symbole:<15} {valeur:>10} {"   "} {unite:<10}', file=file)

def printsepfile(f):
    print("-"*77, file=f)