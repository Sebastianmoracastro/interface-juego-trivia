from random import randint
import random
import requests
# Conjunto para llevar un registro de usuarios conectados
connected_users = set()

# Función para registrar un nuevo usuario
def registerUser(name, password):
    name = name.strip().lower()  
    password = password.strip()

    try:
        with open("usuarios.txt", "r") as file:#Se intenta abrir el archivo usuarios.txt en modo lectura r. Si el archivo no existe, se lanzara una excepcion para mas adelante
            for line in file:#Se itera sobre cada linea del archivo abierto.
                if line:  #verifica si la linea esta vacia
                    parts = line.split(",")  #Se divide la línea en partes utilizando la coma paramseparar
                    user = parts[0].strip().lower()  #se pasa el name a minusculas
                    if user == name:  
                        return "ya registrado"
    except FileNotFoundError:
        
        open("usuarios.txt", "w").close()

    with open("usuarios.txt", "a") as file:#abre el archivo txt
        file.write(f"{name},{password},0,no_conectado\n") 
    return "registrado"

def openCloseSession(name, password, flag):
    name = name.strip().lower()
    password = password.strip()
    lines = []#para actualizar las lineas del archivo
    user_found = False# se inicia asi para verificar si el usuario esta en el txt

    with open("usuarios.txt", "r") as file:
        for line in file:
            if line:  
                try:
                    user, passw, user_score, status = line.split(",")#se divide en comas el user,passw,etc
                    if user == name and passw == password:#verifica que si el usuario y la contraseña digitada esta en el txt
                        user_found = True#si se encontro
                       
                        status = "conectado" if flag else "desconetado"#se actualiza el estado a true que es conenctado,si no lo es pasa lo contrario
                    lines.append(f"{user},{passw},{user_score},{status}") #agrega el nuevo estado conectado
                except ValueError:
                    continue  

    if user_found:#procede a actualzair el archivo
        with open("usuarios.txt", "w") as file:#sobreescribe lo que ya existia 
            file.write("\n".join(lines) + "\n")#se escribe en el archivo el contenido de lines 
        return "seccion iniciada" if flag else "Sseccion cerrada"
    
    return "eror de contrasa o usuario"
  
def updateScore(name, password, new_score):
    name = name.strip().lower()
    password = password.strip()
    updated = False
    lines = []#almacena cualquier linea del archivo

    with open("usuarios.txt", "r") as file:
        for line in file:
            if line:  
                try:
                    user, passw, user_score, status = line.split(",")
                    if user.lower() == name and passw == password:
                        user_score = new_score  #se asigna el nuevo dato 
                        updated = True# si fue actualziadao
                    lines.append(f"{user},{passw},{user_score},{status}")#se agrega ala actualizacion a line
                except ValueError:
                    continue 

    if updated:
        with open("usuarios.txt", "w") as file:#sobreescribe el dato"w"
            file.write("\n".join(lines) + "\n")
        return "Actualizado"
    
    return "eror de contra o usuario"

def getScore(name, password):
    name = name.strip().lower()
    password = password.strip()

    with open("usuarios.txt", "r") as file:
        for line in file:
            line = line.strip()
            if line:  
                try:
                    user, passw, user_score, status = line.split(",")
                    if user == name and passw == password:
                        return user_score
                except ValueError:
                    continue  
    return "error de contra o usuario"

def usersList(name=None, password=None):
    connected_users = []# guarda el nombre  delos usuarios

    try:
        with open("usuarios.txt", "r") as file:
            for line in file:
                if line:  
                    try:
                        parts = line.split(",") 
                        #Se Comprueba que hay 4 datos de largo(longuitud),se comprueba que el 4 dato es igual conectado
                        if len(parts) >= 4 and parts[3].strip().lower() == "conectado": 
                            connected_users.append(parts[0].strip())  
                    except IndexError:
                        continue  
    except FileNotFoundError:
        return "usuaruio no registrado"

    if connected_users:
        return f"Usuarios conectados: {', '.join(connected_users)}"
    else:
        return "No hay usuarios conectados."
    
def getQuestion(url, name, password, category):
            response = requests.get(url + '/question', data=f'name={name}&password={password}&cat={category}')
            
            if response.status_code != 200:
                print("Error al obtener la pregunta del servidor.")
                return "Error"  # Devolver un mensaje de error si la solicitud falla

            questions = response.content.decode('utf-8').splitlines()  # Divide la respuesta en líneas
            random.shuffle(questions)  # Mezcla las preguntas

            return questions  # Devolver las preguntas mezcladas

def question(name, password, category):
    total_points = 0  # Iniciar acomulado
    asked_questions = []  # guardar preguntas que salgan
    user_answers = []  # guardar respuestas del usuario
    question_list = []  # iniciar la lista de preguntas

    try:
        with open("preguntas.txt", "r", encoding="utf-8") as file:  #para que funcione con la codificacion de caracteres (utf-8)
            questions = file.readlines()  # Lee todas las lineas del archivo

            if questions:
                question_buffer = []
                
                for line in questions:
                    line = line.strip()

                    if line == "":  # Si es una linea vacia, significa que terminamos una pregunta
                        if question_buffer:
                            # Parseo de preguntas y categorías
                            category_line = question_buffer[0].strip()
                            if category_line.startswith("Categoría:"):
                                category_num = int(category_line.split(":")[1].strip())
                            else:
                                category_num = None

                            # Si la categoría no coincide, omitimos esta pregunta
                            if category_num == category:
                                question_text = question_buffer[1] 
                                options = question_buffer[2:6]  
                                correct_answer = question_buffer[-1].split(":")[1].strip()  

                                question_list.append({
                                    "question": question_text,
                                    "options": options,
                                    "answer": correct_answer
                                })

                            # Limpiar el buffer de pregunta
                            question_buffer = []
                    else:
                        question_buffer.append(line)

                # Mezclador de preguntas
                random.shuffle(question_list)  


                for question_data in question_list:
                    # muestra la pregunta
                    print(f"\nPregunta: {question_data['question']}")
                    for option in question_data['options']:
                        print(option)

                    user_answer = input("Escribe tu respuesta (A, B, C o D): ").strip().upper()

                    # Almacena la pregunta y respuesta del usuario
                    asked_questions.append(question_data['question'])
                    user_answers.append(user_answer)

                    # verifica si la respuesta es correcta
                    if user_answer == question_data['answer']:
                        total_points += 1
                        print("¡Correcto!")
                    else:
                        print("Incorrecto.")  

                    # Pregunta si desea continuar
                    continue_game = input("¿Quieres continuar? (s/n): ").strip().lower()
                    if continue_game != 's':
                        break  

                # Mostrar los resultados finales
                print("\n*"+ "\n*")
                print("\nFin del juego.")
                print(f"Tu puntaje final es:==>> {total_points}")
                print("\nPreguntas y tus respuestas:")
                for i in range(len(asked_questions)):
                    print(f"Pregunta: {asked_questions[i]}")
                    print(f"Tu respuesta: {user_answers[i]}")                
                    print(f"Respuesta correcta: {question_list[i]['answer']}\n")
                
                return total_points
            else:
                print("No hay preguntas disponibles en el archivo.")
                return 0
    except FileNotFoundError:
        print("Error: El archivo de preguntas no existe.")
        return 0


