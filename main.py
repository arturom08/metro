import tkinter as tk

from tkinter import *
from tkinter import ttk
from tkinter import messagebox

class FormularioClientes:
    def Formulario():

        try:
            base = Tk()
            base.geometry("1200x300")
            base.title("formulario Python")

            groupBox = LabelFrame(base,text="Datos del personal",padx=5,pady=5)
            groupBox.grid(row=0,column=0,padx=10,pady=10)

            labelId=Label(groupBox,text="Id:",width=13,font=("arial",12)).grid(row=0,column=0)

            base.mainloop()

        except ValueError as error:
            print("Error al mostrar la interfaz, error: {}".format(error))


    Formulario()