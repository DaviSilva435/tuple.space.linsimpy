import threading

import Pyro4
import json

from tkinter import *
from tkinter.scrolledtext import ScrolledText
import tkinter as tk

import linsimpy

"""
Cria objeto "Tkinter"/"Tk"
"""
root = tk.Tk()
root.withdraw()

class Project():

    def __init__(self):
        self.server = Pyro4.core.Proxy('PYRONAME:project.tuple')
        self.env = linsimpy.TupleSpaceEnvironment()
        self.abort = 0
        self.contador_ambiente = 1
        self.contador_dispositivo = 1
        self.contador_usuario = 1

    # CRIAR AMBIENTE / USUARIO / DISPOSITIVO
    def criar_ambiente(self):
        nome_ambiente = f'amb{self.contador_ambiente}'
        self.contador_ambiente += 1
        ambientes = self.env.inp(("ambientes", object))
        temp = list(ambientes[1])
        temp.append(nome_ambiente)
        self.env.out(("ambientes", tuple(temp)))
        self.env.out(("usuarios", nome_ambiente, tuple([])))
        self.env.out(("dispositivos", nome_ambiente, tuple([])))
        print("ambientes: " + str(temp))
        self.tela_ambiente(nome_ambiente)

    def criar_usuario(self, ambiente):
        nome_ambiente = ambiente
        nome_usuario = f'user{self.contador_usuario}'
        self.contador_usuario += 1
        usuarios = self.env.inp(("usuarios", nome_ambiente, object))
        temp = list(usuarios[2])
        temp.append(nome_usuario)
        self.env.out(("usuarios", nome_ambiente, tuple(temp)))
        print("Usuario criado no ambiente: " + nome_ambiente)
        #self.tela_usuario(nome_usuario)

    def criar_dispositivo(self, ambiente):
        nome_ambiente = ambiente
        nome_usuario = f'user{self.contador_usuario}'
        self.contador_usuario += 1
        dispositivos = self.env.inp(("dispositivos", nome_ambiente, object))
        temp = list(dispositivos[2])
        temp.append(nome_usuario)
        self.env.out(("dispositivos", nome_ambiente, tuple(temp)))
        print("Dispositivos criado no ambiente: " + nome_ambiente)

    # LISTAR AMBIENTE / USUARIO / DISPOSITIVO
    def listar_usuarios(self, nomeSala):
        usuarios = self.env.rdp(("usuarios", nomeSala, object))
        print(usuarios)
        print(list(usuarios[2]))

    def listar_dispositivos(self, nomeSala):
        dispositivos = self.env.rdp(("dispositivos", nomeSala, object))
        print(dispositivos)
        print(list(dispositivos[2]))


    # MOVER USUARIO / DISPOSITIVO
    def move_usuario_ambiente(self):
        nomeUser = 'user1'
        nomeSala = 'amb1'
        novaSala = 'amb2'

        # Remove a tupla antiga
        integrantes = self.env.inp(("usuarios", nomeSala, object))
        temp = list(integrantes[2])
        temp.remove(nomeUser)
        self.env.out(("usuarios", nomeSala, tuple(temp)))
        print("Saiu sala " + nomeSala)


        # Adiciona a nova tupla 
        usuarios = self.env.inp(("usuarios", novaSala, object))
        temp = list(usuarios[2])
        temp.append(nomeUser)
        self.env.out(("usuarios", novaSala, tuple(temp)))
        print("Usuario criado no ambiente: " + novaSala)


    def conexao_cliente(self):
        self.env.out(("ambientes", tuple([])))
        newWindow = Toplevel(root)
        newWindow.title("INICIAR JOGO")
        newWindow.geometry("300x170")
        newWindow.config(bg="#4F4F4F")

        newWindow.protocol("WM_DELETE_WINDOW", lambda: self.fecha_janela(newWindow))

        # BG cor de fundo  FG cor da letra
        label_nome_cliente = Label(newWindow, text="DIGITE SEU NOME:", font=('Ivy 15 bold'), fg="#FFFFFF", bg="#4F4F4F")
        label_nome_cliente.place(x=40, y=20)

        jogar_button = Button(newWindow, text='Criar Ambiente', font='sans 11 bold', width=12, height=int(1.5),
                              command=lambda: self.criar_ambiente())
        jogar_button.place(x=80, y=95)


        jogar_button = Button(newWindow, text='Listar Ambientes', font='sans 11 bold', width=12, height=int(1.5),
                        command=lambda: self.listar_ambiente())
        jogar_button.place(x=80, y=130)


    def tela_ambiente(self, nome_ambiente):
        newWindow = Toplevel(root)
        newWindow.title("AMBIENTE!")
        newWindow.geometry("300x300")
        newWindow.config(bg="#4F4F4F")

        newWindow.protocol("WM_DELETE_WINDOW", lambda: self.fecha_tela(newWindow))

        # BG cor de fundo  FG cor da letra
        label_nome_cliente = Label(newWindow, text=nome_ambiente, font=('Ivy 15 bold'), fg="#FFFFFF", bg="#4F4F4F")
        label_nome_cliente.place(x=40, y=20)

        jogar_button = Button(newWindow, text='Criar Usuário', font='sans 11 bold', width=12, height=int(1.5),
                              command=lambda: self.criar_usuario(nome_ambiente))
        jogar_button.place(x=80, y=95)

        jogar_button = Button(newWindow, text='Listar Usuarios', font='sans 11 bold', width=12, height=int(1.5),
                        command=lambda: self.listar_usuarios(nome_ambiente))
        jogar_button.place(x=80, y=130)

        jogar_button = Button(newWindow, text='Listar Usuarios', font='sans 11 bold', width=12, height=int(1.5),
                        command=lambda: self.move_usuario_ambiente())
        jogar_button.place(x=80, y=165)

    def tela_usuario(self, nome):
        newWindow = Toplevel(root)
        newWindow.title("AMBIENTE!")
        newWindow.geometry("300x150")
        newWindow.config(bg="#4F4F4F")

        newWindow.protocol("WM_DELETE_WINDOW", lambda: self.fecha_tela(newWindow))

        # BG cor de fundo  FG cor da letra
        label_nome_cliente = Label(newWindow, text=nome, font=('Ivy 15 bold'), fg="#FFFFFF", bg="#4F4F4F")
        label_nome_cliente.place(x=40, y=20)

        jogar_button = Button(newWindow, text='Criar Ambiente', font='sans 11 bold', width=12, height=int(1.5),
                              command=lambda: self.criar_ambiente())



    def fecha_janela(self, Toplevel):
        Toplevel.destroy()
        Toplevel.quit()
        root.destroy()

    def fecha_tela(self, Toplevel):
        Toplevel.destroy()

class DaemonThread(threading.Thread):
    def __init__(self, chatter):
        threading.Thread.__init__(self)
        self.chatter = chatter
        self.setDaemon(True)

    def run(self):
        with Pyro4.core.Daemon() as daemon:
            daemon.register(self.chatter)
            daemon.requestLoop(lambda: not self.chatter.abort)

if __name__ == "__main__":
    p = Project()
    daemonthread = DaemonThread(p)
    daemonthread.start()
    p.conexao_cliente()
    root.mainloop()