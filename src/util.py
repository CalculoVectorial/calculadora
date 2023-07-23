import numpy as np
import time
import pygame as py
 
POINTNAME = [f'P{i}' for i in range(100)]
VECTORNAME = [f'V{i}' for i in range(100)]
CURVANAME = [f'C{i}' for i in range(100)]
CAMPONAME = [f'Camp{i}' for i in range(100)]
SUPNAME = [f'S{i}' for i in range(100)]
SUPPARNAME = [f'SP{i}' for i in range(100)]
BOLANAME = [f'B{i}' for i in range(100)]


def eliminar_repetidos(arr1, arr2):
    #Elimina repetidos de un array
    arr2_copy = np.setdiff1d(arr2, arr1)
    return np.concatenate((arr1, arr2_copy))

def prueba_velocidad(func, num):
    #Prueba la velocidad de una funcion
    valores = np.random.randint(1,10, size=(num, 1000000))
    i=time.time()
    func(valores)
    print(time.time() - i)

def is_desempaquetado(obj):
    #Verifica si un objeto viene desempaquetado
    return isinstance(obj, tuple) and len(obj) != 1

def empaquetar(obj): 
    #Vuelve a empaquetar si un objeto llega desempaquetado
    try:
        return np.array(obj)
    except:
        obj = list(obj)
        for i in range(len(obj)):
            if np.array(obj[i]).size == 1:
                obj[i] = np.full(len(obj[i-1]), obj[i])
        return np.array(obj)

def true_rotacion2D(coord, angulo): #Rota un vector 2d
    fila1 = [np.cos(angulo), -np.sin(angulo)]
    fila2 = [np.sin(angulo), np.cos(angulo)]
    matriz_rotacion = np.array([fila1, fila2])
    return np.matmul(matriz_rotacion, coord)

def true_rotacion3D( coord, theta, phi):
        fila1 = [np.cos(theta), -np.sin(theta), 0]
        fila2 = [np.sin(theta), np.cos(theta)*np.cos(phi), -np.sin(phi)]
        fila3 = [0, np.sin(phi), np.cos(phi)]
        matriz_rotacion = np.array([fila1, fila2, fila3])
        result = np.matmul(matriz_rotacion, coord)
        return result

def cartesiano(rango1, rango2, rebanadas):
    x = np.linspace(rango1[0],rango1[1], rebanadas)
    y = np.linspace(rango2[0],rango2[1], rebanadas)
    X, Y =  np.meshgrid(x, y)
    result = np.column_stack((X.ravel(), Y.ravel()))
    return result

def cartesiano3D(rango1, rango2, rango3, rebanadas):
    x = np.linspace(rango1[0],rango1[1], rebanadas)
    y = np.linspace(rango2[0],rango2[1], rebanadas)
    z = np.linspace(rango3[0],rango3[1], rebanadas)
    X, Y, Z = np.meshgrid(x, y, z)
    result = np.column_stack((X.ravel(), Y.ravel(), Z.ravel()))
    return result

def detectar_color(color):
    if color.find(',')>0:
        color = np.array(color.split(','), dtype=int)
    return py.Color(color)

def move_column(array, axis):
    if axis==2:
        num = 1
    elif axis==3:
        num=0
    else:
        num=2
    array[:, [num, 2]] = array[:, [2, num]]

def gen_dom(coords, rebanadas, rango, axis):
    dom = None
    if coords == 'Esfera':
        if axis==2:
            dom = cartesiano((0, 2*np.pi), (0, rango), rebanadas)
        elif axis==3:
            dom = cartesiano((0, rango), (0, np.pi), rebanadas)
        else:
            dom = cartesiano((0, 2*np.pi), (0, np.pi), rebanadas)
    
    elif coords == 'Cilindro':
        if axis==2:
            dom = cartesiano((0, rango), (-rango, rango), rebanadas)
        elif axis==3:
            dom = cartesiano((-rango, rango), (0, 2*np.pi), rebanadas)
        else:
            dom = cartesiano((0, rango), (0, 2*np.pi), rebanadas)
    else:
        dom = cartesiano((-rango, rango), (-rango, rango), rebanadas)
    return dom

def identificar_tipo_entrada(texto):
    # Verificar si es un punto
    if texto.startswith(('Esfera', 'Elipse', 'Hiperboloide1', 'Hiperboloide2', 'Cono', 'Parametro', 'Bola')):
        return "Special"
        
    elif texto.startswith("(") and texto.endswith(")") and "," in texto:
        return "Point"

    # Verificar si es un vector
    elif texto.startswith("[") and texto.endswith("]") and "," in texto:
        return 'Vector'

    # Verificar si es una superficie
    elif ("x" in texto or "y" in texto) and not ";" in texto and not "[" in texto and not"(x,y)" in texto:
        return "Superficie"

    # Verificar si es una superficie paramétrica
    elif ("u" in texto or "v" in texto) and ";" in texto:
        return "SuperficieParametrica"

    # Verificar si es una curva
    elif "t" in texto and ";" in texto:
        return "Curva"

    # Verificar si es campo
    elif ("x" in texto or "y" in texto  or "z" in texto) and not"(x,y)" in texto:
        return "Campo"
    
    elif ";" in texto:
        return "Campo"

    elif not ";" in texto:
        return "Superficie"
    
    else:
        return "Entrada no identificada"

def nombre_default(tipo):
    if tipo == "Point":
        return POINTNAME.pop(0)
    elif tipo == "Vector":
        return VECTORNAME.pop(0)
    elif tipo == 'Curva':
        return CURVANAME.pop(0)
    elif tipo == 'Campo':
        return CAMPONAME.pop(0)
    elif tipo == 'Superficie' or tipo == 'Special':
        return SUPNAME.pop(0)
    elif tipo == 'SuperficieParametrica':
        return SUPPARNAME.pop(0)
    else:
        return 'Nada'

def ajustar_rango(rango1, rango2, mode, axis):
    if str(rango1) == '':
        if mode == 'Cartesiano':
            rango1 = np.array([-3,3])
        elif mode == 'Cilindro':
            rango1 = np.array([0,3])
        else:
            rango1 = np.array([0,2*np.pi])

    if str(rango2) == '':
        if mode == 'Cartesiano':
            rango2 = np.array([-3,3])
        elif mode == 'Cilindro':
            rango2 = np.array([0,2*np.pi])
        else:
            rango2 = np.array([0,np.pi])

    if mode == 'Cartesiano':
        return [rango1, rango2]
    elif mode == 'Cilindro' and axis!=3:
        if rango1[0]<0:
            rango1[0] = 0
        if rango1[1]<0:
            rango1[1] = abs(rango1[1])
    elif mode == 'Esfera' and axis==2:
        if rango2[0]<0:
            rango2[0] = 0
        if rango2[1]<0:
            rango2[1] = abs(rango2[1])
    elif mode == 'Esfera' and axis==3:
        if rango1[0]<0:
            rango2[0] = 0
        if rango1[1]<0:
            rango1[1] = abs(rango1[1])

    return [rango1, rango2]

def info_special_sup(exp):
    index = exp.find('(')
    name = exp[:index]
    parametros = exp.replace(name, '')[1:-1]
    index = parametros.find('(')
    info = parametros[:index]
    desplazamiento = parametros[index:]
    info = info[:-1].split(",")
    return name, info, desplazamiento

