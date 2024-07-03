from tkinter import *
from tkinter import messagebox as mb
from PIL import Image, ImageTk, ImageOps
from datetime import datetime as dt
import sqlite3 as sq
from random import randint
import os


def get_time_str():
    return dt.now().strftime('%Y/%m/%d | %H:%M')


def connect_make():
    if not os.path.isdir('./DB'):
        os.mkdir('./DB')
    else:
        if os.path.isfile('./DB/data.db'):
            return sq.connect('./DB/data.db')
    conn = sq.connect('./DB/data.db')
    c = conn.cursor()
    c.execute('CREATE TABLE USERS (username TEXT, password TEXT)')
    c.execute('CREATE TABLE SELLS (seller TEXT, name TEXT, price INTEGER, amount INTEGER, discount INTEGER, date TEXT)')
    c.execute("INSERT INTO USERS (username, password) VALUES ('sale', 'qwerrewq')")
    conn.commit()
    return conn


class Login(Frame):
    def __init__(self, parent, controller):
        self.parent = parent
        self.controller = controller
        Frame.__init__(self, parent)
        self.image = ImageOps.mirror(Image.open("./Pics/LoginBack.jpg"))
        self.img_copy = self.image.copy()
        self.background_image = ImageTk.PhotoImage(self.image)
        self.background = Label(self, image=self.background_image)
        self.background.pack(fill=BOTH, expand=YES)
        self.background.bind('<Configure>', self._resize_image)

        headingFrame1 = Frame(self, bg="#BEBEBE", bd=5)
        headingFrame1.place(relx=0.5, rely=0.2, anchor=CENTER)
        title = Label(headingFrame1, text='  Sales Login Page  ',
                      font=('Courier', 20, 'bold'), bg='black', fg='yellow')
        title.grid(row=0, column=0)

        headingFrame2 = Frame(self, bg="#BEBEBE", bd=5)
        headingFrame2.place(relx=0.5, rely=0.6, anchor=CENTER)

        userl = Label(headingFrame2, text='Username', font=(
            'Courier', 15), bg='black', fg='yellow')
        userl.grid(row=0, column=0)

        self.useren = Entry(headingFrame2, font=('Courier', 14))
        self.useren.grid(row=0, column=1)

        passl = Label(headingFrame2, text='Password', font=(
            'Courier', 15), bg='black', fg='yellow')
        passl.grid(row=1, column=0)

        self.passen = Entry(headingFrame2, font=('Courier', 14), show='*')
        self.passen.grid(row=1, column=1)

        headingFrame3 = Frame(self, bg="#BEBEBE", bd=5)
        headingFrame3.place(relx=0.5, rely=0.8, anchor=CENTER)

        loginbtn = Button(headingFrame3, text='Login', font=('arial', 19), relief='ridge', bg='black',
                          fg='yellow', command=lambda: self.login(self.useren.get(), self.passen.get()))
        loginbtn.grid(row=0, column=0)

        resetbtn = Button(headingFrame3, text='Reset', font=('arial', 19), relief='ridge',
                          bg='black', fg='yellow', command=lambda: self.reset(self.useren, self.passen))
        resetbtn.grid(row=0, column=1)

        quitbtn = Button(self, text='QUIT', font=(
            'Courier', 13, 'bold'), fg='yellow', bg='#BEBEBE', command=self.quit)
        quitbtn.place(relx=0.99, rely=0.99, anchor=SE)

        newaccbtn = Button(self, text='Make New Account', font=('Courier', 13, 'bold'),
                           fg='yellow', bg='#BEBEBE', command=lambda: self.controller.show_frame(NewAcc))
        newaccbtn.place(relx=0.01, rely=0.99, anchor=SW)

    def login(self, usr, pss):
        if self.get(usr, pss):
            self.controller.username = usr
            self.controller.password = pss
            self.reset(self.useren, self.passen)
            self.controller.show_frame(Main)
        else:
            self.reset(self.useren, self.passen)
            mb.showerror(
                'Login Error', 'Login info was not correct.\nTry again!')
            self.useren.focus()

    def reset(self, *args):
        for i in args:
            i.delete(0, END)
        args[0].focus()

    def get(self, usr, pss):
        c = self.controller.conn.cursor()
        data = c.execute('SELECT * FROM USERS').fetchall()
        return (usr, pss) in data

    def quit(self):
        self.controller.destroy()

    def _resize_image(self, event):

        new_width = event.width
        new_height = event.height

        self.image = self.img_copy.resize((new_width, new_height))

        self.background_image = ImageTk.PhotoImage(self.image)
        self.background.configure(image=self.background_image)


class NewAcc(Frame):
    def __init__(self, parent, controller):
        self.parent = parent
        self.controller = controller
        Frame.__init__(self, parent)
        self.image = ImageOps.mirror(Image.open("./Pics/NewAccBack.jpg"))
        self.img_copy = self.image.copy()
        self.background_image = ImageTk.PhotoImage(self.image)
        self.background = Label(self, image=self.background_image)
        self.background.pack(fill=BOTH, expand=YES)
        self.background.bind('<Configure>', self._resize_image)

        infoframe = Frame(self, bg="#BEBEBE", bd=5)
        infoframe.place(relx=0.48, rely=0.4, anchor=CENTER)

        Username = StringVar()
        Password = StringVar()
        Password_re = StringVar()

        usernamelabel = Label(infoframe, text='Username', font=(
            'Courier', 14), bg='black', fg='yellow')
        usernamelabel.grid(row=0, column=0)

        usernameentry = Entry(
            infoframe, textvariable=Username, font=('Courier', 14))
        usernameentry.grid(row=0, column=1)

        passwordlabel = Label(infoframe, text='Password', font=(
            'Courier', 14), bg='black', fg='yellow')
        passwordlabel.grid(row=1, column=0)

        passwordentry = Entry(infoframe, textvariable=Password,
                              font=('Courier', 14), show='*')
        passwordentry.grid(row=1, column=1)

        password_re_label = Label(infoframe, text='Password', font=(
            'Courier', 14), bg='black', fg='yellow')
        password_re_label.grid(row=2, column=0)

        password_re_entry = Entry(
            infoframe, textvariable=Password_re, font=('Courier', 14), show='*')
        password_re_entry.grid(row=2, column=1)

        Label(infoframe, text='Repeat the password to confirm it.',
              width=35, font=('arial', 13)).grid(row=3, columnspan=2)

        headingFrame1 = Frame(self, bg="#BEBEBE", bd=5)
        headingFrame1.place(relx=0.5, rely=0.92, anchor=CENTER)

        makebtn = Button(headingFrame1, text='  Make  ', font=('Courier', 18), bg='black', fg='yellow',
                         command=lambda: self.makeacc(Username.get(), Password.get(), Password_re.get()))
        makebtn.grid(row=0, column=0)

        resetbtn = Button(headingFrame1, text='  Reset  ', font=('Courier', 18), bg='black',
                          fg='yellow', command=lambda: self.reset(usernameentry, passwordentry, password_re_entry))
        resetbtn.grid(row=0, column=1)

        backbtn = Button(self, text='Back', font=('arial', 12), bg='black', fg='yellow', relief='ridge', bd=3, command=lambda: (
            self.controller.show_frame(Login), self.reset(usernameentry, passwordentry, password_re_entry)))
        backbtn.place(relx=0.89, rely=0.9)

    def makeacc(self, usr, pss, rpss):
        if pss != rpss:
            mb.showerror('Inputs Error',
                         'Passwords doesn\'t match.\nTry Again!')
            return
        if len(pss) < 5 or len(usr) < 5:
            mb.showerror(
                'Input Error', 'Passwords and Usernames should at least be 5 characters.\nTry a longer one!')
            return
        c = self.controller.conn.cursor()
        users = c.execute('SELECT username FROM USERS').fetchall()
        if (usr,) in users:
            mb.showerror(
                'Input Error', 'Selected username is already taken.\nPick another one!')
            return
        c.execute(
            'INSERT INTO USERS (username, password) VALUES (?, ?)', (usr, pss))
        self.controller.conn.commit()
        mb.showinfo('Info', 'New account is maden successfully.')

    def reset(self, *args):
        for i in args:
            i.delete(0, END)
        args[0].focus()

    def _resize_image(self, event):

        new_width = event.width
        new_height = event.height

        self.image = self.img_copy.resize((new_width, new_height))

        self.background_image = ImageTk.PhotoImage(self.image)
        self.background.configure(image=self.background_image)


class Main(Frame):
    def __init__(self, parent, controller):
        self.parent = parent
        self.controller = controller
        Frame.__init__(self, parent)
        self.image = ImageOps.mirror(Image.open("./Pics/MainBack.jpg"))
        self.img_copy = self.image.copy()
        self.background_image = ImageTk.PhotoImage(self.image)
        self.background = Label(self, image=self.background_image)
        self.background.pack(fill=BOTH, expand=YES)
        self.background.bind('<Configure>', self._resize_image)

        headingFrame1 = Frame(self, bg="#BEBEBE", bd=5)
        headingFrame1.place(relx=0.11, rely=0.235, anchor=CENTER)

        sellbtn = Button(headingFrame1, text='Add a\nSell Item', font=(
            'Courier', 12), bg='black', fg='yellow', command=lambda: self.controller.show_frame(Sell))
        sellbtn.grid()

        headingFrame2 = Frame(self, bg="#BEBEBE", bd=5)
        headingFrame2.place(relx=0.115, rely=0.38, anchor=CENTER)

        buybtn = Button(headingFrame2, text='Buy\nSomething', font=(
            'Courier', 12), bg='black', fg='yellow', command=lambda: self.controller.show_frame(Buy))
        buybtn.grid()

        headingFrame4 = Frame(self, bg="#BEBEBE", bd=5)
        headingFrame4.place(relx=0.115, rely=0.67, anchor=CENTER)

        deletebtn = Button(headingFrame4, text='Accounts', font=(
            'Courier', 12), bg='black', fg='yellow', command=self.accounts)
        deletebtn.grid()

        headingFrame5 = Frame(self, bg="#BEBEBE", bd=5)
        headingFrame5.place(relx=0.11, rely=0.81, anchor=CENTER)

        addbtn = Button(headingFrame5, text='Availables', font=(
            'Courier', 12), bg='black', fg='yellow', command=self.availables)
        addbtn.grid()

        headingFrame7 = Frame(self, bg="#BEBEBE", bd=5)
        headingFrame7.place(relx=0.87, rely=0.53, anchor=CENTER)

        newaccbtn = Button(headingFrame7, text='Make a\nNew Account', font=(
            'Courier', 12), bg='black', fg='yellow', command=lambda: self.controller.show_frame(NewAcc))
        newaccbtn.grid()

        headingFrame9 = Frame(self, bg="#BEBEBE", bd=5)
        headingFrame9.place(relx=0.5, rely=0.98, anchor=S)

        logoutbtn = Button(self, text='Log Out', font=('Courier', 13, 'bold'), fg='yellow',
                           bg='#BEBEBE', relief='ridge', bd=2, command=lambda: self.controller.show_frame(Login))
        logoutbtn.place(relx=0.99, rely=0.99, anchor=SE)

        quitbtn = Button(headingFrame9, text='    Quit App    ', font=(
            'Courier', 18), bg='black', fg='yellow', command=self.controller.destroy)
        quitbtn.grid()

    def accounts(self):
        accs = self.controller.conn.cursor().execute('SELECT * FROM USERS').fetchall()
        with open('./DB/accounts.txt', 'w') as fo:
            fo.write('\t\t'.join(['Username', 'Password']) + '\n')
            for i in accs:
                fo.write('\t\t'.join(str(j) for j in i) + '\n')

    def availables(self):
        items = self.controller.conn.cursor().execute('SELECT * FROM SELLS').fetchall()
        with open('./DB/Items.txt', 'w') as fo:
            fo.write('\t\t'.join(
                ['Seller', 'Name', 'Price', 'Amount', 'Discount', 'Date']) + '\n')
            for i in items:
                fo.write('\t\t'.join(str(j) for j in i) + '\n')

    def _resize_image(self, event):

        new_width = event.width
        new_height = event.height

        self.image = self.img_copy.resize((new_width, new_height))

        self.background_image = ImageTk.PhotoImage(self.image)
        self.background.configure(image=self.background_image)


class Sell(Frame):
    def __init__(self, parent, controller):
        self.controller = controller
        Frame.__init__(self, parent)
        self.image = Image.open("./Pics/SellBack.jpg")
        self.img_copy = self.image.copy()
        self.background_image = ImageTk.PhotoImage(self.image)
        self.background = Label(self, image=self.background_image)
        self.background.pack(fill=BOTH, expand=YES)
        self.background.bind('<Configure>', self._resize_image)

        headingFrame1 = Frame(self, bg="#BEBEBE", bd=5)
        headingFrame1.place(relx=0.8, rely=0.5, anchor=CENTER)

        sellerl = Label(headingFrame1, text='    seller     ',
                        bg='black', fg='yellow')
        sellerl.grid(row=0, column=1)

        namel = Label(headingFrame1, text='    name     ',
                      bg='black', fg='yellow')
        namel.grid(row=1, column=1)

        pricel = Label(headingFrame1, text='price   p/e',
                       bg='black', fg='yellow')
        pricel.grid(row=2, column=1)

        amountl = Label(headingFrame1, text='   amount ',
                        bg='black', fg='yellow')
        amountl.grid(row=3, column=1)

        sellst = StringVar()
        namest = StringVar()
        pricest = StringVar()
        amountst = StringVar()
        discountst = DoubleVar()

        selleren = Entry(headingFrame1, textvariable=sellst, width=25)
        selleren.grid(row=0, column=0)

        nameen = Entry(headingFrame1, textvariable=namest, width=25)
        nameen.grid(row=1, column=0)

        priceen = Entry(headingFrame1, textvariable=pricest, width=25)
        priceen.grid(row=2, column=0)

        amounten = Entry(headingFrame1, textvariable=amountst, width=25)
        amounten.grid(row=3, column=0)

        self.discount = Scale(headingFrame1, label='Discount', bg='black', fg='yellow', length=205,
                              variable=discountst, from_=0, to=99, orient=HORIZONTAL, command=self.valuecheck)
        self.discount.grid(row=4, columnspan=2)

        backbtn = Button(self, text='Back', font=('arial', 12), bg='yellow', relief='ridge', bd=3, command=lambda: (
            self.controller.show_frame(Main), self.reset(selleren, nameen, priceen, amounten), discountst.set(0)))
        backbtn.place(relx=0.99, rely=0.99, anchor=SE)

        headingFrame2 = Frame(self, bg="#BEBEBE", bd=5)
        headingFrame2.place(relx=0.8, rely=0.8, anchor=CENTER)

        addbtn = Button(headingFrame2, text='Add', bg='black', fg='yellow', font=('Courier', 12), relief='ridge', bd=2,
                        command=lambda: self.add(selleren.get(), nameen.get(), priceen.get(), amounten.get(), self.discount.get()))
        addbtn.grid(row=0, column=0)

        resetbtn = Button(headingFrame2, text='Reset', bg='black', fg='yellow', font=('Courier', 12), relief='ridge',
                          bd=2, command=lambda: (self.reset(selleren, nameen, priceen, amounten), discountst.set(0)))
        resetbtn.grid(row=0, column=1)

    def valuecheck(self, value):
        valuelist = range(0, 100, 5)
        newvalue = min(valuelist, key=lambda x: abs(x-float(value)))
        self.discount.set(newvalue)

    def add(self, seller, name, price, amount, discount):
        if not all((seller, name, price, amount)):
            mb.showerror('Inputs Error',
                         'seller, name, price, amount should be filled.')
            return
        try:
            int(price)
            int(amount)
        except:
            mb.showerror(
                'Input Error', 'The values of `price` and `amount` should be integers.')
            return

        if int(price) <= 0 or int(amount) <= 0:
            mb.showerror(
                'Input Error', 'The values of `price` and `amount` should be more than 0.')
            return
        c = self.controller.conn.cursor()
        sells = c.execute('SELECT seller, name FROM SELLS').fetchall()
        if (seller, name) in sells:
            mb.showerror(
                'Value Error', 'This seller has already this item to sell.')
            return
        c.execute('INSERT INTO SELLS (seller, name, price, amount, discount, date) VALUES (?, ?, ?, ?, ?, ?)',
                  (seller, name, price, amount, discount, get_time_str()))
        self.controller.conn.commit()
        mb.showinfo('Done', 'The item is saved succefully.')

    def reset(self, *args):
        for i in args:
            i.delete(0, END)
        args[0].focus()

    def _resize_image(self, event):
        new_width = event.width
        new_height = event.height

        self.image = self.img_copy.resize((new_width, new_height))

        self.background_image = ImageTk.PhotoImage(self.image)
        self.background.configure(image=self.background_image)


class Buy(Frame):
    def __init__(self, parent, controller):
        self.controller = controller
        Frame.__init__(self, parent)
        self.image = Image.open("./Pics/BuyBack.jpg")
        self.img_copy = self.image.copy()
        self.background_image = ImageTk.PhotoImage(self.image)
        self.background = Label(self, image=self.background_image)
        self.background.pack(fill=BOTH, expand=YES)
        self.background.bind('<Configure>', self._resize_image)

        headingFrame1 = Frame(self, bg="#BEBEBE", bd=5)
        headingFrame1.place(relx=0.78, rely=0.27, anchor=CENTER)

        selleren = Entry(headingFrame1, font=('arial', 10))
        nameen = Entry(headingFrame1, font=('arial', 10))

        selleren.grid(row=0, column=0, columnspan=3)
        nameen.grid(row=1, column=0, columnspan=3)

        sellerl = Label(headingFrame1, font=('Courier', 10),
                        text='Seller Name', bg='black', fg='yellow')
        namel = Label(headingFrame1, font=('Courier', 10),
                      text='Item\'s Name', bg='black', fg='yellow')

        sellerl.grid(row=0, column=3)
        namel.grid(row=1, column=3)

        filterbtn = Button(headingFrame1, text='Filter', font=(
            'Courier', 12), bg='black', fg='yellow', command=lambda: self.filt(selleren.get(), nameen.get()))
        filterbtn.grid(row=2, column=0, columnspan=2, sticky=E)

        resetbtn = Button(headingFrame1, text=' Reset ', font=(
            'Courier', 12), bg='black', fg='yellow', command=lambda: (self.reset(selleren, nameen)))
        resetbtn.grid(row=2, column=2, columnspan=2, sticky=W)

        btnframe = Frame(self, bg="#BEBEBE", bd=5)
        btnframe.place(relx=0.5, rely=0.99, anchor=S)

        nexbtn = Button(btnframe, text='  >>', bg='black',
                        fg='yellow', command=lambda: self.show_sells(c=+1))
        bacbtn = Button(btnframe, text='Back', fg='black', bg='yellow', command=lambda: (
            self.controller.show_frame(Main), self.reset(selleren, nameen)))
        lasbtn = Button(btnframe, text='<<  ', bg='black',
                        fg='yellow', command=lambda: self.show_sells(c=-1))
        lasbtn.grid(row=0, column=0)
        bacbtn.grid(row=0, column=1)
        nexbtn.grid(row=0, column=2)

    def filt(self, seller, name):
        if seller and name:
            q = ('SELECT * FROM SELLS WHERE seller=? and name=?', (seller, name))
        elif seller:
            q = ('SELECT * FROM SELLS WHERE seller=?', (seller,))
        elif name:
            q = ('SELECT * FROM SELLS WHERE name=?', (name,))
        else:
            q = ('SELECT * FROM SELLS',)
        self.c = 0
        self.sells = self.controller.conn.cursor().execute(*q).fetchall()
        self.show_sells()

    def show_sells(self, c=0):
        try:
            self.sellframe.destroy()
        except:
            pass
        if not self.sells:
            self.sellframe = Frame(self, bg="#BEBEBE", bd=5)
            self.sellframe.place(relx=0.5, rely=0.5, anchor=CENTER)
            Label(self.sellframe, text='No Item Found!', font=(
                'Courier', 45), bg='black', fg='yellow').pack()
            return

        n = len(self.sells)
        self.c += c
        sell = self.sells[self.c % n]
        seller, name, price, amount, discount, date = sell

        self.sellframe = LabelFrame(self, text='Item\'s Info', bg='#BEBEBE')
        self.sellframe.place(relx=0.005, rely=0.48, anchor=NW)

        self.sellerf = LabelFrame(self.sellframe)
        self.sellerf.grid(row=0, column=0, padx=7, pady=10)
        self.sellercode = Label(
            self.sellerf, text='Seller Name', padx=1, pady=2)
        self.sellercode.grid(row=0, column=0)
        self.sellername = Label(self.sellerf, text=seller, relief='ridge',
                                bg='cadet blue', fg='cornsilk', padx=1, pady=2)
        self.sellername.grid(row=0, column=1)

        self.namef = LabelFrame(self.sellframe)
        self.namef.grid(row=0, column=1, padx=7, pady=10)
        self.namecode = Label(self.namef, text='Name', padx=1, pady=2)
        self.namecode.grid(row=0, column=0)
        self.namename = Label(self.namef, text=name, relief='ridge',
                              bg='cadet blue', fg='cornsilk', padx=1, pady=2)
        self.namename.grid(row=0, column=1)

        self.amountf = LabelFrame(self.sellframe)
        self.amountf.grid(row=0, column=2, padx=7, pady=10)
        self.amountcode = Label(self.amountf, text='How Many?', padx=1, pady=2)
        self.amountcode.grid(row=0, column=0)
        self.amountnum = Label(self.amountf, text=str(
            amount), relief='ridge', bg='cadet blue', fg='cornsilk', padx=1, pady=2)
        self.amountnum.grid(row=0, column=1)

        self.pricef = LabelFrame(self.sellframe)
        self.pricef.grid(row=1, column=0, padx=7, pady=10)
        self.pricecode = Label(self.pricef, text='Price p/e', padx=1, pady=2)
        self.pricecode.grid(row=0, column=0)
        if discount == 0:
            self.pricenum = Label(self.pricef, text=str(
                price), relief='ridge', bg='cadet blue', fg='cornsilk', padx=1, pady=2)
            self.pricenum.grid(row=0, column=1)

        else:
            self.pricenum = Label(self.pricef, text=str(price), font=(
                'arial',  10, 'overstrike'), relief='ridge', bg='red', fg='yellow', padx=1, pady=2)
            self.pricenum.grid(row=0, column=1, padx=2)
            self.pricenum = Label(self.pricef, text=str(price * (100 - discount)/100), font=(
                'arial',  10), relief='ridge', bg='cadet blue', fg='cornsilk', padx=1, pady=2)
            self.pricenum.grid(row=0, column=2)
            self.discountcode = Label(
                self.pricef, text='Discount', padx=1, pady=2)
            self.discountcode.grid(row=1, column=0)
            self.discountnum = Label(self.pricef, text=str(discount) + ' %',  font=(
                'arial',  10), relief='ridge', bg='cadet blue', fg='cornsilk', padx=1, pady=2)
            self.discountnum.grid(row=1, column=1)

        self.datef = LabelFrame(self.sellframe)
        self.datef.grid(row=1, column=1, columnspan=2, padx=7, pady=10)
        self.datecode = Label(self.datef, text='Date of Sell', padx=1, pady=2)
        self.datecode.grid(row=0, column=0)
        self.datenum = Label(self.datef, text=date, relief='ridge',
                             bg='cadet blue', fg='cornsilk', padx=1, pady=2)
        self.datenum.grid(row=0, column=1)

        btnsframe = LabelFrame(self.sellframe, width=180, height=100)
        btnsframe.grid(row=0, rowspan=2, column=3,
                       columnspan=3, padx=7, pady=10)

        wantval = DoubleVar()

        def btn(val):
            btnsell.config(
                text=f'Buy with {int(val) * price * (100 - discount) / 100}$')

        want = Scale(btnsframe, label='How Much you want?', bg='black', fg='yellow',
                     length=170, variable=wantval, from_=1, to=amount, orient=HORIZONTAL, command=btn)
        want.grid(row=0, column=0, padx=4)

        btnsell = Button(btnsframe, text=f'Buy with {price * (100 - discount) / 100}', font=(
            'Courier', 13), bg='black', fg='yellow', command=lambda: self.buy(seller, name, amount, wantval.get()))
        btnsell.grid(row=1, column=0)

    def buy(self, seller, name, amount, want):
        c = self.controller.conn.cursor()
        c.execute('UPDATE SELLS SET amount=? WHERE seller=? AND name=?',
                  (amount - want, seller, name))
        self.controller.conn.commit()
        self.filt('', '')

    def reset(self, *args):
        for i in args:
            i.delete(0, END)
        args[0].focus()

    def _resize_image(self, event):
        new_width = event.width
        new_height = event.height

        self.image = self.img_copy.resize((new_width, new_height))

        self.background_image = ImageTk.PhotoImage(self.image)
        self.background.configure(image=self.background_image)


# User, Password:
# sale, qwerrewq


class Root(Tk):
    def __init__(self, *args, **keywargs):
        self.conn = connect_make()
        Tk.__init__(self, *args, **keywargs)
        self.geometry('600x500')
        self.resizable(width=False, height=False)
        self.title('Grocery Sale')
        self.iconbitmap('./Pics/icon.ico')

        self.container = Frame(self)
        self.container.pack(side='top', fill='both', expand=True)
        self.container.grid_rowconfigure(0, weight=1)
        self.container.grid_columnconfigure(0, weight=1)

        self.frames = {}
        for F in (Login, NewAcc, Main, Sell, Buy):
            frame = F(self.container, self)
            self.frames[F] = frame
            frame.grid(row=0, column=0, sticky='nsew')
            self.show_frame(F)

        self.show_frame(Login)

    def show_frame(self, cont):
        self.frames[cont].tkraise()


app = Root()
app.mainloop()
