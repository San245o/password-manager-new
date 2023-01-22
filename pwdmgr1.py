import tkinter
import mysql.connector  #pip install  mysql-connector
from tkinter import *
from functools import partial
from tkinter import messagebox
from PIL import ImageTk,Image
from cryptography.fernet import Fernet #pip install cryptography
from tkinter import ttk
import pyperclip #pip install pyperclip 
import random
from tabulate import tabulate #pip install tabulate

'''
('CREATE DATABASE pwd IF NOT EXISTS;')
('USE pwd;')
('CREATE TABLE encrypt_decrypt(encryption_key varchar(200),decrypt_value text);')
('CREATE TABLE data(user_name varchar(100), site_name varchar(100), password varchar(100));')
'''    

mydb = mysql.connector.connect(host="localhost", user = "root",passwd = "sankeerthsanvi",database = 'pwd')
mycursor = mydb.cursor()

def unsuccess_msg():
    return messagebox.showinfo("error", "passwords cannot match!")
def delete_msg():
    return messagebox.showinfo('confirmation','all records deleted')
def success_msg():
    return messagebox.showinfo("saved", "Saved Successfully")
def copy():
    return messagebox.showinfo("clipboard","Copied to clipboard!")

tkWindow = Tk()  
tkWindow.geometry('810x432')  
tkWindow.title('pwd manager')
tkWindow.configure(bg='#12c4c0')
tkWindow.resizable(0,0)

def display():
    new = Toplevel(tkWindow)
    new.title('display')
    new.geometry('800x500')
    new.config(bg ='black' )

    mycursor.execute('SELECT * FROM DATA LIMIT 15')
    my_cursor=mycursor.fetchall()
    t = tabulate(my_cursor,headers = ['Site Name','Username','Password'],tablefmt = "pretty")
    e = Label(new,font = ('consolas 14'),fg = 'cyan',text = t,bg ='black').place(x = 0,y = 0)
    y = 60

    def encrypt(record):

        Key = Fernet.generate_key()
        fernet = Fernet(Key)
        password = record[0]
        encrypt_message = str(fernet.encrypt(password.encode()))
        real_encrypt = (encrypt_message.replace("b'",'')).replace("'",'')
        mycursor.execute(f'INSERT INTO encrypt_decrypt Values("{real_encrypt}","{password}")')
        mydb.commit()

    for index, record in enumerate(my_cursor):
        encrypt_button = Button(new, text="Encrypt", command = partial(encrypt,record),
                                fg = 'cyan',bg = 'black',border = 0,
                                font = ('Segoe_UI 12 underline'),activeforeground='#E26D5A',activebackground='black')
        encrypt_button.place(x = 670,y = y)
        y += 24


def new_pass():
    global w
    w=Frame(tkWindow,width=810,height=415,bg='#5A5A5A')
    w.place(x=50,y=50)

    sitelabel = Label(tkWindow, text = "Site Name : ",height = 4,bg = '#5A5A5A',width = 30,font=('Bahnschrift','16','bold'),fg = 'cyan')
    sitelabel.place(x = 280, y = 55)
    siteEntry = Entry(tkWindow,width = 22,relief = 'solid',font = ('Bahnschrift 12'),border = 2,selectbackground='#00DDFF',selectforeground='black')
    siteEntry.place(x = 355, y = 120)


    usernameLabel = Label(tkWindow, text="User Name : ",height = 2,width = 30,bg = '#5A5A5A',
                            font=('Bahnschrift','16','bold'),fg = 'cyan')
    usernameLabel.place(x = 280, y = 155)
    usernameEntry = Entry(tkWindow,width =22,relief = 'solid',font = ('Bahnschrift 12'),selectbackground='#00DDFF',selectforeground='black',border = 2)
    usernameEntry.place(x = 355, y = 200)

    passwordLabel = Label(tkWindow,text="Password : ",height = 2,width  = 30,bg = '#5A5A5A',font=('Bahnschrift','16','bold'),fg = 'cyan')
    passwordLabel.place(x = 280,y = 235)  
    passwordEntry = Entry(tkWindow,width = 22, show='*',relief = 'solid',font = ('Bahnschrift 12'),border = 2,selectbackground='#00DDFF',selectforeground='black')
    passwordEntry.place(x = 355,y = 280)   


    def save_data():
        site_value = siteEntry.get()
        user_value = usernameEntry.get()
        pass_value = passwordEntry.get()
        mycursor.execute(f"INSERT INTO DATA VALUES('{site_value}','{user_value}','{pass_value}')")
        mydb.commit()
        success_msg()

    saveButton = Button(tkWindow, text="save", command=save_data,border = 8,bg = '#28b3c4',font = ('consolas','14','bold'),activebackground='#64C2C2')
    saveButton.place(x =  250,y=330)
    display_button = Button(tkWindow,text = 'display & encrypt records',command = display,border = 8,bg = '#28b3c4',
                                font = ('consolas','14','bold'),activebackground='#64C2C2')
    display_button.place(x =470  ,y=330)

new_pass()

def show_encrypt():
    s = Toplevel(tkWindow)
    s.title('Display Encrypted records')
    s.geometry('800x450')
    s.config(bg ='black' )
    Scroll  = Scrollbar(s,orient = 'vertical')
    Scroll.pack(side = RIGHT,fill = Y)
    mycursor.execute('SELECT * FROM ENCRYPT_DECRYPT')
    my_cursor = mycursor.fetchall()
    t = tabulate(my_cursor,headers = ['Encrypted text','site_name'],tablefmt = "pretty",maxcolwidths=[40, None])
    display = Label(s,font = ('consolas 12'),fg = 'cyan',text = t,bg = 'black')
    display.place(x=0,y=0)
    y = 60
    def copy2(record):
        pyperclip.copy(record[0])
        copy()
    for index,record in enumerate(my_cursor):
        copy_button = Button(s,text = 'copy',command = partial(copy2,record),
                            fg ='cyan',bg = 'black',border = 1,
                            font = ('consolas 13 '))
        copy_button.place(x=600,y=y)
        y+=60



def delete():
    query = 'delete from data'
    mycursor.execute(query)
    mydb.commit()
    delete_msg()

def decrypt():
    z = Toplevel(tkWindow)
    z .title('decrypt')
    z.geometry('700x200')
    z.config(bg ='#5A5A5A' )
    dlabel = Label(z,text = 'enter text to be decrypted : ',bg = '#5A5A5A',font=('consolas','20','bold'),fg = 'cyan').place(x =150 ,y=40)
    dentry = Entry(z,width = 40,font = ('consolas 12 bold'),relief = 'solid')
    dentry.place(x=170,y=90)
    def get_value():
        dvalue = dentry.get()
        query = f'SELECT site_name from ENCRYPT_DECRYPT WHERE  encryption_key = "{dvalue}"'
        mycursor.execute(query)
        value = mycursor.fetchone()
        dnC = (f'The decrypted value is : \n "{value[0]}" ')
        def copy3(record):
            pyperclip.copy(record)  
            copy()
            z.destroy()
        Label(z, text=dnC, font= ('Consolas 13 bold'),bg='#3DAAB6').pack(ipadx=20, ipady=20, padx=20, pady=20,fill=tkinter.BOTH, expand=True)
        button = Button(z,text = 'copy!',font = ('consolas 10 bold'),relief = 'solid',border = 2,command = partial(copy3,value[0]),bg = 'grey',fg = 'black')
        button.place(x=320,y=130)
    button = Button(z,text = 'decrypt!',command = get_value,width = 10,border = 5,bg = '#5A5A5A',font = ('consolas 11 bold'),activebackground = '#5B7878').place(x =310,y = 140)



def random_pass():
    x = Toplevel(tkWindow)
    x .title('generate a random password')
    x.geometry('450x240')
    x.config(bg ='#5A5A5A' )
    dlabel = Label(x,text = 'enter difficulty of the password : ',bg = '#5A5A5A',font=('consolas','11','bold'),fg = 'cyan').place(x =100 ,y=50)
    char = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ1234567890!@#$%^&*()<>.,"
    def copy1():
        x.destroy()
        return messagebox.showinfo("clipboard","Copied to clipboard!")

    def pwd():
        for i in range(0,5):
            password = ""
            for i in range(0,5):
                password_char = random.choice(char[:52])
                password = password + password_char
        q = 'your password is : {}'.format(password)
        Label(x,text = q,font= ('Consolas 13 bold'),bg='#3DAAB6').pack(ipadx=10, ipady=10, padx=10, pady=10,fill=tkinter.BOTH, expand=True)
        B = Button(x,text= 'copy to clipboard',width = 15,border = 3,bg = '#19474D',command=copy1)
        B.place(x =170,y = 140)
        pyperclip.copy(password)

    def pwd0():
        for i in range(0,10):
            password = ""
            for i in range(0,10):
                password_char = random.choice(char[:62])
                password = password + password_char
        q = 'your password is : {}'.format(password)
        Label(x,text = q,font= ('Consolas 13 bold'),bg='#3DAAB6').pack(ipadx=10, ipady=10, padx=10, pady=10,fill=tkinter.BOTH, expand=True)
        B = Button(x,text= 'copy to clipboard',width = 15,border = 3,bg = '#19474D',command=copy1)
        B.place(x =170,y = 140)
        pyperclip.copy(password)

    def pwd1():
        for i in range(0,15):
            password = ""
            for i in range(0,15):
                password_char = random.choice(char)
                password = password + password_char
        q = 'your password is : {}'.format(password)
        Label(x,text = q,font= ('Consolas 13 bold'),bg='#3DAAB6').pack(ipadx=10, ipady=10, padx=10, pady=10,fill=tkinter.BOTH, expand=True)
        B = Button(x,text= 'copy to clipboard',width = 15,border = 3,bg = '#19474D',command=copy1)
        B.place(x =170,y = 140)
        pyperclip.copy(password)

    Button(x,text = 'easy',command = pwd,width = 10,border = 5,bg = '#5A5A5A',activebackground = '#5B7878').place(x =75,y = 120)
    Button(x,text = 'medium',command = pwd0,width = 10,border = 5,bg = '#5A5A5A',activebackground = '#5B7878').place(x =180,y = 120)
    Button(x,text = 'hard',command = pwd1,width = 10,border = 5,bg = '#5A5A5A',activebackground = '#5B7878').place(x=295,y=120)  # type: ignore


def toggle_win():
    f1=Frame(tkWindow ,width=286,height=500,bg='#12c4c0')
    f1.place(x=0,y=0)


    #buttons
    def bttn(x,y,text,bcolor,fcolor,cmd):
     
        def on_entera(e):
            myButton1['background'] = bcolor #ffcc66
            myButton1['foreground']= '#5A5A5A'  #000d33

        def on_leavea(e):
            myButton1['background'] = fcolor
            myButton1['foreground']= 'black'

        myButton1 = Button(f1,text=text,
                       width=35,
                       height=2,
                       fg='#262626',
                       border=0,
                       bg=fcolor,
                       activeforeground='#262626',
                       activebackground=bcolor,            
                        command=cmd,font = ('Franklin_Gothic_Demi_Cond 10 bold'))
                      
        myButton1.bind("<Enter>", on_entera)
        myButton1.bind("<Leave>", on_leavea)

        myButton1.place(x=x,y=y)

    bttn(0,90,'S H O W   E N C R Y P T E D   R E C O R D S','#0f9d9a','#12c4c0',show_encrypt)
    bttn(0,165,'D E C R Y P T ','#0f9d9a','#12c4c0',decrypt)
    bttn(0,240,'G E N E R A T E   A   P A S S W O R D ','#0f9d9a','#12c4c0',random_pass)
    bttn(0,315,'D E L E T E   R E C O R D S ','#0f9d9a','#12c4c0',delete)

    #
    def dele():
        f1.destroy()

    global img2
    img2 = ImageTk.PhotoImage(Image.open("close.png"))

    Button(f1,
           image=img2,
           border=0,
           command=dele,
           bg='#12c4c0',
           activebackground='#12c4c0').place(x=0,y=0)
    

img1 = ImageTk.PhotoImage(Image.open("open5.png"))

Button(tkWindow,image=img1,
       command=toggle_win,
       border=0,
       bg='#12c4c0',
       activebackground='#12c4c0').place(x=0,y=0)

def update_password():
    w=Frame(tkWindow,width=810,height=415,bg='#28b3c4')
    w.place(x=50,y=50)


    usernamelabel = Label(tkWindow, text = "User name : ",height = 2,bg = '#28b3c4',width = 17,font=('Bahnschrift','16','bold'))
    usernamelabel.place(x = 360, y = 78)
    userentry = Entry(tkWindow,width = 22,relief = 'solid',font = ('Bahnschrift 12'),border=2,selectbackground='#00DDFF',selectforeground='black')
    userentry.place(x = 360, y = 120)


    pass_1 = Label(tkWindow, text="Old password : ",height = 2,width = 17,bg = '#28b3c4',font=('Bahnschrift','16','bold'))
    pass_1.place(x = 360,y=160)
    pass_1_Entry = Entry(tkWindow,width = 22,relief= 'solid',font = ('Bahnschrift 12'),border = 2,selectbackground='#00DDFF',selectforeground='black')
    pass_1_Entry.place(x = 360, y = 200)  


    pass_2 = Label(tkWindow,text="New password : ",height = 2,width  = 17,bg = '#28b3c4',font=('Bahnschrift','16','bold'))
    pass_2.place(x =360 ,y = 240)
    pass_2_Entry = Entry(tkWindow,width = 22, show='*',relief = 'solid',font = ('Bahnschrift 12'),border =2,selectbackground='#00DDFF',selectforeground='black')
    pass_2_Entry.place(x=360,y = 280)

    def save_value():
        user_value = userentry.get()
        pass_1_Entry_value = pass_1_Entry.get()
        pass_2_Entry_Value = pass_2_Entry.get()
        mycursor.execute(f'UPDATE data SET password = "{pass_2_Entry_Value}" WHERE  user_name = "{user_value}"')
        mydb.commit()
        success_msg()

    saveButton = Button(tkWindow, text="save", command=save_value,border = 8,bg = '#5A5A5A',font = ('Bahnschrift','13','bold'),activebackground='#5B7878')
    saveButton.place(x =  430,y=330) 

Button(tkWindow,width=48,height=2,text='U P D A T E   P A S S W O R D',pady=4,border=0, command = update_password,bg='#28b3c4',fg='black',
            activebackground='#408FA0',activeforeground='white',font = ('Bahnschrift 12 ')).place(x=425,y=0)
Button(tkWindow,width=44,height=2,text='S T O R E  P A S S W O R D',pady=4,border=0, command = new_pass,bg='#5A5A5A',
            fg='cyan',activebackground='#408FA0',activeforeground='white',font = ('Bahnschrift 12 ')).place(x=50,y=0)

mycursor.execute("select * from data")
for i in  mycursor:
    print(i)

tkWindow.mainloop()
mydb.close()

