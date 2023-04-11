from functools import partial
from tkinter import *
from tkinter import ttk, messagebox
from turtle import width
import pymysql
import program_customization as cs
import credentials as cr
import verify_email as vl

class Management:
    def __init__(self, root):
        self.window = root
        self.window.title("Customer Communication Management System")
        self.window.geometry("960x540")
        self.window.config(bg = "white")
        
        # Here we are fixing the values of the colors imported from program_customization
        self.color_1 = cs.color_1
        self.color_2 = cs.color_2
        self.color_3 = cs.color_3
        self.color_4 = cs.color_4
        self.font_1 = cs.font_1
        self.font_2 = cs.font_2
        self.columns = cs.columns

        # Here all the connection attributes are taken from the credentials.py program.
        #my local host, mysql server password, and database name is used for connection.
        self.host = cr.host
        self.user = cr.user
        self.password = cr.password
        self.database = cr.database

        # Here We are creating the left frame with the width of 740
        self.frame_1 = Frame(self.window, bg=cs.color_1)
        self.frame_1.place(x=0, y=0, width=740, relheight = 1)

        # code to create right frame
        self.frame_2 = Frame(self.window, bg = cs.color_2)
        self.frame_2.place(x=740,y=0,relwidth=1, relheight=1)

        # These are the TKINTER buttons, when pressed methods are triggered
        self.add_new_bt = Button(self.frame_2, text='Add Customer Data', font=(cs.font_1, 12), bd=2, command=self.AddRecord,cursor="hand2", bg=self.color_2,fg=self.color_3).place(x=50,y=40,width=140)
        self.display_bt = Button(self.frame_2, text='Display Customer Data', font=(cs.font_1, 12), bd=2, command=self.DisplayRecords, cursor="hand2", bg=self.color_2,fg=self.color_3).place(x=50,y=100,width=150)
        self.search_bt = Button(self.frame_2, text='Search Customer', font=(cs.font_1, 12), bd=2, command=self.GetContact_to_Search,cursor="hand2", bg=self.color_2,fg=self.color_3).place(x=50,y=160,width=120)
        self.clear_bt = Button(self.frame_2, text='Clear', font=(cs.font_1, 12), bd=2, command=self.ClearScreen,cursor="hand2", bg=self.color_2,fg=self.color_3).place(x=50,y=340,width=100)
        self.exit_bt = Button(self.frame_2, text='Exit', font=(cs.font_1, 12), bd=2, command=self.Exit, cursor="hand2", bg=self.color_2,fg=self.color_3).place(x=50,y=400,width=100)
        
    '''This function is used to print and display the records'''
    def DisplayRecords(self):
        self.ClearScreen()
        # Defining two scrollbars
        scroll_x = ttk.Scrollbar(self.frame_1, orient=HORIZONTAL)
        scroll_y = ttk.Scrollbar(self.frame_1, orient=VERTICAL)
        self.tree = ttk.Treeview(self.frame_1, columns=self.columns, height=400, selectmode="extended", yscrollcommand=scroll_y.set, xscrollcommand=scroll_x.set)
        scroll_y.config(command=self.tree.yview)
        # vertical scrollbar: left side
        scroll_y.pack(side=LEFT, fill=Y)
        scroll_x.config(command=self.tree.xview)
        # Horizontal scrollbar: at bottom
        scroll_x.pack(side=BOTTOM, fill=X)

        #headings for the tables
        self.tree.heading('first_name', text='First Name', anchor=W)
        self.tree.heading('last_name', text='Last Name', anchor=W)
        self.tree.heading('address', text='Address', anchor=W)
        self.tree.heading('contact', text='Contact', anchor=W)
        self.tree.heading('email', text='Email', anchor=W)
        self.tree.pack()

        try:
            connection = pymysql.connect(host=self.host, user=self.user, password=self.password, database=self.database)
            curs = connection.cursor()
            curs.execute("select * from contact_register")
            rows=curs.fetchall()
            if rows == None:
                messagebox.showinfo("Database Empty","There is no data to show",parent=self.window)
                connection.close()
                self.ClearScreen()
            else:
                connection.close()
        except Exception as e:
            messagebox.showerror("Error!",f"Error due to {str(e)}",parent=self.window)
        for list in rows:
            self.tree.insert("", 'end', text=(rows.index(list)+1), values=(list[0], list[1], list[2], list[3], list[4]))

    '''to show the data searched'''
    def ShowRecords(self, rows):
        self.ClearScreen()
        scroll_x = ttk.Scrollbar(self.frame_1, orient=HORIZONTAL)
        scroll_y = ttk.Scrollbar(self.frame_1, orient=VERTICAL)
        self.tree = ttk.Treeview(self.frame_1, columns=self.columns, height=400, selectmode="extended", yscrollcommand=scroll_y.set, xscrollcommand=scroll_x.set)
        scroll_y.config(command=self.tree.yview)
        scroll_y.pack(side=LEFT, fill=Y)
        scroll_x.config(command=self.tree.xview)
        scroll_x.pack(side=BOTTOM, fill=X)

        # Table headings
        self.tree.heading('first_name', text='First Name', anchor=W)
        self.tree.heading('last_name', text='Last Name', anchor=W)
        self.tree.heading('address', text='Address', anchor=W)
        self.tree.heading('contact', text='Contact', anchor=W)
        self.tree.heading('email', text='Email', anchor=W)
        self.tree.pack()
        self.tree.bind('<Double-Button-1>')
        # Insert the data into the tree table
        for list in rows:
            self.tree.insert("", 'end', text=(rows.index(list)+1), values=(list[0], list[1], list[2], list[3], list[4]))

    '''Widget to add customer information'''
    def AddRecord(self):
        self.ClearScreen()

        self.name = Label(self.frame_1, text="First Name", font=(self.font_2, 15, "bold"), bg=self.color_1).place(x=220,y=30)
        self.name_entry = Entry(self.frame_1, bg=self.color_4, fg=self.color_3)
        self.name_entry.place(x=220,y=60, width=300)

        self.surname = Label(self.frame_1, text="Surname", font=(self.font_2, 15, "bold"), bg=self.color_1).place(x=220,y=100)
        self.surname_entry = Entry(self.frame_1, bg=self.color_4, fg=self.color_3)
        self.surname_entry.place(x=220,y=130, width=300)

        self.addr = Label(self.frame_1, text="Address", font=(self.font_2, 15, "bold"), bg=self.color_1).place(x=220,y=170)
        self.addr_entry = Entry(self.frame_1, bg=self.color_4, fg=self.color_3)
        self.addr_entry.place(x=220,y=200, width=300)

        self.contact = Label(self.frame_1, text="Contact", font=(self.font_2, 15, "bold"), bg=self.color_1).place(x=220,y=240)
        self.contact_entry = Entry(self.frame_1, bg=self.color_4, fg=self.color_3)
        self.contact_entry.place(x=220,y=270, width=300)

        self.email = Label(self.frame_1, text="Email", font=(self.font_2, 15, "bold"), bg=self.color_1).place(x=220,y=310)
        self.email_entry = Entry(self.frame_1, bg=self.color_4, fg=self.color_3)
        self.email_entry.place(x=220,y=340, width=300)

        self.submit_bt_1 = Button(self.frame_1, text='Submit', font=(self.font_1, 12), bd=2, command=self.Submit, cursor="hand2", bg=self.color_2,fg=self.color_3).place(x=310,y=389,width=100)

    
    def GetContact_to_Search(self):
        self.ClearScreen()
        getName = Label(self.frame_1, text="Name", font=(self.font_2, 18, "bold"), bg=self.color_1).place(x=160,y=70)
        self.name_entry = Entry(self.frame_1, font=(self.font_1, 12), bg=self.color_4, fg=self.color_3)
        self.name_entry.place(x=160, y=110, width=200, height=30)

        getSurname = Label(self.frame_1, text="Surname", font=(self.font_2, 18, "bold"), bg=self.color_1).place(x=420,y=70)
        self.surname_entry = Entry(self.frame_1, font=(self.font_1, 12), bg=self.color_4, fg=self.color_3)
        self.surname_entry.place(x=420, y=110, width=200, height=30)

        submit_bt_2 = Button(self.frame_1, text='Submit', font=(self.font_1, 10), bd=2, command=self.CheckContact_to_Search, cursor="hand2", bg=self.color_2,fg=self.color_3).place(x=340,y=160,width=80)
            
    '''code for clearing the screen'''
    def ClearScreen(self):
        for widget in self.frame_1.winfo_children():
            widget.destroy()

    '''method for exit or terminating'''
    def Exit(self):
        self.window.destroy()

    
    def CheckContact_to_Search(self):
        if self.name_entry.get() == "" and self.surname_entry.get() == "":
            messagebox.showerror("Error!", "You must input Name or Surname",parent=self.window)
        else:
            try:
                connection = pymysql.connect(host=self.host, user=self.user, password=self.password, database=self.database)
                curs = connection.cursor()
                curs.execute("select * from contact_register where f_name=%s or l_name=%s", (self.name_entry.get(), self.surname_entry.get()))
                rows=curs.fetchall()
                if len(rows) == 0:
                    messagebox.showerror("Error!","This name doesn't exists",parent=self.window)
                    connection.close()
                    self.name_entry.delete(0, END)
                    self.surname_entry.delete(0, END)
                else:
                    self.ShowRecords(rows)
                    connection.close()
            except Exception as e:
                messagebox.showerror("Error!",f"Error due to {str(e)}",parent=self.window)

  
    
    '''function to successfully add a new record'''
    def Submit(self):
        if self.name_entry.get() == "" or self.surname_entry.get() == "" or self.addr_entry.get() == "" or self.contact_entry.get() == "" or self.email_entry.get() == "":
            messagebox.showerror("Error!","Sorry!, All fields are required",parent=self.window)
        else:
            try:
                connection = pymysql.connect(host=self.host, user=self.user, password=self.password, database=self.database)
                curs = connection.cursor()
                curs.execute("select * from contact_register where contact=%s", self.contact_entry.get())
                row=curs.fetchone()

                if row!=None:
                    messagebox.showerror("Error!","The contact number is already exists, please try again with another number",parent=self.window)
                else:
                    if vl.IsValidEmail(self.email_entry.get()):
                        curs.execute("insert into contact_register (f_name,l_name,address,contact,email) values(%s,%s,%s,%s,%s)",
                                            (
                                                self.name_entry.get(),
                                                self.surname_entry.get(),
                                                self.addr_entry.get(),
                                                self.contact_entry.get(),
                                                self.email_entry.get()  
                                            ))
                        connection.commit()
                        connection.close()
                        messagebox.showinfo('Done!', "The data has been submitted")
                        self.reset_fields()
                    else:
                        messagebox.showerror("Error!", "Please enter a valid email id")
            except Exception as e:
                messagebox.showerror("Error!",f"Error due to {str(e)}",parent=self.window)

    '''To Reset all the fields'''
    def reset_fields(self):
        self.name_entry.delete(0, END)
        self.surname_entry.delete(0, END)
        self.addr_entry.delete(0, END)
        self.contact_entry.delete(0, END)
        self.email_entry.delete(0, END)

# The main function
if __name__ == "__main__":
    root = Tk()
    obj = Management(root)
    root.mainloop()