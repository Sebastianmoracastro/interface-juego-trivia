#interface
from tkinter import *
from tkinter import messagebox #mensajes o alertas
from trivia_client import registerUser, updateScore
from users import openCloseSession
from random import shuffle #mezclar preguntas de una lista
from PIL import Image, ImageTk #mostra imagenes y manipularlas

class trivia(Tk):
    def __init__(self):
        super().__init__()
    
        self.title("trivia Game") #configurar nombre
        self.geometry("700x650") #configurar ventana

        self.username = ""
        self.password = ""
        self.questions = [] #carga de preguntas
        self.current_questions_index = 0
        self.score = 0

        #para que no se pueda redimencionar la ventana
        self.resizable(False, False)
        #cargar y redimencionar la imagen
        self.imagen = Image.open("imagen.jfif").resize((700, 650))
        self.photo = ImageTk.PhotoImage(self.imagen)
        

        self.show_login()

    def show_login(self):
        #limpiar la ventana
        for widget in self.winfo_children():
            widget.destroy()

        
        # Crear el lienzo y agregar la imagen de fondo
        self.canvas = Canvas(self, width=700, height=650)
        self.canvas.pack(fill="both", expand=True)
        self.canvas.create_image(0, 0, image=self.photo, anchor="nw")

        # Widgets de inicio de sesión sobre el fondo
        self.canvas.create_text(350, 50, text="Iniciar sesión", font=("Arial", 16), fill="white")
        self.canvas.create_text(350, 120, text="Usuario", fill="white")
        self.username_entry = Entry(self)
        self.canvas.create_window(350, 140, window=self.username_entry)

        self.canvas.create_text(350, 180, text="Contraseña", fill="white")      
        self.password_entry = Entry(self, show="*") #agrega campos
        self.canvas.create_window(350, 200, window=self.password_entry)

        # Botones de iniciar sesión y registro
        login_button = Button(self, text="Iniciar sesión", command=self.login)
        self.canvas.create_window(350, 250, window=login_button)

        register_button = Button(self, text="Registrarse", command=self.register)
        self.canvas.create_window(350, 290, window=register_button)

    def login (self):
        #datos de usuario
        self.username=self.username_entry.get().strip()
        self.password=self.password_entry.get().strip()
        #se llama ala funcion openclosesession
        result = openCloseSession(self.username, self.password,  True)
        if result == "seccion iniciada":
            messagebox.showinfo("inicio de sesion", "bienvenido al juego")
            self.category_screen() #ir ala pantalla de la categoria
        else:
            messagebox.showerror("error", result)

    def register(self):
        #obtener datos de usuario
        self.username=self.username_entry.get().strip()
        self.password=self.password_entry.get().strip()
        #se lama ala funcion registerUser para regitar al usuario
        register_result = registerUser(self.username, self.password)
        if register_result=="registrado":
            messagebox.showinfo("registro", "registro exitoso ahora puedes iniciar sesion.")
        else:
            messagebox.showerror("error", "el usuario ya esta registrado.")

    def category_screen(self):
        #limpiar ventana
        for widget in self.winfo_children():
            widget.destroy()

        Label(self, text="elije la categoria", font=("Arial", 16)).pack(pady=10)
        #crear boton para comenzar juego
        Button(self, text="comenzar juego", command=lambda: self.start_trivia("comenzar juego")).pack(pady=5)
        #boton para cerrar sesion
        Button(self, text="cerrar sesion", command=self.logout).pack(pady=20)

    #funcion para cerrar sesion
    def logout(self):
        #llama ala funcion openClosesion
        logout_result=openCloseSession(self.username, self.password, False)
        if logout_result == "Sseccion cerrada":
            messagebox.showinfo("cerrar sesion", "sesion cerrada exitosamente")
            self.show_login()#regresa ala pantalla de inicio
        
        else:
            messagebox.showerror("error", logout_result)
        
    def start_trivia(self, category):
        self.questions = self.load_question(category)
        if not self.questions:
            messagebox.showerror("error", f"no ay preguntas disponibles")
         
        self.current_questions_index = 0
        self.score = 0
        self.show_question()
    
    def load_question(self, category):
        questions = []
        try:
            with open("preguntas.txt", "r", encoding="utf-8") as file: #abre el archivo en lectura ready compatibilidad de acentos y simbolos
                questions_aleatory = []
                for line in file:
                    line = line.strip()
                    if line == "":
                        if questions_aleatory:
                            question_text = questions_aleatory[0]
                            option = questions_aleatory[1:5]
                            correct_answer = questions_aleatory[-1].split(":")[1].strip()
                            questions.append({
                                "question": question_text,
                                "options":option,
                                "answer":correct_answer
                            })
                            questions_aleatory = []
                    
                    else:
                        questions_aleatory.append(line)
            shuffle(questions)#mesclar preguntas
            return questions
        except FileNotFoundError:
            messagebox.showerror("error")
            return[]


    def show_question(self):
        #limpiar la ventana
        for widget in self.winfo_children():
            widget.destroy()
        #obtener la pregunta aleatoria actual en modo de diccionario
        question_data = self.questions[self.current_questions_index]
        #crea la etiqueta de la pregunta
        Label(self, text=question_data["question"], font=("Arial", 12)).pack(padx=10)
        #crear botones de las opciones
        for option in question_data["options"]:
            Button(self, text=option, command=lambda opt=option: self.check_answer(opt)).pack(padx=5)

    def check_answer(self, selected_option):
        #verifica si la respuesta es correcta
        correct_answer = self.questions[self.current_questions_index]["answer"]
        select_letter = selected_option[0]
        #compara la letra seleccionada por la letra correcta
        if select_letter == correct_answer:
            self.score +=1
            messagebox.showinfo("Correcto", "Respuesta correcta")
        else:
            messagebox.showinfo("Incorrecto", f"Respuesta incorrecta. la respuesta correcta es:{correct_answer}")
        
        #ir a la siguiente pregunta
        self.current_questions_index +=1
        if self.current_questions_index < len(self.questions):
            self.show_question()# muestra la siguiente pregunta
        else:
            self.finally_trivia()#termina el juego ya no ay pregunta

    def finally_trivia(self):
        #mostar puntaje final
        messagebox.showinfo("juego terminado", f"tu puntaje actual es:¨{self.score}")
        #actualiza el puntaje
        update_result= updateScore(self.username, self.password, self.score)
        if update_result == "Actualizado":
            messagebox.showinfo("puntaje", "puntaje actualizado.")
        else:
            messagebox.showinfo("error", update_result)
        
        #volver a la pantalla de inicio
        self.show_login()

            
    #ejecutar aplicacion
app = trivia()
app.mainloop()
