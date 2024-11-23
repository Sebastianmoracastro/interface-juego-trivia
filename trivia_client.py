# Instalar el módulo requests haciendo desde una terminal: pip install requests
import requests


# Función para registrar usuario
def registerUser(url,name,password):    
    response=requests.post(url+'/register',data=f'name={name}&password={password}')
    return response.content.decode('utf-8')

# Funciónn para abrir una sesión
def openSession(url,name,password):    
    response=requests.put(url+'/login',data=f'name={name}&password={password}')
    return response.content.decode('utf-8')

# Función para cerrar una sesión
def closeSession(url,name,password):    
    response=requests.put(url+'/logout',data=f'name={name}&password={password}')
    return response.content.decode('utf-8')


# Función para abrir o cerrar sesión en el servidor
def openCloseSession(url, name, password, flag):
    # Se hace la solicitud PUT para iniciar/cerrar sesión
    response = requests.put(url + '/session', data={'name': name, 'password': password, 'flag': flag})
    
    # Se devuelve la respuesta del servidor
    return response.content.decode('utf-8')




# Función para actualizar el puntaje
def updateScore(url,name,password,score):    
    response=requests.put(url+'/score',f'name={name}&password={password}&score={score}')
    return response.content.decode('utf-8')

# Función para obtener el puntaje
def getScore(url,name,password):    
    response=requests.get(url+'/score',data=f'name={name}&password={password}')
    return response.content.decode('utf-8')

# Función para obtener la lista de usuarios conectados
def getList(url,name,password):    
    response=requests.get(url+'/list',data=f'name={name}&password={password}')
    return response.content.decode('utf-8')

# Función para obtener una pregunta aleatoria
def getQuestion(url,name,password,cat):    
    response=requests.get(url+'/question',data=f'name={name}&password={password}&cat={cat}')
    return response.content.decode('utf-8')


