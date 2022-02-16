#*********************** START OF PROGRAM **************************
 
# ************ IMPORTING ALL ESSENTIAL PACKAGES AND MODULES ********
 
from tkinter import * # FOR GUI 
import tkinter.messagebox
import pymysql # FOR CONNECTING PYTHON AND MYSQL
from datetime import timedelta, date
 
# ****************** CONNECTING PYTHON AND MYSQL *******************
 
con=pymysql.connect(host=xxxx,user=xxxx,passwd=xxxx,db=xxxx)
cur=con.cursor()
 
cur.execute("create table if not exists studetail   (rollno varchar(20) primary key,name varchar(30),password varchar(30));")
cur.execute("create table if not exists books (bookid varchar(20) primary key,title varchar(30),genre varchar(30),author varchar(30),status varchar(30) not null default 'Available');")
cur.execute("create table if not exists issuedetail (bookid varchar(20) primary key,rollno varchar(20),borrow_date DATE, return_date DATE);")
 
# ******************  SELECTING & BORROWING PAGE *******************
 
def selectBook():
    
    greet_borrow.destroy()
    dropdown.destroy()
    select_bt.destroy()
    
    
    today = date.today()
    deadline = date.today() + timedelta(days=30)
 
    today = str(today)
    deadline = str(deadline)
    
    selected_opt = variable.get()
    selected_id = selected_opt[0:3]
   
    sql = "insert into issuedetail values ('"+selected_id+"','"+Id+"','"+today+"','"+deadline+"')"
    cur.execute(sql)
    con.commit()
    
    sql = "update books set status = 'Unavailable' where bookid = ('"+selected_id+"')"
    cur.execute(sql)
    con.commit()
    
    
    dashboard_label = Label(root, text = 'Your Dashboard', font=("Helvetica", 14), bg = 'white')
    dashboard_label.place(relx=0.38, rely=0.05)
    
    borrowed_label = Label(root, text = 'Borrowed Book(s)', font=("Helvetica", 14), bg = 'white')
    borrowed_label.place(relx=0.15, rely=0.25)
    
    sql = "select * from issuedetail where rollno = ('"+Id+"');"
    cur.execute(sql)
    issdet = cur.fetchall()
    
    c = 0.30
    
    for row in issdet:
        query = "select title from books where bookid = ('"+row[0]+"')"
        cur.execute(query)
        book_title = cur.fetchone()
        
        book_label = Label(root, text = row[0] + ' | ' + book_title[0] + ' | Date issued: ' + str(row[2]) + ' | Date to be returned: ' + str(row[3]))
        book_label.place(relx=0.15, rely=c)
        
        c = c + 0.075
        
 
def borrowPage():
    greet_user.destroy()
    borrowButton.destroy()
    returnButton.destroy()
    
    global greet_borrow
    greet_borrow = Label(root, text = 'Select the book you want to borrow from the list below', font=("Helvetica", 14), bg = 'white')
    greet_borrow.place(relx=0.27, rely=0.05)
    
    
    book_options = []
    
    sql = "select * from books;"
    
    cur.execute(sql)
    records = cur.fetchall()
    
    text=''
    
    for row in records:
        if row[4] == 'Available':
            text =  row[0] + ' | Title: ' + row[1] + ' | Genre: ' + row[2] + ' | Author: ' + row[3]  
            book_options.append(text)
    
    global variable
    variable = StringVar(root)
    variable.set(book_options[0])  
 
    global dropdown
    dropdown = OptionMenu(root, variable, *book_options)
    dropdown.place(relx=0.25, rely=0.4)    
    
    global select_bt
    select_bt = Button(root, text = 'Select', bg = 'green', height = 3, width = 20, command = selectBook)
    select_bt.place(relx=0.4, rely=0.7)
    
    
    
# ******************** SELECTING & RETURNING PAGE ******************
 
def selectReturn():
    
    selected_opt = var.get()
    selected_id = selected_opt[0:3]
    
    
    query = "select rollno,return_date from issuedetail where bookid = ('"+selected_id+"')"
    cur.execute(query)
    rec = cur.fetchone()
    
    today = date.today()
    deadline = rec[1]
    
    
    if rec[0] == Id:
        
        query = "delete from issuedetail where bookid = ('"+selected_id+"')"
        cur.execute(query)
        con.commit()
        
        if today < deadline:
            query = "update books set status = 'Available' where bookid = ('"+selected_id+"')"
            cur.execute(query)
            con.commit()
            messagebox.showinfo("Success","Your book has been returned")
        else:
            messagebox.showinfo("Overdue","Your book has been returned past deadline. As a result, you are subject to a fine. Please contact the library admin.")
            
    else:
        messagebox.showinfo("Error","You did not borrow this book")
 
def returnPage():
    greet_user.destroy()
    borrowButton.destroy()
    returnButton.destroy()
    
    
    greet_return = Label(root, text = 'Select the book you want to return from the list below', font=("Helvetica", 14), bg = 'white')
    greet_return.place(relx=0.2, rely=0.05)
    
    
    book_options = []
    
    sql = "select * from books;"
    
    cur.execute(sql)
    records = cur.fetchall()
    
    text=''
    
    for row in records:
        if row[4] == 'Unavailable':
            text =  row[0] + ' | Title: ' + row[1] + ' | Genre: ' + row[2] + ' | Author: ' + row[3]  
            book_options.append(text)
    
    global var
    var = StringVar(root)
    var.set(book_options[0])  
 
    
    dropdown_return = OptionMenu(root, var, *book_options)
    dropdown_return.place(relx=0.27, rely=0.4)    
    
    
    select_but = Button(root, text = 'Select', bg = 'green', height = 3, width = 20, command = selectReturn)
    select_but.place(relx=0.4, rely=0.7)
    
    
  
  
    
# ****************** BORROW OR RETURN OPTION PAGE ******************
 
def borrowOrReturn():
    
     
    loginmsg.destroy()
    user_ID.destroy()
    user_name.destroy()
    user_pwd.destroy()
    ent_id.destroy()
    ent_name.destroy()
    ent_pwd.destroy()
    button_sub.destroy()
    retorbor_button.destroy()
        
 
    global greet_user
    greet_user = Label(root, text = 'Welcome, ' + name.capitalize() + '!', font=("Helvetica", 16), bg = 'white')
    greet_user.place(relx=0.4, rely=0.05)
    
    global borrowButton
    borrowButton = Button(root, text = 'Borrow', bg = 'green', height = 3, width = 20, command = borrowPage)
    borrowButton.place(relx=0.2, rely=0.5)
    
    global returnButton
    returnButton = Button(root, text = 'Return', bg = 'red', height = 3, width = 20, command = returnPage)
    returnButton.place(relx=0.6, rely=0.5)



#****************** SUCCESSFUL LOGIN MESSAGE BOX *******************
 
def successfulLogin():
    
    global Id
    Id = ent_id.get()
    global name
    name = ent_name.get()
    password = ent_pwd.get()
    signin = 0
    
    try:
        if (type(int(Id)) == int):
            pass
        else:
            messagebox.showinfo("Invalid Value","Unique ID should be an integer")
            return
    except:
        messagebox.showinfo("Invalid Value","Unique ID should be an integer")
        return
        
    sql = "select * from studetail"
    cur.execute(sql)
    stdet = cur.fetchall()
    
    for row in stdet:
        if row[0]==Id and row[1]==name and row[2]==password:
            signin = 1
            messagebox.showinfo("Success","Successfully signed in as " + name)
            break
            
    
    if signin == 0:
        sql = "insert into studetail values ('"+Id+"','"+name+"','"+password+"')" 
        
        cur.execute(sql)
        con.commit()
        tkinter.messagebox.showinfo('Success', 'Successfully signed up.')
        signin = 1
            
    
    if signin == 1: 
        global retorbor_button
        retorbor_button = Button(root, text = 'Take me to my options', bg = 'red', command = borrowOrReturn)
        retorbor_button.place(relx=0.4, rely=0.8)    
    
 
 
# ************************** LOGIN FORM ****************************
        
        
def loginForm():
 
    greeting.destroy()
    bt1.destroy()
    bt2.destroy()
    bt3.destroy()
    
    global loginmsg
    loginmsg = Label(root, text = 'Please Login / Sign Up', font=("Helvetica", 16), bg = 'white')
    loginmsg.place(relx=0.35, rely=0.05)
    global user_ID
    user_ID = Label(root, text='User ID')
    user_ID.place(relx=0.3, rely=0.45)
    global user_name
    user_name = Label(root, text='Username')
    user_name.place(relx=0.3, rely=0.5)
    global user_pwd
    user_pwd = Label(root, text='Password')
    user_pwd.place(relx=0.3, rely=0.55)
    global ent_id 
    ent_id = Entry(root)
    ent_id.place(relx=0.5, rely=0.45)
    global ent_name 
    ent_name = Entry(root)
    ent_name.place(relx=0.5, rely=0.5)
    global ent_pwd
    ent_pwd = Entry(root, show='*')
    ent_pwd.place(relx=0.5, rely=0.55)
    
    global button_sub
    button_sub = Button(root, text = 'Submit', bg='green', command = successfulLogin)
    button_sub.place(relx=0.45, rely=0.65)



 
 
 
# ******************** DISPLAYING THE BOOKS ************************
 
def displayBooks():
    
    try:
        greeting.destroy()
        bt1.destroy()
        bt2.destroy()
        bt3.destroy()
        login_msg.destroy()
        user_ID.destroy()
        user_name.destroy()
        user_pwd.destroy()
        ent_id.destroy()
        ent_name.destroy()
        ent_pwd.destroy()
        button_sub.destroy()
    except NameError:
        pass
    
    greet_label = Label(root, text = 'Books in the library', font=("Helvetica", 16), bg = 'white')
    greet_label.grid(row=0,columnspan=9, sticky=W)
    blank_label = Label(root, text = '', bg='lightblue').grid(row=1)
    
    query = "select * from books"
    cur.execute(query)
    records = cur.fetchall()
    text=''
    c = 2
    for row in records:
        text = 'Id: ' + row[0] + ' | Title: ' + row[1] + ' | Genre: ' + row[2] + ' | Author: ' + row[3] + ' | Status: ' + row[4] 
        label = Label(root, text=text, font=("Arial", 10)).grid(row=c, columnspan = 9, sticky=W)
        c+=1
    
 
    
    
 
 
 
# ************************** MAIN PROGRAM **************************



root=Tk()
root.title('Library Management System')
root.geometry('800x600')
root.configure(bg='lightblue')
 
bt1 = Button(root, text = 'DISPLAY ALL BOOKS', bg = 'blue', fg = 'white', height = 3, width = 20, command = displayBooks)
bt2 = Button(root, text = 'BORROW', bg = 'blue', fg = 'white', height = 3, width = 20, command = loginForm)
bt3 = Button(root, text = 'RETURN', bg = 'blue', fg = 'white', height = 3, width = 20, command = loginForm)
 
bt1.place(relx=0.5, rely=0.25, anchor=CENTER)
bt2.place(relx=0.5, rely=0.5, anchor=CENTER)
bt3.place(relx=0.5, rely=0.75, anchor=CENTER)
 
greeting = Label(root, text = 'Welcome to TRA Library!', font=("Comic Sans", 20), bg = 'white')
greeting.place(relx=0.5, rely=0.05, anchor=CENTER)
 
        
        
        
        
        
 
root.mainloop()
 
#************************** END OF PROGRAM *************************
