import tkinter as tk
import random
from tkinter import CENTER, E, END, RIGHT, W, Y, Button, Entry, Label, Scrollbar, ttk
from tkinter import messagebox
import database as bk


HEIGHT = 525
WIDTH = 700

class ProjectList():
     
    def __init__(self):
        self.my_database = bk.BackEnd()
        self.window = tk.Tk()
            
        #CENTER THE WINDOW
        
        ws = self.window.winfo_screenwidth()
        hs = self.window.winfo_screenheight()
        
        corner_x = (ws/2) - (WIDTH/2)
        corner_y = (hs/2) - (HEIGHT/2)
        
        self.window.geometry(f"{WIDTH}x{HEIGHT}+{int(corner_x)}+{int(corner_y)}") #centers the window
        self.window.resizable(False, False)
        self.window.configure(bg='lightsteelblue2')
        self.window.title("A To Do List")
        
        #Allows to use the functions
        self.database_frame = self.create_database_frame()
        self.database_treeview = self.display_database_treeview()
        self.label_entry_frame = self.create_label_entry_frame()
        self.buttons_frame = self.create_button_frame()
        self.create_buttons = self.button_functions()
        
        #Labels
        labels = ["To Do", "Programming Language", "Start", "Target"]
        
        #Instead of having to use multiple lines to create the labels, using a for loop would save time and lines
        counter_label = 0
        for value_labels in labels:
            text_label = Label(self.label_entry_frame, text=value_labels, bg="lightsteelblue3", font=("DM Sans", 11))
            text_label.grid(row=0, column=counter_label)
            counter_label+=1
         
        #Entry - did not use a for loop as each entry had to be unique to be able to use the .get()
        self.to_do = Entry(self.label_entry_frame, font=("DM Sans", 10, "italic"))
        self.to_do.grid(row=1, column=0, padx=10, pady=10)
        self.to_do.focus_set()
        
        self.programming_lang = Entry(self.label_entry_frame, font=("DM Sans", 10, "italic"))
        self.programming_lang.insert(0, "NA")
        self.programming_lang.grid(row=1, column=1, padx=10, pady=10)
        self.programming_lang.bind('<FocusIn>', lambda event: self.programming_lang.selection_range(0, END))
        
        self.start_date = Entry(self.label_entry_frame, font=("DM Sans", 10, "italic"))
        self.start_date.insert(0, "NA")
        self.start_date.grid(row=1, column=2, padx=10, pady=10)
        self.start_date.bind('<FocusIn>', lambda event: self.start_date.selection_range(0, END))

        self.target_date = Entry(self.label_entry_frame, font=("DM Sans", 10, "italic"))
        self.target_date.insert(0, "NA")
        self.target_date.grid(row=1, column=3, padx=10, pady=10)
        self.target_date.bind('<FocusIn>', lambda event: self.target_date.selection_range(0, END))
        

        self.database_treeview.tag_configure('oddrow', background="skyblue3")
        self.database_treeview.tag_configure('evenrow', background="skyblue4")
        
        # print(self.database_treeview)
        
    def selected_records(self, event):
        self.to_do.delete(0,tk.END)
        self.programming_lang.delete(0,tk.END)
        self.start_date.delete(0,tk.END)
        self.target_date.delete(0,tk.END)
        
        row_id = self.database_treeview.selection()
        select = self.database_treeview.item(row_id, 'values')
        # print(select)

        self.to_do.insert(0,select[0])
        self.programming_lang.insert(0,select[1])
        self.start_date.insert(0,select[2])
        self.target_date.insert(0,select[3])
            
    def refresh(self):
        self.window.destroy()
        self.__init__()
        
    def add_record(self):
        current_val = self.my_database.showProjects()[-1][5]
        #print("test", current_val)
        if self.to_do.get() == "":
            tk.messagebox.showinfo(title="Entry", message="Must have a project")
        else:
            if (current_val) % 2 == 0:
                #print(self.to_do.get(), self.programming_lang.get(), self.start_date.get(), self.target_date.get())
                capitalise_title = " ".join(title[0].upper()+title[1:] for title in self.to_do.get().split())
                self.database_treeview.insert(parent='', 
                                                index='end', 
                                                iid=None, 
                                                values=(capitalise_title, self.programming_lang.get(), self.start_date.get(), self.target_date.get(), "No"), 
                                                tags=('evenrow'))
                
                self.my_database.insertProjectName(capitalise_title, 
                                        self.programming_lang.get(), 
                                        self.start_date.get(), 
                                        self.target_date.get(), "No")

                self.to_do.delete(0, tk.END)
                self.programming_lang.delete(0, tk.END)
                self.programming_lang.insert(0, "NA")
                self.start_date.delete(0, tk.END)
                self.start_date.insert(0, "NA")
                self.target_date.delete(0, tk.END)
                self.target_date.insert(0, "NA")
                current_val+=1
                self.refresh()
            else:
                #print(self.to_do.get(), self.programming_lang.get(), self.start_date.get(), self.target_date.get())
                capitalise_title = " ".join(title[0].upper()+title[1:] for title in self.to_do.get().split())
                self.database_treeview.insert(parent='', 
                                                index='end', 
                                                iid=None, 
                                                values=(capitalise_title, self.programming_lang.get(), self.start_date.get(), self.target_date.get(), "No"),
                                                tags=('oddrow'))
                
                self.my_database.insertProjectName(capitalise_title, 
                                        self.programming_lang.get(), 
                                        self.start_date.get(), 
                                        self.target_date.get(), "No")

                self.to_do.delete(0, tk.END)
                self.programming_lang.delete(0, tk.END)
                self.programming_lang.insert(0, "NA")
                self.start_date.delete(0, tk.END)
                self.start_date.insert(0, "NA")
                self.target_date.delete(0, tk.END)
                self.target_date.insert(0, "NA")
                current_val+=1
                self.refresh()
                
    def delete_records(self):
        selected_items = self.database_treeview.selection()
        new_list = []
        for selected_item in selected_items:
            store = self.database_treeview.item(selected_item, 'values')[5] #gets the id
            print("l", store)
            new_list.append(store)
        
        if len(new_list)>1:
            msg_box = tk.messagebox.askquestion('Delete Record',
                                                'Are you sure you want to delete?',
                                                icon = 'warning')
            
            if msg_box == "yes":
                for items in selected_items:
                    self.database_treeview.delete(items)
                bk.deleteProjects(new_list)
                self.refresh()
        elif new_list:
            self.database_treeview.delete(selected_items)
            self.my_database.deleteProjects(new_list)
            self.refresh()
        else:
            tk.messagebox.showinfo(title="Error", 
                                    message="Must select record")
                
    def complete_selected_projects(self):
        selected_items = self.database_treeview.selection()
        new_list = []
        for selected_item in selected_items:
            store = self.database_treeview.item(selected_item, 'values')[5]
            #print(store)
            new_list.append(store)
        
        print(new_list)
        if not new_list:
            tk.messagebox.showinfo(title="Error",
                                    message="Must select record")
        else:
            self.my_database.completedProject(new_list)  
            self.refresh()
            
    def incomplete_selected_projects(self):
        selected_items = self.database_treeview.selection()
        new_list = []
        for selected_item in selected_items:
            store = self.database_treeview.item(selected_item, 'values')[5]
            #print(store)
            new_list.append(store)
        if not new_list:
            tk.messagebox.showinfo(title="Error", message="Must select record")
        else:
            self.my_database.incompletedProject(new_list) 
            self.refresh()
            
        return new_list
                
    def update_record(self):
        try:
            selected_items = self.database_treeview.selection()
            store = self.database_treeview.item(selected_items, 'values')[5]
            print("This is the value ", store)
            # val = store
            print(len(selected_items))
            if self.to_do.get() == "":
                tk.messagebox.showinfo(title="Error", message="Must enter project title", icon='warning')
            else:
                self.my_database.updateProject(self.to_do.get(), self.programming_lang.get(), self.start_date.get(), self.target_date.get(), "No", store)
                self.refresh()
        except:
            tk.messagebox.showinfo(title="Error", message="Must select ONE record", icon='warning')
            
        
    def randomise(self):
        try:
            items = []
            new_list = []
            for i in self.database_treeview.get_children():
                if self.database_treeview.item(i)['values'][4] == "No" and self.database_treeview.item(i)['values'][2] == "NA" and self.database_treeview.item(i)['values'][3] == "NA":
                    new_list.append(i)
            rand_opt = random.choice(new_list)
            if rand_opt in items:
                if len(items) == len(new_list):
                    items.clear()
                return self.randomise()
            self.database_treeview.selection_set(rand_opt)
            hi = " ".join(w.capitalize() for w in self.database_treeview.item(rand_opt)['values'][0].split())
                
            messagebox.showinfo(title="Project", message=hi)
            items.append(rand_opt)
        except IndexError:
            tk.messagebox.showinfo(title="Error", message="Can only randomly select projects with no start or target date", icon='warning')
        
        #Button functionality 
    def button_functions(self): 
        self.add_button = Button(self.buttons_frame, text="Insert", bg="lightsteelblue3", font=("DM Sans", 13, "italic"), borderwidth=1, command = self.add_record)
        self.add_button.grid(row=2, column=0, padx=10, pady=20)
        
        self.update_button = Button(self.buttons_frame, text="Update", bg="lightsteelblue3", font=("DM Sans", 13, "italic"), borderwidth=1, command = self.update_record)
        self.update_button.grid(row=2, column=1, padx=10, pady=20)
        
        self.delete_button = Button(self.buttons_frame, text="Delete", bg="lightsteelblue3", font=("DM Sans", 13, "italic"), borderwidth=1, command = self.delete_records)
        self.delete_button.grid(row=2, column=2, padx=10, pady=20)
        
        self.completed_button = Button(self.buttons_frame, text="Complete", bg="lightsteelblue3", font=("DM Sans", 13, "italic"), borderwidth=1, command = self.complete_selected_projects)
        self.completed_button.grid(row=2, column=3, padx=10, pady=20)
        
        self.incompleted_button = Button(self.buttons_frame, text="Incomplete", bg="lightsteelblue3", font=("DM Sans", 13, "italic"), borderwidth=1, command = self.incomplete_selected_projects)
        self.incompleted_button.grid(row=2, column=4, padx=10, pady=20)
        
        self.random_button = Button(self.buttons_frame, text="Randomise", bg="lightsteelblue3", font=("DM Sans", 13, "italic"), borderwidth=1, command = self.randomise)
        self.random_button.grid(row=2, column=5, padx=10, pady=20)
        
        self.reset_button = Button(self.buttons_frame, text="Reset", bg="lightsteelblue3", font=("DM Sans", 13, "italic"), borderwidth=1, command = self.refresh)
        self.reset_button.grid(row=2, column=6, padx=10, pady=20)
    
        self.database_treeview.bind('<Double-Button-1>',self.selected_records)
    #Shows the treeview with rows and headings
    def display_database_treeview(self):
        tree_scroll_bar = Scrollbar(self.database_frame, orient='vertical')
        tree_scroll_bar.pack(side=RIGHT, fill=Y)
        database_tree = ttk.Treeview(self.database_frame, show="headings", selectmode="extended", yscrollcommand=tree_scroll_bar.set)
        tree_scroll_bar.config(command=database_tree.yview, bg='lightsteelblue2')
        # database_tree.bind('<Motion>', 'break')
        database_tree['columns'] = ["To Do", "Programming Language", "Start Date", "Target Date", "Done"]
        
        #Styling the treeview
        style = ttk.Style()
        style.theme_use('default')
        style.configure('Treeview.Heading', foreground='black', anchor=E, background="skyblue2", borderwidth = 0.5)
        style.configure("Treeview",
        background="skyblue2",
        foreground="black",
        rowheight=25,
        fieldbackground="skyblue2",
        borderwidth = 1)
        style.configure("Vertical.TScrollbar", background="green", bordercolor="red", arrowcolor="white")
        
        style.map('Treeview',
        background=[('selected', "LightSteelBlue4")])
        #Creating the columns and headings
        database_tree.column('#0', width="150")
        database_tree.heading('#0', text='\n')
        for values in database_tree['columns']:
            if values == "Start Date" or values == "Target Date":
                database_tree.column(values, width=100, anchor=CENTER)
                database_tree.heading(values, text = values)
            elif values == "To Do":
                database_tree.column(values, width=250, anchor=CENTER)
                database_tree.heading(values, text = values)     
            elif values == "Done":
                database_tree.column(values, width=50, anchor=CENTER)
                database_tree.heading(values, text = values)                          
            else:
                database_tree.column(values, width=150, anchor=CENTER)
                database_tree.heading(values, text = values)
        
        #Styles rows - makes it into stripes
        database_tree.tag_configure('completed', background="lightskyblue1")
        # print("THIS IS THE DATABASE", self.my_database.showProjects())
        counter = 0
        for projects in self.my_database.showProjects():
            if counter % 2 == 0:
                if projects[4] == "Yes":
                    database_tree.insert(parent='', index='end', iid=None, text='', values=(projects), tags=('completed'))
                else:
                    database_tree.insert(parent='', index='end', iid=None, text='', values=(projects), tags=('evenrow'))
            else:
                if projects[4] == "Yes":
                    database_tree.insert(parent='', index='end', iid=None, text='', values=(projects), tags=('completed'))
                else:
                    database_tree.insert(parent='', index='end', iid=None, text='', values=(projects), tags=('oddrow'))
            counter+=1
        
        database_tree.pack(expand="yes")
        return database_tree
        
    def create_database_frame(self):
        frame = tk.Frame(self.window, height = 250, width = 200, bg="grey")
        frame.pack(fill="y", padx=10)
        return frame
    
    def create_label_entry_frame(self):
        frame = tk.LabelFrame(self.window, text="Record", background="lightsteelblue3")
        frame.pack(fill="x", expand="yes", padx=15, pady=10)
        return frame
    
    def create_button_frame(self):
        frame = tk.LabelFrame(self.window, text="Commands", background="lightsteelblue3")
        frame.pack(fill="x", expand="yes", padx=15, pady=20)
        return frame

    def run(self):
        self.window.mainloop()

if __name__ == "__main__":
    projectList = ProjectList()
    projectList.run()


