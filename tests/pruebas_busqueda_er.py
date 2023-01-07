'''
Created on 14/7/2019

@author: Jesus Enrique
'''

import re

# -------------------------------------------------------------

def buscar(patrones,texto):
    for patron in patrones:
        print(re.findall(patron, texto))

# -------------------------------------------------------------

if __name__ == '__main__':
    
    texto= "hola esto es un texto hola"
    palabra= "hola"
    encontrado = re.search(palabra, texto)
    if encontrado:
        print("Se enconto ",palabra)
        print(encontrado.string)
    else:
        print("No se enconto ",palabra)

    print(re.split(' ',texto))
    
    #print(re.sub())
    
    print(len(re.findall(palabra, texto)))
    
    print(len(re.findall('es|texto',texto))) 
    
    patrones = ['hla', 'hola', 'hoola']
    buscar(patrones, texto)