from tkinter import *
import mysql.connector
from tkinter import messagebox, ttk, END

root = Tk()
root.title("Password Manager")
root.geometry("1000x500")
root.minsize(1000, 500)
root.maxsize(1000, 500)

frame = Frame(root, bg="#80c1ff", bd=5)
frame.place(relx=0.50, rely=0.50, relwidth=0.98, relheight=0.45, anchor = "n")


conn = mysql.connector.connect(host="localhost",password="password", user="root", database="passwordmanager")
cursor = conn.cursor()


cursor.execute(""" CREATE TABLE IF NOT EXISTS manager (
                        id int not null primary key auto_increment,
                        app_name text,
                        url text,
                        email_id text,
                        password text
                        )
""")


conn.commit()
conn.close()

def submit():
    conn = mysql.connector.connect(host="localhost",password="password", user="root", database="passwordmanager")
    cursor = conn.cursor()

    if app_name.get()!="" and url.get()!="" and email_id.get()!="" and password.get()!="":
        cursor.execute("INSERT INTO manager VALUES (0,%s, %s, %s, %s)",
            (
                app_name.get(),
                url.get(),
                email_id.get(),
                password.get()
            )
        )
        conn.commit()
        conn.close()
        messagebox.showinfo("Info", "Record Added in Database!")

        app_name.delete(0, END)
        url.delete(0, END)
        email_id.delete(0, END)
        password.delete(0, END)
        table.delete(*table.get_children())
        query()

    else:
        messagebox.showinfo("Alert", "Please fill all details!")
        conn.close()


def query():

    conn = mysql.connector.connect(host="localhost",password="password", user="root", database="passwordmanager")
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM manager")
    records = cursor.fetchall()
    print(records)
    table.delete(*table.get_children())

    for record in records:
        table.insert('', END, values=(record[0],record[1],record[2],record[3],record[4]))

    conn.commit()

    conn.close()

def delete():

    conn = mysql.connector.connect(host="localhost",password="password", user="root", database="passwordmanager")
    cursor = conn.cursor()

    t = delete_id.get()
    if(t!=""):
        cursor.execute("DELETE FROM manager where id = " + delete_id.get())
        delete_id.delete(0, END)
        table.delete(*table.get_children())
        query()
        messagebox.showinfo("Alert", "Record %s Deleted")
    else:
        messagebox.showinfo("Alert", "Please enter record id to delete!")
    conn.commit()

    conn.close()

def update():
    t = update_id.get()
    if(t!=""):
        global edit
        edit = Tk()
        edit.title("Update Record")
        edit.geometry("500x400")
        edit.minsize(450, 300)
        edit.maxsize(450, 300)

        global app_name_edit, url_edit, email_id_edit, password_edit

        app_name_edit = Entry(edit, width=30)
        app_name_edit.grid(row=0, column=1, padx=20)
        url_edit = Entry(edit, width=30)
        url_edit.grid(row=1, column=1, padx=20)
        email_id_edit = Entry(edit, width=30)
        email_id_edit.grid(row=2, column=1, padx=20)
        password_edit = Entry(edit, width=30)
        password_edit.grid(row=3, column=1, padx=20)

        app_name_label_edit = Label(edit, text="Application Name:")
        app_name_label_edit.grid(row=0, column=0)
        url_label_edit = Label(edit, text="URL:")
        url_label_edit.grid(row=1, column=0)
        email_id_label_edit = Label(edit, text="Email Id:")
        email_id_label_edit.grid(row=2, column=0)
        password_label_edit = Label(edit, text="Password:")
        password_label_edit.grid(row=3, column=0)

        submit_btn_edit = Button(edit, text="Save Record", command=change)
        submit_btn_edit.grid(row=4, column=0, columnspan=2, pady=5, padx=15, ipadx=135)

        conn = mysql.connector.connect(host="localhost",password="password", user="root", database="passwordmanager")
        cursor = conn.cursor()

        cursor.execute("SELECT * FROM manager where id = " + update_id.get())
        records = cursor.fetchall()

        for record in records:
            app_name_edit.insert(0, record[1])
            url_edit.insert(0, record[2])
            email_id_edit.insert(0, record[3])
            password_edit.insert(0, record[4])

        conn.commit()

        conn.close()

    else:
        messagebox.showinfo("Alert", "Please enter record id to update!")

def change():

    conn = mysql.connector.connect(host="localhost",password="password", user="root", database="passwordmanager")
    cursor = conn.cursor()

    if app_name_edit.get()!="" and url_edit.get()!="" and email_id_edit.get()!="" and password_edit.get()!="":
        cursor.execute("""UPDATE manager SET 
                app_name = :app_name,
                url = :url,
                email_id = :email_id,
                password = :password
                
                WHERE oid = :oid""",
                       {
                           'app_name': app_name_edit.get(),
                           'url': url_edit.get(),
                           'email_id': email_id_edit.get(),
                           'password': password_edit.get(),
                           'oid': update_id.get()
                       }
        )

        conn.commit()

        conn.close()

        messagebox.showinfo("Info", "Record Updated in Database!")

        update_id.delete(0, END)
        edit.destroy()

    else:
        messagebox.showinfo("Alert", "Please fill all details!")
        conn.close()


app_name = Entry(root, width=30)
app_name.grid(row=2, column=2, padx=20, pady=10)
url = Entry(root, width=30)
url.grid(row=3, column=2, padx=20, pady=10)
email_id = Entry(root, width=30)
email_id.grid(row=4, column=2, padx=20, pady=10)
password = Entry(root, width=30)
password.grid(row=5, column=2, padx=20, pady=10)
delete_id = Entry(root, width=20)
delete_id.grid(row=8, column=6, padx=20, pady=10)
update_id = Entry(root, width=20)
update_id.grid(row=8, column=4, padx=20, pady=10)

app_name_label = Label(root, text = "Application Name:")
app_name_label.grid(row=2, column=1)
url_label = Label(root, text = "URL:")
url_label.grid(row=3, column=1)
email_id_label = Label(root, text = "Email Id:")
email_id_label.grid(row=4, column=1)
password_label = Label(root, text = "Password:")
password_label.grid(row=5, column=1)


submit_btn = Button(root, text = "Add Record", command = submit, )
submit_btn.grid(row = 7, column=1, pady=5, padx=15, ipadx=35)

query_btn = Button(root, text = "Show Records", command = query)
query_btn.grid(row=7, column=2, pady=5, padx=5, ipadx=35)

delete_btn = Button(root, text = "Delete Record", command = delete)
delete_btn.grid(row=8, column=5, ipadx=30)

update_btn = Button(root, text = "Update Record", command = update)
update_btn.grid(row=8, column=3, ipadx=30)


table = ttk.Treeview(root, columns=('S.no','Application','URL','Email','Password'), show='headings')
table.heading('S.no', text='S.no')
table.heading('Application', text='Application')
table.heading('URL', text='URL')
table.heading('Email', text='Email')
table.heading('Password', text='Password')
table['displaycolumns'] = ('S.no','Application','URL','Email','Password')
table.place(x=0,y=250)

def main():
    root.mainloop()

if __name__ == '__main__':
    main()
