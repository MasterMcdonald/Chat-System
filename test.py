"""
client clode
@Druft: Haoian Shen
@Author: Zelan Xiang, Haoian Shen
@Editor: Zelan Xiang
@GUI_Author: Zelan Xiang
@DATABASE_Author: Zelan Xiang
"""
import socket
from ScrolledText import ScrolledText
from Tkinter import *
#Button, Label, Frame, Toplevel, Entry, Menu
import MySQLdb


class Signup(object):
    """
    This is the signup class
    """
    def __init__(self, mysocket):
        """
        This is the signup gui
        """
        self.mysocket = mysocket
        self.toptop = Toplevel()
        self.toptop.title('Signup')
        self.frame_tri = Frame(self.toptop)
        self.line_one = Frame(self.frame_tri)
        self.line_two = Frame(self.frame_tri)
        self.line_tri = Frame(self.frame_tri)

        self.name_text = Label(self.line_one, text='User Name:')
        self.name_text.pack(side=LEFT)
        self.name_entrybox = Entry(self.line_one)
        self.name_entrybox.pack(side=RIGHT)

        self.password_text = Label(self.line_two, text='   Password:')
        self.password_text.pack(side=LEFT)
        self.password_entrybox = Entry(self.line_two)
        self.password_entrybox.pack(side=RIGHT)

        self.confirm_text = Label(self.line_tri, text='    Confirm:')
        self.confirm_text.pack(side=LEFT)
        self.confirm_entrybox = Entry(self.line_tri)
        self.confirm_entrybox.pack(side=RIGHT)

        self.line_one.pack(side=TOP)
        self.line_two.pack(side=TOP)
        self.line_two.pack(side=BOTTOM)
        self.frame_tri.pack(side=LEFT)

        self.signup_button = Button(self.toptop, text='SIGNUP',
                                    width=5, height=2, font=('Arial', 13, "bold"),
                                    fg='white', bg='DarkOrange',
                                    command=lambda: self.signup_db
                                    (self.name_entrybox.get(), self.password_entrybox.get()))
        self.signup_button.pack(side=RIGHT)

    def signup_db(self, username, passwords):
        """
        This is db for signup
        """
        try:
            CURSOR.execute("SELECT * FROM USERS WHERE UNAME='%s'" % (username))
            intable = CURSOR.fetchall()
            if intable == ():
                CURSOR.execute("INSERT INTO USERS(UNAME, PASSWORD) VALUES(%s, %s)"
                               %('\''+username+'\'', '\''+passwords+'\''))
                DATABASE.commit()
                self.mysocket.send('login'+username)
                self.toptop.destroy()
            else:
                error_win = Toplevel()
                error_win.title('Error')
                error_text = Label(error_win, text='User already exist.')
                error_text.pack(side=TOP)
                close_button = Button(error_win, text='Close', width=5, height=1,
                                    font=('Arial', 13, "bold"),
                                    fg='white', bg='DarkOrange',
                                    command=error_win.destroy)
                close_button.pack(side=BOTTOM)
        except Exception:
            CURSOR.execute("INSERT INTO USERS(UNAME, PASSWORD) VALUES(%s, %s)"
                           %('\''+username+'\'', '\''+passwords+'\''))
            DATABASE.commit()
            self.mysocket.send('login'+username)
            self.toptop.destroy()


class Login(object):
    """
    This is the login class
    """
    def __init__(self, mysocket):
        """
        This is the login gui
        """
        self.mysocket = mysocket
        self.topper = Toplevel()
        self.topper.title('Login')
        self.frame_two = Frame(self.topper)
        self.line_one = Frame(self.frame_two)
        self.line_two = Frame(self.frame_two)

        self.name_text = Label(self.line_one, text='User Name:')
        self.name_text.pack(side=LEFT)
        self.name_entrybox = Entry(self.line_one)
        self.name_entrybox.pack(side=RIGHT)

        self.password_text = Label(self.line_two, text='   Password:')
        self.password_text.pack(side=LEFT)
        self.password_entrybox = Entry(self.line_two)
        self.password_entrybox.pack(side=RIGHT)

        self.line_one.pack(side=TOP)
        self.line_two.pack(side=BOTTOM)
        self.frame_two.pack(side=LEFT)

        self.login_button = Button(self.topper, text='LOGIN',
                                   width=5, height=2, font=('Arial', 13, "bold"),
                                   fg='white', bg='DarkOrange',
                                   command=lambda: self.login_db
                                   (self.name_entrybox.get(), self.password_entrybox.get()))
        self.login_button.pack(side=RIGHT)

    def login_db(self, username, passwords):
        """
        this is the login function
        """
        username = username.strip()
        passwords = passwords.strip()
        try:
            CURSOR.execute("SELECT * FROM USERS WHERE UNAME='%s'" % (username))
            user = CURSOR.fetchone()
            password = user[1]
            if password == passwords:
                self.mysocket.send('login'+username)
                self.topper.destroy()
            else:
                self.error_gui('password')
        except Exception:
            self.error_gui('accout')

    def error_gui(self, error_type):
        """
        This is the error gui
        """
        error_win = Toplevel()
        error_win.title('Error')
        error_text = Label(error_win, text=error_type + ' is wrong')
        error_text.pack(side=TOP)
        close_button = Button(error_win, text='Close', width=5, height=1,
                              font=('Arial', 13, "bold"),
                              fg='white', bg='DarkOrange',
                              command=error_win.destroy)
        close_button.pack(side=BOTTOM)


def send(messages):
    """
    the sending method
    """
    input_split = messages.split(" ")
    if len(input_split) > 1:
        msg = str(input_split[1:])
    if input_split[0] == "/quit":
        S.close()
        quit()
    elif input_split[0] == "/create":
        action = '01'
    elif input_split[0] == "/delete":
        action = '02'
    elif input_split[0] == "/join":
        action = '03'
    elif input_split[0] == "/block":
        action = '04'
    elif input_split[0] == "/unblock":
        action = '05'
    elif input_split[0] == "/set_alias":
        action = '06'
    else:
        action = '00'
        msg = input_split[0:]
        msg = reduce((lambda x, y: x+' '+y), msg)
        MESSAGE_DISPLAY.insert(END, "[You]: " + msg)
    message = action + msg
    S.send(message)
    MESSAGE_INPUT.delete("0.0", "end")

def recieve():
    """
    recieve method
    """

    try:
        data = S.recv(1024)
        if data:
            MESSAGE_DISPLAY.insert(END, data)
        else:
            MESSAGE_DISPLAY.insert(END, 'disconnect')
    except socket.error:
        pass

def info_gui():
    """
    This is a info
    """
    info_m = '***This is chat system ***\n ***It is not perfect, but it works, mostly.***\n'
    MESSAGE_DISPLAY.insert(END, info_m)





if __name__ == '__main__':
    #Socket
    HOST = socket.gethostname()
    PORT = 10000
    ADDRESS = (HOST, PORT)
    MSG = ''
    S = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    S.connect(ADDRESS)
    #Database
    DATABASE = MySQLdb.connect('127.0.0.1', 'root', 'Xiang918', 'Chatus')
    CURSOR = DATABASE.cursor()
    #GUI
    ROOT = Tk()
    ROOT.title('Chatus')
    MENU_BAR = Menu(ROOT)
    FIRST_MENU = Menu(MENU_BAR, tearoff=0)

    #Main Menu
    FIRST_MENU.add_command(label='Login', command=lambda: Login(S))
    FIRST_MENU.add_command(label='signup', command=lambda: Signup(S))
    FIRST_MENU.add_command(label='Exit', command=ROOT.quit)
    MENU_BAR.add_cascade(label='Main', menu=FIRST_MENU)
    #Help Menu
    SECOND_MENU = Menu(MENU_BAR, tearoff=0)
    SECOND_MENU.add_command(label='Info', command=lambda: info_gui())
    MENU_BAR.add_cascade(label='Help', menu=SECOND_MENU)
    #Text Display
    MESSAGE_DISPLAY = ScrolledText(ROOT, width=37, height=15, font=('Arial', 13),
                                   fg='black', bg='white')
    MESSAGE_DISPLAY.pack(expand=1, padx=5, pady=5, side=TOP)

    FRAME_ONE = Frame(ROOT)
    #Text Input
    MESSAGE_INPUT = ScrolledText(FRAME_ONE, width=25, height=5, font=('Arial', 13),
                                 fg='black', bg='white')
    MESSAGE_INPUT.pack(expand=1, padx=5, pady=5, side=RIGHT)
    #Send Button
    FRAME_ONE_LEFT = Frame(FRAME_ONE)
    SEND_BUTTON = Button(FRAME_ONE_LEFT, text='SEND', width=10,
                         height=2, font=('Arial', 13, "bold"),
                         fg='white', bg='DarkOrange',
                         command=lambda: send(MESSAGE_INPUT.get("0.0", "end")))
    SEND_BUTTON.pack(side=TOP)
    #Refresh Button
    REFRESH_BUTTON = Button(FRAME_ONE_LEFT, text='REFRESH',
                            width=10, height=2, font=('Arial', 13, "bold"),
                            fg='white', bg='DarkOrange', command=lambda: recieve())
    REFRESH_BUTTON.pack(side=BOTTOM)
    FRAME_ONE_LEFT.pack(side=LEFT)
    FRAME_ONE.pack(side=BOTTOM)

    ROOT.config(menu=MENU_BAR)
    ROOT.mainloop()
