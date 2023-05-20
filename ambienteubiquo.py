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
        self.nova_mensagem = 0
        self.mensagem = ''
        self.destino_mensagem = '' 

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
    def listar_usuarios(self, nomeSala, listbox):
        usuarios = self.env.rdp(("usuarios", nomeSala, object))
        print(usuarios)
        print(list(usuarios[2]))

        listbox.delete(0, END)
        for usuario in list(usuarios[2]):
            listbox.insert(END, usuario)
        

        
        
    def listar_dispositivos(self, nomeSala):
        dispositivos = self.env.rdp(("dispositivos", nomeSala, object))
        print(dispositivos)
        print(list(dispositivos[2]))


    # MOVER USUARIO / DISPOSITIVO
    def move_usuario_ambiente(self, ambiente_posterior, usuario, ambiente_anterior):
        nomeUser = usuario
        nomeAmbienteAnterior = ambiente_anterior
        nomeAmbientePosterior = ambiente_posterior

        # Remove a tupla antiga
        integrantes = self.env.inp(("usuarios", nomeAmbienteAnterior, object))
        temp = list(integrantes[2])
        temp.remove(nomeUser)
        self.env.out(("usuarios", nomeAmbienteAnterior, tuple(temp)))
        print("Saiu sala " + nomeAmbienteAnterior)

        # Adiciona a nova tupla 
        usuarios = self.env.inp(("usuarios", nomeAmbientePosterior, object))
        temp = list(usuarios[2])
        temp.append(nomeUser)
        self.env.out(("usuarios", nomeAmbientePosterior, tuple(temp)))
        print("Usuario movido para o ambiente: " + nomeAmbientePosterior)


    def conexao_cliente(self):
        self.env.out(("ambientes", tuple([])))
        newWindow = Toplevel(root)
        newWindow.title("INICIAR JOGO")
        newWindow.geometry("300x170")
        newWindow.config(bg="#4F4F4F")

        newWindow.protocol("WM_DELETE_WINDOW", lambda: self.fecha_janela(newWindow))

        # BG cor de fundo  FG cor da letra
        label_nome_cliente = Label(newWindow, text="BEM VINDO!", font=('Ivy 15 bold'), fg="#FFFFFF", bg="#4F4F4F")
        label_nome_cliente.place(x=40, y=20)

        jogar_button = Button(newWindow, text='Criar Ambiente', font='sans 11 bold', width=12, height=int(1.5),
                              command=lambda: self.criar_ambiente())
        jogar_button.place(x=60, y=95)


    def tela_ambiente(self, nome_ambiente):
        newWindow = Toplevel(root)
        newWindow.title("AMBIENTE!")
        newWindow.geometry("400x300")
        newWindow.config(bg="#4F4F4F")

        newWindow.protocol("WM_DELETE_WINDOW", lambda: self.fecha_tela(newWindow))

        # Create a listbox
        #listbox = Listbox(newWindow, x=70, y=20, width=10, height=10, selectmode=MULTIPLE)        
        listbox = Listbox(newWindow)
        listbox.place(x=180, y=20)  

        # BG cor de fundo  FG cor da letra
        label_nome_cliente = Label(newWindow, text="AMBIENTE", font=('Ivy 15 bold'), fg="#FFFFFF", bg="#4F4F4F")
        label_nome_cliente.place(x=20, y=5)

        label_nome_ambiente = Label(newWindow, text=nome_ambiente, font=('Ivy 15 bold'), fg="#FFFFFF", bg="#4F4F4F")
        label_nome_ambiente.place(x=20, y=40)

        jogar_button = Button(newWindow, text='Criar Usuário', font='sans 11 bold', width=12, height=int(1.5),
                              command=lambda: self.criar_usuario(nome_ambiente))
        jogar_button.place(x=20, y=95)

        jogar_button = Button(newWindow, text='Atualizar Usuarios', font='sans 11 bold', width=12, height=int(1.5),
                        command=lambda: self.listar_usuarios(nome_ambiente, listbox))
        jogar_button.place(x=20, y=130)

        jogar_button = Button(newWindow, text='Mover Usuario', font='sans 11 bold', width=12, height=int(1.5),
                        command=lambda: self.tela_mover_usuario(listbox, nome_ambiente))
        jogar_button.place(x=20, y=165)

        jogar_button = Button(newWindow, text='Chat Usuario', font='sans 11 bold', width=12, height=int(1.5),
                command=lambda: self.tela_chat_usuario(listbox, nome_ambiente))
        jogar_button.place(x=20, y=200)

    def tela_mover_usuario(self, listbox, nome_ambiente):
        newWindow = Toplevel(root)
        newWindow.title("MOVER USUARIO!")
        newWindow.geometry("400x300")
        newWindow.config(bg="#4F4F4F")

        newWindow.protocol("WM_DELETE_WINDOW", lambda: self.fecha_tela(newWindow))

        label_nome_cliente = Label(newWindow, text="Mover " + listbox.get(ACTIVE) + " para o ambiente:", font=('Ivy 15 bold'), fg="#FFFFFF", bg="#4F4F4F")
        label_nome_cliente.place(x=40, y=20)

        ambiente_name_input = Entry(newWindow, width=27)
        ambiente_name_input.place(x=60, y=60)

        jogar_button = Button(newWindow, text='Mover', font='sans 11 bold', width=12, height=int(1.5),
                              command=lambda: self.move_usuario_ambiente(str(ambiente_name_input.get()), listbox.get(ACTIVE), nome_ambiente))
        jogar_button.place(x=80, y=95)

        print("Esporte: " + listbox.get(ACTIVE))

    def tela_chat_usuario(self, nome_usuario, nome_ambiente):
        newWindow = Toplevel(root)
        newWindow.title("BEM VINDO!")
        newWindow.geometry("660x390")
        frame_chat = Frame(newWindow, width=310, height=390, bg="#4F4F4F", pady=0, padx=0)
        frame_chat.grid(row=1, column=0)

        #    newWindow.protocol("WM_DELETE_WINDOW", mostra_janela_SAIR_PARTIDA)

        text_area_chat = ScrolledText(frame_chat, wrap=WORD, width=38, height=15, font=("Callibri", 8))
        text_area_chat.place(x=15, y=90)
        text_area_chat.focus()

        label_peca = Label(frame_chat, text="CHAT", height=1, padx=0, relief="flat", anchor="center",
                           font=('Ivy 25 bold'),
                        bg="#4F4F4F",fg="#FFFFFF")
        label_peca.place(x=100, y=10)

        label_mensagem = Entry(frame_chat, width=34)
        label_mensagem.pack(padx=10, pady=10)
        label_mensagem.place(x=15, y=300)

        button_envia_mensagem = Button(frame_chat, text='ENVIAR', command=lambda: self.envia_mensagem(str(label_mensagem.get()), nome_usuario, nome_ambiente))
        button_envia_mensagem.place(x=120, y=330)

        self.threadRecebe_Mensagens_func(text_area_chat, nome_usuario, nome_ambiente)

    def threadRecebe_Mensagens_func(self, text_area_chat, nome_usuario, nome_ambiente):
        threading.Thread(target=self.recebe_mensagens, args=(text_area_chat, nome_usuario, nome_ambiente,)).start()

    def envia_mensagem(self, entry_widget, nome_usuario, nome_ambiente):
        msg = entry_widget
        if(msg != ""):
            self.nova_mensagem = 1;
            self.mensagem = entry_widget
            self.destino_mensagem = nome_ambiente
            """ mandaMensagem(tse, nome_sala_chat, nome_usuario, destinatario, msg)
            flag_Monitora_Novas_Mensagens = 1 """

    """    def mandaMensagem(ts, nomeSala, remetente, destinatario, mensagem):

        mensagens = ts.inp(("SALA", nomeSala, object))
        temp = list(mensagens[2])
        temp.clear()
        
        if destinatario != "Todos":
            temp.append((destinatario,"<" + remetente + " - *Msg Privada para vc>: " + mensagem),)
        else:
            temp.append((destinatario,"<" + remetente + ">: " + mensagem),)
            
        ts.out(("SALA", nomeSala, tuple(temp)))
        print("Destinatario " + str(destinatario))
        print("Mandou MSG " + str(temp)) """

    def recebe_mensagens(self, ScrolledText, listbox, salaAtual):        
        while(True):
            if self.nova_mensagem == 1 and self.destino_mensagem == salaAtual:
                ScrolledText.insert(tk.INSERT, self.mensagem)
                print(listbox.get(ACTIVE) + " recebeu a msg!")
                self.nova_mensagem = 0
            else:
                pass

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