import socket
from threading import Thread
from tkinter import *

# nickname = input("Choose your nickname: ")

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

ip_address = '127.0.0.1'
port = 8000

client.connect((ip_address, port))

print("Connected with the server...")

class GUI:
    def __init__(self):
        self.Window = Tk()
        self.Window.withdraw()

        self.login = Toplevel()
        self.login.title("Login")

        self.login.resizable(width=False, height=False)
        self.login.configure(width=400, height=300)
        
        self.pls = Label(self.login,
					text = "Please login to continue",
					justify = CENTER,
					font = "Helvetica 14 bold")
        self.pls.place( relheight = 0.15,
                        relx = 0.2,
                        rely = 0.07)

        self.labelName = Label(self.login,
							text = "Name: ",
							font = "Helvetica 12")
        self.labelName.place(   relheight = 0.2,
							    relx = 0.1,
							    rely = 0.2)

        self.entryName = Entry(self.login,
							font = "Helvetica 14")
        self.entryName.place(relwidth = 0.4,
							relheight = 0.12,
							relx = 0.35,
							rely = 0.2)
        self.entryName.focus()

        self.go = Button(self.login,
						text = "CONTINUE",
						font = "Helvetica 14 bold",
						command = lambda: self.goAhead(self.entryName.get()))
        self.go.place(  relx = 0.4,
					    rely = 0.55)
        
        self.Window.mainloop()

    def goAhead(self, name):
        self.login.destroy()
        self.layout(name)
        rcv = Thread(target=self.receive)
        rcv.start()

    def layout(self,name):
        self.name=name
        self.Window.deiconify()
        self.Window.title("Chatroom")
        self.Window.resizable(width=True,height=True)
        self.Window.configure(width=500,height=500,bg="salmon")
        self.labelHead=Label(self.Window,bg="skyblue",text=self.name,pady=5,font="Helvetica 13 bold")
        self.labelHead.place(relwidth=1)

        self.line=Label(self.Window,width=450,bg="black")
        self.line.place(relwidth=1,rely=0.07,relheight=0.01)
        self.textcons=Text(self.Window,width=20,height=2,bg="skyblue",padx=5, pady=5,font="Helvetica 14")
        self.textcons.place(relheight=0.7,relwidth=1,rely=0.08)

        self.labelBottom=Label(self.Window,bg="skyblue",height=80)
        self.labelBottom.place(relwidth=1,rely=0.8)
        self.entryMsg=Entry(self.labelBottom,bg="skyblue",font="Helvetica 45")
        self.entryMsg.place(relwidth=0.7,relheight=0.06,rely=0.008,relx=0.01)
        self.entryMsg.focus()

        self.buttonMsg = Button(self.labelBottom,text = "SEND",width=20,font = "Helvetica 14 bold",command = lambda: self.sendButton(self.entryMsg.get()))
        self.buttonMsg.place(  relx = 0.7, rely = 0.008,relheight=0.06,relwidth=0.2)
        self.textcons.config(cursor="arrow")
        scrollbar=Scrollbar(self.textcons)
        scrollbar.place(relheight=1,relx=0.9)
        scrollbar.config(command=self.textcons.yview)
        self.textcons.config(state=DISABLED)

    def sendButton(self,msg):
         self.textcons.config(state=DISABLED)
         self.msg=msg
         self.entryMsg.delete(0,END)
         snd=Thread(target=self.write)
         snd.start()

    def show_message(self,message):
        self.textcons.config(state=NORMAL)
        self.textcons.insert(END,message+"\n\n")
        self.textcons.config(state=DISABLED)
        self.textcons.see(END)


    def receive(self):
        while True:
            try:
                message = client.recv(2048).decode('utf-8')
                if message == 'NICKNAME':
                    client.send(self.name.encode('utf-8'))
                else:
                    pass
            except:
                print("An error occured!")
                client.close()
                break
    
    def write(self):
        self.textcons.config(state=DISABLED)
        while True:
            message = (f"{self.name}:{self.msg}")
            client.send(message.encode('utf-8'))
            self.show_message(message)
            break

g = GUI()

# def write():
#     while True:
#         message = '{}: {}'.format(nickname, input(''))
#         client.send(message.encode('utf-8'))

# receive_thread = Thread(target=receive)
# receive_thread.start()
# write_thread = Thread(target=write)
# write_thread.start()
