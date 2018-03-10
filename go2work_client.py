import tkinter as tk
import tkinter.messagebox
import json
import connection
import defineCommands

employees = ['Igor Mamorski', 'Elad Hezi', 'Alex Melnic', 'Benny Mounits', 'Bibi Netaniahu', 'Oren Hazan', 'Jim Carrey',
             'Guy Cohen', 'Gidi Cohen', 'Gidi Bucks', 'Pamela Anderson', 'Chuck Norris', 'Bill Gates', 'Omer Adam',
             'Bred Pit',
             'Johny Depp', 'Orlando Bloom', 'Penelope Cruz']


class App(tk.Frame):
    data = {}
    active_frame = []

    def update_shift(self, set):
        selection = self.listbox1.curselection()
        message = ""
        for each in selection:
            message = message + employees[each] + "\n"
        if set == 1:
            tkinter.messagebox.showinfo("Shift Update", message + "selected for tomorrow")
        elif set == 2:
            tkinter.messagebox.showinfo("Shift Update", message + "unselected for tomorrow")

    def forget_frames(self):
        for frame in self.active_frame:
            frame.pack_forget()
        self.active_frame.clear()

    def run_algorithm(self):
        self.forget_frames()
        # alg_data = str(defineCommands.RUN_ALGORITHM) + ';{}'
        # result = connection.send_request_to_server(alg_data)
        # if result:
        #     tkinter.messagebox.showinfo("Create Routes", "Creating in process.")
        # else:
        #     tkinter.messagebox.showinfo("Create Routes", "Creating fail.")
        pass

    def get_employees(self):
        self.forget_frames()
        self.show_employee_frame.pack(padx=50, pady=20, anchor='n')
        self.active_frame.append(self.show_employee_frame)
        for name in employees:
            self.listbox1.insert('end', name)
        self.listbox1.grid(row=0, column=1, sticky='w')
        self.scrollbar_V.grid(row=0, column=2, sticky='w')
        self.scrollbar_V.config(command=self.listbox1.yview)
        tk.Button(self.show_employee_frame, text='Set Shift', default='active',
                  command=lambda: self.update_shift(1)).grid(row=1, column=0, sticky='w', pady=10, padx=30, ipady=10,
                                                             ipadx=20)
        tk.Button(self.show_employee_frame, text='Unset Shift', default='active',
                  command=lambda: self.update_shift(2)).grid(row=1, column=1, sticky='w', pady=10, ipady=10, ipadx=20)
        tk.Button(self.show_employee_frame, text='Remove', default='active',
                  command=lambda: self.update_shift(3)).grid(row=1, column=2, sticky='w', pady=10, padx=30, ipady=10,
                                                             ipadx=20)

    def search_employee(self):
        self.forget_frames()
        self.search_frame.pack(padx=50, pady=20, anchor='n')
        self.active_frame.append(self.search_frame)
        var = tk.IntVar()
        var.set(0)
        tk.Radiobutton(self.search_frame, text="By name", variable=var, value=1).grid(row=0, column=0, sticky='w',
                                                                                      pady=10)
        tk.Radiobutton(self.search_frame, text="By id", variable=var, value=2).grid(row=1, column=0, sticky='w',
                                                                                    pady=10)
        tk.Radiobutton(self.search_frame, text="By address", variable=var, value=3).grid(row=2, column=0, sticky='w',
                                                                                         pady=10)
        self.search_input.grid(row=1, column=1, sticky='w')

        pass

    def add_employee(self):
        self.forget_frames()
        self.add_employee_frame.pack(padx=50, pady=100, anchor='n')
        self.active_frame.append(self.add_employee_frame)
        tk.Label(self.add_employee_frame, text='Name', font=("Times New Roman", 14)).grid(row=0, column=0, sticky='w')
        name = self.add_name.grid(row=0, column=1, sticky='w', padx=20)
        tk.Label(self.add_employee_frame, text='Last Name', font=("Times New Roman", 14)).grid(row=1, column=0,
                                                                                               sticky='w')
        last_name = self.add_last_name.grid(row=1, column=1, sticky='w', padx=20)
        tk.Label(self.add_employee_frame, text='Address', font=("Times New Roman", 14)).grid(row=2, column=0,
                                                                                             sticky='w')
        address = self.add_address.grid(row=2, column=1, sticky='w', padx=20)
        tk.Button(self.add_employee_frame, text='Add', font=("Times New Roman", 10), command=lambda: send_to_db()).grid(
            row=3, column=1, sticky='w')

        def send_to_db():
            # add_data = {
            #     'name': name,
            #     'last_name': last_name,
            #     'address': address
            # }
            # json_str = json.dumps(add_data)
            # json_str = str(defineCommands.ADD_EMPLOYEE) + json_str
            # result = connection.send_request_to_server(json_str)
            # if result:
            #     tkinter.messagebox.showinfo("Add Employee", "Employee {} {} successfully added.".format(name, last_name))
            # else:
            #     tkinter.messagebox.showinfo("Add Employee", "Failed to add employee, try later or contact your help desc")
            pass

    def show_login_page(self):
        self.forget_frames()
        self.admin_frame.pack_forget()
        # self.label_frame.pack(padx=50, pady=20, anchor='n')
        # self.active_frame.append(self.label_frame)
        self.dialog_frame.pack(padx=50, pady=20, anchor='w')
        self.active_frame.append(self.dialog_frame)
        tk.Label(self.dialog_frame, text="Login to GO2WORK system", font=("Times New Roman", 16)).grid(row=0, columnspan=3,
                                                                                                       sticky='n',
                                                                                                       padx=20, pady=20)
        tk.Label(self.dialog_frame, text='Username:', font=("Times New Roman", 14)).grid(row=1, column=0, sticky='w',
                                                                                         padx=20)
        self.user_input = tk.Entry(self.dialog_frame, background='white', width=24)
        self.user_input.grid(row=1, column=1, sticky='w', padx=20)
        self.user_input.focus_set()
        tk.Label(self.dialog_frame, text='Password:', font=("Times New Roman", 14)).grid(row=2, column=0, sticky='w',
                                                                                         padx=20)
        self.pass_input.grid(row=2, column=1, sticky='w', padx=20)
        tk.Button(self.dialog_frame, text='OK', default='active', command=lambda: self.click_ok()).grid(row=3, column=0,
                                                                                                        sticky='w',
                                                                                                        padx=20,
                                                                                                        pady=20,
                                                                                                        ipady=10,
                                                                                                        ipadx=20)
        tk.Button(self.dialog_frame, text='Cancel', default='active', command=lambda: self.click_cancel()).grid(row=3,
                                                                                                                column=1,
                                                                                                                sticky='w',
                                                                                                                padx=20,
                                                                                                                pady=20,
                                                                                                                ipady=10,
                                                                                                                ipadx=20)

    def show_admin_page(self):
        self.forget_frames()
        self.admin_frame.pack(padx=20, pady=15)
        tk.Button(self.admin_frame, text='Show Employee List', font=("Times New Roman", 10),
                  command=lambda: self.get_employees()).grid(row=0, column=0)
        tk.Button(self.admin_frame, text='Create Routes', font=("Times New Roman", 10),
                  command=lambda: self.run_algorithm()).grid(row=0, column=2)
        tk.Button(self.admin_frame, text='Search Employee', font=("Times New Roman", 10),
                  command=lambda: self.search_employee()).grid(row=0, column=3)
        tk.Button(self.admin_frame, text='Add Employee', font=("Times New Roman", 10),
                  command=lambda: self.add_employee()).grid(row=0, column=4)
        tk.Button(self.admin_frame, text='Logout', font=("Times New Roman", 10),
                  command=lambda: self.show_login_page()).grid(row=0, column=5)

    def click_ok(self):
        self.data['username'] = self.user_input.get()
        self.data['password'] = self.pass_input.get()
        self.pass_input.delete(0, len(self.data['password']))
        # json_str = json.dumps(data)
        # json_str = '1;' + json_str
        # result = connection.send_request_to_server(json_str)
        # print(result)
        # for debug it's hardcoded
        if self.data['username'] == 'root' and self.data['password'] == 'root':
            result = True
        else:
            result = False

        if result:
            # tkinter.messagebox.showinfo("Login page", "Hello, " + self.data['username'])
            # self.label_frame.destroy()
            # self.dialog_frame.destroy()
            self.show_admin_page()
        else:
            tkinter.messagebox.showwarning("Login page", "The User Name or Password is incorrect.")

    def click_cancel(self):
        msg = tkinter.messagebox.askyesno("Login page", "Are you sure you want to cancel login?")
        if msg:
            exit()

    def __init__(self, master):
        tk.Frame.__init__(self, master)
        self.label_frame = tk.Frame(self)
        self.dialog_frame = tk.Frame(self)
        self.show_employee_frame = tk.Frame(self)
        self.admin_frame = tk.Frame(self)
        self.search_frame = tk.Frame(self)
        self.add_employee_frame = tk.Frame(self)
        self.user_input = tk.Entry(self.dialog_frame, background='white', width=24)
        self.pass_input = tk.Entry(self.dialog_frame, background='white', width=24, show='*')
        self.search_input = tk.Entry(self.search_frame, background='white', width=24)
        self.add_name = tk.Entry(self.add_employee_frame, background='white', width=24)
        self.add_last_name = tk.Entry(self.add_employee_frame, background='white', width=24)
        self.add_address = tk.Entry(self.add_employee_frame, background='white', width=24)
        self.pack()
        self.master.title("GO2WORK")
        self.master.geometry('720x480')
        self.scrollbar_V = tk.Scrollbar(self.show_employee_frame)
        self.listbox1 = tk.Listbox(self.show_employee_frame, yscrollcommand=self.scrollbar_V.set, height=15,
                                   selectmode='multiple')
        self.show_login_page()


if __name__ == '__main__':
    root = tk.Tk()
    app = App(root)
    app.mainloop()
