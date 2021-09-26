from tkinter import *
from PIL import ImageTk,Image
from os.path import isfile
from tkinter import messagebox
import main


def play(root,username):                                                                        #function to close game menu window and starts the main game
    '''Closes game menu and opens  main game'''
    root.destroy()
    main.game(username, 'main_game')                                                             #opens main game


def game(index):                                                                                #function for the window of game menu
    '''creates game menu window on screen'''
    root=Tk()
    root.title('MENU')
    root.geometry('780x436')
    root.resizable(False,False)
    bg=ImageTk.PhotoImage(file='Images//gtabg.png')
    Label(root,image=bg).grid(row=0,column=0)
    with open("usernames//username.txt") as file:                                                          #opens the file to read and get usernames
        list_users = file.readlines()
        user_profile = eval(list_users[index])
        username = user_profile['username']

    root.iconbitmap('Images//car.ico')
    frame=LabelFrame(root,bg='#030404')                                                         #creates a frame to place buttons and entries on the screen
    frame.grid(row=0,column=0,ipadx=30,ipady=20)
   
    b1=Button(frame,text=' Play Game ',bg='#921426',fg='white',command=lambda: play(root,username),font=('Times New Roman',16 ),activebackground='#921426')
    b1.pack(pady=10)
        
    b2=Button(frame,text='  Exit  ',bg='#921426',fg='white',command=root.destroy,font=('Times New Roman',16),width=9,height=1,activebackground='#921426')
    b2.pack(pady=10)
   
    

    root.mainloop()

                 
def encrypt(text):      #function for encryption
    '''encrypt text according to rules'''
    rules = {'a':'o', 'b':'c',  'd':'w',  'e':'l',  'f':'x',  'g':'n',  'h':'d',  'char':'y',             #rules for the encryption
            'j':'p', 'k':'a',  'l':'u',  'm':'j',  'n':'v',  'o':'b', 'p':'k',   'q':'e',  'r':'t',
            's':'h', 't':'s',  'u':'f',  'v':'q',  'w':'g',  'x':'z', 'y':'char','   z':'r',  'A':'O',
            'B':'C',  'D':'W',  'E':'L',  'F':'X',  'G':'N',  'H':'D', 'I':'Y',   'J':'P',  'K':'A',
            'L':'U',   'M':'J',  'N':'V',  'O':'B',  'P':'K',  'Q':'E', 'R':'T',  'S':'H',   'T':'S',
            'U':'F',   'V':'Q',   'W':'G',  'X':'Z',  'Y':'I',  'Z':'R', '1':'0',  '2':'3',   '3':'5',
            '4':'9',   '5':'1','  6':'8',    '7':'4',  '8':'7',  '9':'2', '0':'6'

            }
    encrypted = ""
    for char in text:
        encrypted += rules.get(char, char)
    return encrypted

    
def check_username(user):                                                               #function to check whether entered username is present in the file or not
    '''checks username is present in the file or not'''
    data=open("usernames//username.txt",'r')
    usernames=[]
    info=True
    index=0
    for player_data in data.readlines():
        players = eval(player_data)
        usernames.append(players.get("username"))
    for username in usernames:
        if user==username:
            info= False
            break
        index+=1
    return info,index


def sign_game(coins,entry_use,password_sign,sign_up):                                            #function for the signup procedure
    '''creates files of new user'''
    user_name = entry_use.get()
    pass_user = password_sign.get()
    user_dict={}
    user_profile = {'username': user_name , 'coins': coins}
    encrypted_password = encrypt(pass_user)                                                     #encryption of password
    user_dict["username"], user_dict["encrypted_password"] = user_name, encrypted_password
    if isfile('usernames//username.txt'):
        exp,index=check_username(user_name)
        if not exp:                                                                             #check signup id already exists or not
            messagebox.showwarning('signup error','This username already exists.')
        else:                                                                                  
            with open('usernames//username.txt','a') as data:
                data.write(f"{user_dict}\n")                                                    #appending user's information in data

            with open(f"profiles//profile_{user_name}.txt", "a") as file:
                file.write(f'{user_profile}\n')
                    
    else:
        with open('usernames//username.txt','a') as data:
            data.write(f"{user_dict}\n")                                                        #appending user's information in data

        with open(f"profiles//profile_{user_name}.txt", "a") as file:
                    file.write(f'{user_profile}\n')
    sign_up.destroy()


def signup(back):                                                                               #function for the sign_up window
    '''creates window of signup menu'''
        
    coins = 500
    sign_up=Toplevel()
    sign_up.title('Sign_up')
    sign_up.iconbitmap('Images//contract.ico')
       
    Label(sign_up,image=back).grid(row=0,column=0)
    frame_sign=LabelFrame(sign_up,bg='#030404')                                                 #creates a frame to place buttons and entries on the screen
    frame_sign.grid(row=0,column=0,ipadx=30,ipady=20)
    sign_lb=Label(frame_sign,text='SIGNUP',font=('Time New Roman',16,'bold'),bg='#030404',fg='white')
    sign_lb.pack()
    user_name=Label(frame_sign,text='Username: ',bg='#030404',fg='white')
    user_name.pack()
    entry_use=Entry(frame_sign,width=15)
    entry_use.pack()
    sign_lbl2=Label(frame_sign,text='Passward: ',bg='#030404',fg='white')
    sign_lbl2.pack()
    password_sign=Entry(frame_sign,width=15,show='*')
    password_sign.pack()
    sign_bt=Button(frame_sign,text='REGISTER',font=('Time New Roman',12,'bold'),bg='#921426',activebackground='#921426',fg='white',command=lambda:sign_game(coins,entry_use,password_sign,sign_up))
    sign_bt.pack(pady=10)

def open_game(log_in,index):                                                                #function to destroy log_in window and open game menu window
    '''closes login menu and opens game menu'''
    log_in.destroy()
    game(index)  
    

def log_game(entry,password,log_in):                                                        #function to check whether the login id is valid or not
    '''checks user's login credentials''' 
    user_name=entry.get()
    pass_user=password.get()
    if isfile('usernames//username.txt'):
        exp,index=check_username(user_name)
        if exp:
            messagebox.showwarning('login info','This username is not found\nPlease Signup first')   #to show invalid login
        else:             
            
            encrypt_password = encrypt(pass_user)		            
            data=open('usernames//username.txt','r')
            data_in_file = (data.readlines())					            #saving data in data_in_file
                
            player_data=data_in_file[index]
            player_data = eval(player_data)				                    #dictionary of each player
            if  encrypt_password == player_data["encrypted_password"]:
                open_game(log_in,index)
                    
            else:
                messagebox.showwarning('login info','Credentials are not valid.')
    else:
        messagebox.showwarning('login info','This username is not found\nPlease Signup first!')
    

def login_procedure():                                                                          #function to create log_in window
    '''creates window of login menu'''
    log_in=Tk()
    log_in.title('Log_in')
    log_in.geometry('780x441')
    log_in.resizable(False,False)
    log_in.iconbitmap('Images//user.ico')

    
    bg=ImageTk.PhotoImage(Image.open('Images//gtabg1.png'))
    Label(log_in,image=bg).grid(row=0,column=0)
    back=ImageTk.PhotoImage(Image.open('Images//sign_up.png'))
    frame=LabelFrame(log_in,bg='#030404')                                                    #creates a frame to place buttons and entries on the screen
 
    frame.grid(row=0,column=0,ipadx=30,ipady=20)
    log_lb=Label(frame,text='LOGIN ',font=('Time New Roman',20,'bold'),bg='#030404',fg='white')
    log_lb.pack()
    username = Label(frame,text='Enter Username: ',bg='#030404',fg='white')
    username.pack()
    entry=Entry(frame,width=18)
    entry.pack()
    log_lbl2=Label(frame,text='Enter Passward: ',bg='#030404',fg='white')
    log_lbl2.pack()
    password=Entry(frame,width=18,show='*')
    password.pack()
    log_bt=Button(frame,text='Login',font=('Time New Roman',14,'bold'),bg='#921426',fg='white',command=lambda: log_game(entry,password,log_in),activebackground='#921426')
    log_bt.pack(pady=10)
    msg_lbl=Label(frame,text='If you don\'t have an account,\nthen click. ',bg='#030404',fg='white')
    msg_lbl.pack()
    log_bt=Button(frame,text='SIGNUP',font=('Time New Roman',12,'bold'),bg='#921426',fg='white',command=lambda: signup(back),activebackground='#921426')
    log_bt.pack(pady=10)
    
    log_in.mainloop()           
    
login_procedure()

