import tkinter as tk
import tkinter.messagebox
import json
import connection
import defineCommands
import validate_address
import openmap
import os


# employees = ['Igor Mamorski', 'Elad Hezi', 'Alex Melnic', 'Benny Mounits', 'Bibi Netaniahu', 'Oren Hazan', 'Jim Carrey',
#              'Guy Cohen', 'Gidi Cohen', 'Gidi Bucks', 'Pamela Anderson', 'Chuck Norris', 'Bill Gates', 'Omer Adam',
#              'Bred Pit',
#              'Johny Depp', 'Orlando Bloom', 'Penelope Cruz']

#img = tk.PhotoImage()

# receved_routes = {'1': {'1': {'empID': 1231, 'address': 'Sarig St 5 Karmiel', 'firstname': 'igor', 'lastname': 'mamorski'},'2': {'empID': 1234, 'address': 'Ramim St 37 Karmiel', 'firstname': 'vered', 'lastname': 'hezi'},'3': {'empID': 1233, 'address': 'Ha-Dekel St 56 Karmiel', 'firstname': 'elad', 'lastname': 'hezi'},'4': {'empID': 1230, 'address': 'Snunit St 51 Karmiel', 'firstname': 'root', 'lastname': 'root'},'5': {'empID': 1235, 'address': 'Arava St 10 Karmiel', 'firstname': 'ronaldo', 'lastname': 'bloom'},'6': {'empID': 1236, 'address': 'HaShoshanim Street 4 Karmiel', 'firstname': 'johni', 'lastname': 'depp'}},'2': {'1': {'empID': 123456789, 'address': 'pinsker st 15 kiryat ata', 'firstname': 'omer', 'lastname': 'adam'}, '2': {'empID': 1237, 'address': 'Sderot Jabotinsky 10 Kiryat Yam', 'firstname': 'bibi', 'lastname': 'nati'},'3': {'empID': 2030405, 'address': 'kiryat ata, histadrut 10', 'firstname': 'oren', 'lastname': 'hazan'}}}
bgrd_color = 'deep sky blue'
btn_bg_color = 'OliveDrab1'# 'light blue'
lbl_bg_color = 'deep sky blue'
radio_color = 'saddle brown'
radio_font = ("Times New Roman", 14, 'bold')
lbl_font = font=("Times New Roman", 16, 'bold')
lbl_color = 'saddle brown'
# noinspection PyAttributeOutsideInit
class App(tk.Frame):
    data = {}
    active_frame = []

    def forget_frames(self):
        for frame in self.active_frame:
            frame.pack_forget()
        self.active_frame.clear()

    def update_shift_or_delete_worker(self, set_shift, employees):
        selection = self.listbox1.curselection()
        if len(selection) == 0:
            tkinter.messagebox.showinfo("Update", "No one is selected")
            return
        message = ""
        sub_message = ['unselected for tomorrow', 'selected for tomorrow', 'deleted']
        shift_data = []
        index = 0
        for each in selection:
            message = message + employees[each]['firstname'] + ' ' + employees[each]['lastname'] + "\n"
            shift_data.append({})
            shift_data[index]['empID'] = employees[each]['empID']
            shift_data[index]['status'] = set_shift
            index += 1
        if set_shift != 2:
            json_str = json.dumps(shift_data)
            json_str = str(defineCommands.SET_WORKER) + ';' + json_str
            result = connection.send_request_to_server(json_str)
        else:
            msg = tkinter.messagebox.askyesno("Delete", "Are you sure you want to delete this worker?")
            if msg:
                json_str = json.dumps(shift_data)
                json_str = str(defineCommands.REMOVE_EMPLOYEE) + ';' + json_str
                result = connection.send_request_to_server(json_str)
            else: 
                return
        if result:
            tkinter.messagebox.showinfo("Update", message + sub_message[set_shift])
        else:
            tkinter.messagebox.showinfo("Update", "We got some error...\nApparently aliens stole your data")
        self.get_employees(0)

    def run_algorithm(self):
        self.forget_frames()
        self.run_algo_frame = tk.Frame(self)
        self.run_algo_frame.pack(fill='both')
        self.run_algo_frame.configure(bg=bgrd_color, pady=100)
        self.active_frame.append(self.run_algo_frame)
        tk.Label(self.run_algo_frame, text='Number of vehicles', bg=lbl_bg_color, fg=lbl_color, font=lbl_font).grid(row=0, column=0, sticky='w', pady=10, padx=50)
        self.num_of_vehicles = tk.Entry(self.run_algo_frame, background='white', width=5)
        self.num_of_vehicles.insert('end', 4)
        self.num_of_vehicles.grid(row=0, column=1, sticky='w', pady=10)
        tk.Label(self.run_algo_frame, text='Quality of routes', bg=lbl_bg_color, fg=lbl_color, font=lbl_font).grid(row=1, column=0, sticky='w', pady=30, padx=50)
        var = tk.IntVar()
        var.set(1)
        tk.Radiobutton(self.run_algo_frame, bg=lbl_bg_color, text="low", fg=radio_color, font=radio_font, variable=var, value=0).grid(row=1, column=1, sticky='w')
        tk.Radiobutton(self.run_algo_frame, bg=lbl_bg_color, text="medium", fg=radio_color, font=radio_font, variable=var, value=1).grid(row=1, column=2, sticky='w')
        tk.Radiobutton(self.run_algo_frame, bg=lbl_bg_color, text="high", fg=radio_color, font=radio_font, variable=var, value=2).grid(row=1, column=3, sticky='w')
        tk.Button(self.run_algo_frame, bg=btn_bg_color, text='Create', default='active', command=lambda: run()).grid(row=3, column=1)
        def run():
            quality = ['low', 'medium', 'high']
            if self.num_of_vehicles == "":
                tkinter.messagebox.showinfo("Create Routes", "Please, enter number of vehicles.")
                return
            if not self.num_of_vehicles.get().isdigit():
                tkinter.messagebox.showinfo("Create Routes", "Please, enter only digits.")
                return
            alg_data = {
                'numofvehicles': int(self.num_of_vehicles.get()),
                'routequality' : quality[var.get()]
            }
            json_str = json.dumps(alg_data)
            json_str = str(defineCommands.RUN_ALGORITHM) + ';' + json_str
            result = connection.send_request_to_server(json_str)
            if result:
                tkinter.messagebox.showinfo("Create Routes", "Creating in process.")
            else:
                tkinter.messagebox.showinfo("Create Routes", "Creating fail.")

    def check_algorithm_status(self):
        self.forget_frames()
        self.check_frame = tk.Frame(self)
        self.check_frame.pack(fill='both')
        self.check_frame.configure(bg=bgrd_color, pady=70)
        self.active_frame.append(self.check_frame)
        request = str(defineCommands.CHECK_ALGORITHM_STATUS) + ';{}'
        result = connection.send_request_to_server(request)
        if result:
            tkinter.messagebox.showinfo("Check route status", "Creating in process.")
        else:
            tkinter.messagebox.showinfo("Check route status", "No process found")

    def get_employees(self, employee_list):
        self.forget_frames()
        self.show_employee_frame = tk.Frame(self)
        self.show_employee_frame.pack(fill='both')
        self.active_frame.append(self.show_employee_frame)
        self.show_employee_frame.configure(background=bgrd_color, pady=50)
        self.scrollbar_V = tk.Scrollbar(self.show_employee_frame)
        self.listbox1 = tk.Listbox(self.show_employee_frame, yscrollcommand=self.scrollbar_V.set, height=15,
                                   width=40, selectmode='multiple')
        if employee_list == 0:
            get_data = str(defineCommands.GET_EMPLOYEE_LIST) + ';{}'
            received_data = connection.send_request_to_server(get_data)
            # received_data = result.decode("utf-8")
        else:
            received_data = employee_list
        if received_data != '':
            received_data = json.loads(received_data)
        for employee in received_data:
            self.listbox1.insert('end', employee['firstname'] + ' ' + employee['lastname'] + ' - Status ' + str(employee['status']))
        self.listbox1.grid(rowspan=5, row=0, column=1, sticky='w', pady=50)
        self.scrollbar_V.grid(row=0, rowspan=5, column=2, sticky='w')
        self.scrollbar_V.config(command=self.listbox1.yview)
        tk.Button(self.show_employee_frame, bg=btn_bg_color, text='Set Shift', default='active', command=lambda: self.update_shift_or_delete_worker(1, received_data)).grid(row=0, column=0, sticky='w',
                                                                                             ipady=10, ipadx=20, pady=20, padx=50)
        tk.Button(self.show_employee_frame, bg=btn_bg_color, text='Unset Shift', default='active',
                  command=lambda: self.update_shift_or_delete_worker(0, received_data)).grid(row=1, column=0, sticky='w',
                                                                                             ipady=10, ipadx=12, pady=20, padx=50)
        tk.Button(self.show_employee_frame, bg=btn_bg_color, text='Remove', default='active',
                  command=lambda: self.update_shift_or_delete_worker(2, received_data)).grid(row=2, column=0, sticky='w',
                                                                                             pady=20, ipady=10, ipadx=20, padx=50)
        tk.Button(self.show_employee_frame, bg=btn_bg_color, text='Update', default='active',
                  command=lambda: self.update_worker(received_data)).grid(row=3, column=0, sticky='w', ipady=10,
                                                                          ipadx=20, pady=20, padx=50)

    def update_worker(self, employees):
        selection = self.listbox1.curselection()
        if len(selection) == 0:
            tkinter.messagebox.showinfo("Update", "No one is selected")
            return
        if len(selection) > 1:
            tkinter.messagebox.showinfo("Update", "You should select only one person")
            return
        window = tk.Toplevel(root)
        window.configure(background=bgrd_color)
        self.add_name = tk.Entry(window, background='white', width=24)
        self.add_name.insert('end', employees[selection[0]]['firstname'])
        self.add_name.grid(row=0, column=1, sticky='w', padx=20)
        self.add_last_name = tk.Entry(window, background='white', width=24)
        self.add_last_name.grid(row=1, column=1, sticky='w', padx=20)
        self.add_last_name.insert('end', employees[selection[0]]['lastname'])
        self.add_address = tk.Entry(window, background='white', width=24)
        self.add_address.grid(row=2, column=1, sticky='w', padx=20)
        self.add_address.insert('end', employees[selection[0]]['address'])
        self.add_id = tk.Entry(window, background='white', width=24)
        self.add_id.grid(row=3, column=1, sticky='w', padx=20)
        self.add_id.insert('end', employees[selection[0]]['empID'])
        self.add_status = tk.Entry(window, background='white', width=24)
        self.add_status.grid(row=4, column=1, sticky='w', padx=20)
        self.add_status.insert('end', employees[selection[0]]['status'])
        tk.Label(window, text='Name', bg=lbl_bg_color, fg=lbl_color,
                 font=lbl_font).grid(row=0, column=0, sticky='w')
        tk.Label(window, text='Last Name', bg=lbl_bg_color, fg=lbl_color, font=lbl_font).grid(
            row=1, column=0, sticky='w')
        tk.Label(window, text='Address', bg=lbl_bg_color, fg=lbl_color, font=lbl_font).grid(
            row=2, column=0, sticky='w')
        tk.Label(window, text='Id', bg=lbl_bg_color, fg=lbl_color, font=lbl_font).grid(row=3, column=0, sticky='w')
        tk.Label(window, text='Status', bg=lbl_bg_color, fg=lbl_color, font=lbl_font).grid(
            row=4, column=0, sticky='w')
        tk.Button(window, text='Update', bg=btn_bg_color, font=("Times New Roman", 10),
                  command=lambda: make_update()).grid(row=5, column=0, sticky='w', padx=20, pady=20)
        tk.Button(window, text='Cancel', bg=btn_bg_color, font=("Times New Roman", 10),
                  command=lambda: window.destroy()).grid(row=5, column=1, sticky='w', pady=20)

        def make_update():
            if (self.add_status.get() == '' or self.add_address.get() == '' or self.add_last_name.get() == ''
                    or self.add_name.get() == '' or self.add_id.get() == ''):
                tkinter.messagebox.showinfo("Update", "You should fill all fields")
                return
            try:
                address = validate_address.validate_address(self.add_address.get())
            except:
                address = False
            if not address:
                tkinter.messagebox.showinfo("Update", "Address is not valid, please enter valid address")
                return
            if not self.add_id.get().isdigit():
                tkinter.messagebox.showinfo("Update", "Id must be only digit")
                return
            add_data = {
                'firstname': self.add_name.get(),
                'lastname': self.add_last_name.get(),
                'address': self.add_address.get(),
                'empID': self.add_id.get(),
                'status': self.add_status.get()
            }
            json_str = json.dumps(add_data)
            json_str = str(defineCommands.UPDATE) + ';' + json_str
            result = connection.send_request_to_server(json_str)
            if result:
                tkinter.messagebox.showinfo("Update", "Success")
                self.get_employees(0)
                window.destroy()
            else:
                tkinter.messagebox.showinfo("Update", "Error")

    def search_employee(self):
        self.forget_frames()
        self.search_frame = tk.Frame(self)
        self.search_frame.pack(fill='both')
        self.search_frame.configure(background=bgrd_color, pady=70, padx=130)
        self.active_frame.append(self.search_frame)
        var = tk.IntVar()
        var.set(0)
        tk.Radiobutton(self.search_frame, bg=lbl_bg_color, fg=radio_color, text="By name", font=radio_font, variable=var, value=1).grid(row=0, column=0, sticky='w', pady=10)
        tk.Radiobutton(self.search_frame, bg=lbl_bg_color, fg=radio_color, text="By id", font=radio_font, variable=var, value=2).grid(row=1, column=0, sticky='w', pady=10)
        tk.Radiobutton(self.search_frame, bg=lbl_bg_color, fg=radio_color, text="By address", font=radio_font, variable=var, value=3).grid(row=2, column=0, sticky='w', pady=10)
        self.search_input = tk.Entry(self.search_frame, background='white', width=24)
        self.search_input.grid(row=1, column=1, sticky='w')
        tk.Button(self.search_frame, bg=btn_bg_color, text='Search', font=("Times New Roman", 10), command=lambda: send_to_db()).grid(row=3, column=1, sticky='w', pady=20)

        def send_to_db():
            if self.search_input.get() == "":
                tkinter.messagebox.showinfo("Search", "Search field is empty")
                return
            if var == 0:
                tkinter.messagebox.showinfo("Search", "Please, check one parameter")
                return
            search_types = ['firstname', 'empID', 'address']
            search_data = {
                'searchby': search_types[var.get() - 1],
                search_types[var.get() - 1]: self.search_input.get()
            }
            json_str = json.dumps(search_data)
            json_str = str(defineCommands.SEARCH) + ';' + json_str
            result = connection.send_request_to_server(json_str)
            if result:
                self.get_employees(result)
            else:
                tkinter.messagebox.showinfo("Search", "Not Found")

    def add_employee(self):
        self.forget_frames()
        self.add_employee_frame = tk.Frame(self)
        self.add_employee_frame.pack(fill='both')
        self.add_employee_frame.configure(background=bgrd_color, pady=70, padx=130)
        self.active_frame.append(self.add_employee_frame)
        self.add_name = tk.Entry(self.add_employee_frame, background='white', width=24)
        self.add_name.grid(row=0, column=1, sticky='w', padx=20)
        self.add_last_name = tk.Entry(self.add_employee_frame, background='white', width=24)
        self.add_last_name.grid(row=1, column=1, sticky='w', padx=20)
        self.add_address = tk.Entry(self.add_employee_frame, background='white', width=24)
        self.add_address.grid(row=2, column=1, sticky='w', padx=20)
        self.add_id = tk.Entry(self.add_employee_frame, background='white', width=24)
        self.add_id.grid(row=3, column=1, sticky='w', padx=20)
        tk.Label(self.add_employee_frame, bg=lbl_bg_color, fg=lbl_color, text='Name', font=lbl_font).grid(row=0, column=0, sticky='w')
        tk.Label(self.add_employee_frame, bg=lbl_bg_color, fg=lbl_color, text='Last Name', font=lbl_font).grid(row=1, column=0, sticky='w')
        tk.Label(self.add_employee_frame, bg=lbl_bg_color, fg=lbl_color, text='Address', font=lbl_font).grid(row=2, column=0, sticky='w')
        tk.Label(self.add_employee_frame, bg=lbl_bg_color, fg=lbl_color, text='Id', font=lbl_font).grid(row=3, column=0, sticky='w')
        tk.Button(self.add_employee_frame, bg=btn_bg_color, text='Add', font=("Times New Roman", 10), command=lambda: send_to_db()).grid(row=5, column=1, sticky='w')

        def send_to_db():
            if (self.add_name.get() == "" or self.add_last_name.get() == "" or self.add_address.get() == ""
                    or self.add_id.get() == ""):
                tkinter.messagebox.showinfo("Add Employee", "One or more entries is empty")
                return
            try:
                address = validate_address.validate_address(self.add_address.get())
            except:
                address = False
            if not address:
                tkinter.messagebox.showinfo("Update", "Address is not valid, please enter valid address")
                return
            if not self.add_id.get().isdigit():
                tkinter.messagebox.showinfo("Update", "Id must be only digit")
                return
            add_data = {
                'firstname': self.add_name.get(),
                'lastname': self.add_last_name.get(),
                'address': self.add_address.get(),
                'empID': self.add_id.get(),
                'status': 0
            }
            json_str = json.dumps(add_data)
            json_str = str(defineCommands.ADD_EMPLOYEE) + ';' + json_str
            result = connection.send_request_to_server(json_str)
            if result:
                tkinter.messagebox.showinfo("Add Employee",
                                            "Employee {} {} successfully added.".format(add_data['firstname'],
                                                                                        add_data['lastname']))
            else:
                tkinter.messagebox.showinfo("Add Employee",
                                            "Failed to add employee, try later or contact your help desc")

    def show_login_page(self):
        self.forget_frames()
        self.admin_frame.pack_forget()
        self.dialog_frame = tk.Frame(self)
        self.dialog_frame.configure(background=bgrd_color)
        self.user_input = tk.Entry(self.dialog_frame, background='white', width=24)
        self.pass_input = tk.Entry(self.dialog_frame, background='white', width=24, show='*')
        self.user_input.insert('end', 'root')
        self.pass_input.insert('end', 'root')
        self.dialog_frame.pack()
        self.active_frame.append(self.dialog_frame)
        tk.Label(self.dialog_frame, text="Login to GO2WORK system", bg=lbl_bg_color, fg=lbl_color, font=("Times New Roman", 22)).grid(row=0, columnspan=3, sticky='n', pady=80)
        tk.Label(self.dialog_frame, text='Username:', bg=lbl_bg_color, fg=lbl_color, font=lbl_font).grid(row=1, column=0, sticky='w')
        self.user_input = tk.Entry(self.dialog_frame, background='white', width=24)
        self.user_input.grid(row=1, column=1, sticky='w', padx=20)
        self.user_input.focus_set()
        tk.Label(self.dialog_frame, text='Password:', bg=lbl_bg_color, fg=lbl_color, font=lbl_font).grid(row=2, column=0, sticky='w')
        self.pass_input.grid(row=2, column=1, sticky='w', padx=20)
        tk.Button(self.dialog_frame, text='   Ok    ', default='active', bg=btn_bg_color, command=lambda: self.click_ok()).grid(row=1, column=2, sticky='w')
        tk.Button(self.dialog_frame, text='Cancel', default='active', bg=btn_bg_color, command=lambda: self.click_cancel()).grid(row=2, column=2, sticky='w')

    def show_route_page(self):
        self.forget_frames()
        self.route_frame = tk.Frame(self)
        self.route_frame.pack(fill='both')
        self.route_frame.configure(background=bgrd_color, pady=50)
        self.active_frame.append(self.route_frame)
        route_data = str(defineCommands.GET_ROUTES) + ";{}"
        received_data = connection.send_request_to_server(route_data)
        # received_data = result.decode("utf-8")
        received_data = json.loads(received_data)
        # received_data = receved_routes
        index = 0
        routes = []
        for vehicle in received_data:
            index += 1
            i = 1
            tk.Button(self.route_frame, bg = btn_bg_color, text='Route {}'.format(index), font=("Times New Roman", 10),
                      command=lambda j=index-1:openmap.openmap(routes, j)).grid(row=0, column=index-1, sticky='w', pady=15)
            for employee in received_data[vehicle]:
                routes.append([])
                routes[index-1].append(received_data[vehicle][employee]["address"])
                my_str = received_data[vehicle][employee]['firstname'] + ' ' + received_data[vehicle][employee]['lastname']
                tk.Label(self.route_frame, text=my_str, bg=lbl_bg_color, fg=lbl_color, font=("Times New Roman", 14)).grid(row=i, column=index-1, sticky='w')
                i += 1
        

    def show_admin_page(self):
        self.forget_frames()
        self.admin_frame.pack(fill='both')
        self.admin_frame.configure(background=bgrd_color)
        tk.Button(self.admin_frame, text='Show Employee List', bg=btn_bg_color, font=("Times New Roman", 10), command=lambda: self.get_employees(0)).grid(row=0, column=0)
        tk.Button(self.admin_frame, bg=btn_bg_color, text='Create Routes', font=("Times New Roman", 10), command=lambda: self.run_algorithm()).grid(row=0, column=2)
        tk.Button(self.admin_frame, bg=btn_bg_color, text='Search Employee', font=("Times New Roman", 10), command=lambda: self.search_employee()).grid(row=0, column=3)
        tk.Button(self.admin_frame, bg=btn_bg_color, text='Add Employee', font=("Times New Roman", 10), command=lambda: self.add_employee()).grid(row=0, column=4)
        tk.Button(self.admin_frame, bg=btn_bg_color, text='Get Routes', font=("Times New Roman", 10), command=lambda: self.show_route_page()).grid(row=0, column=5)
        tk.Button(self.admin_frame, bg=btn_bg_color, text='Check Running Status', font=("Times New Roman", 10), command=lambda: self.check_algorithm_status()).grid(row=0, column=6)
        tk.Button(self.admin_frame, bg=btn_bg_color, text='Logout', font=("Times New Roman", 10), command=lambda: self.logout()).grid(row=0, column=7)


    def logout(self):
        msg = tkinter.messagebox.askyesno("Logout", "Are you sure to logout?")
        if msg:
            self.show_login_page()

    def click_ok(self):
        if self.user_input.get() == "" or self.pass_input.get() == "":
            tkinter.messagebox.showwarning("Login page", "The User Name or Password is empty.")
            return
        self.data['username'] = self.user_input.get()
        self.data['password'] = self.pass_input.get()
        self.pass_input.delete(0, len(self.data['password']))
        json_str = json.dumps(self.data)
        json_str = str(defineCommands.LOGIN) + ';' + json_str
        result = connection.send_request_to_server(json_str)
        # print(result)
        # for debug it's hardcoded
        # if self.data['username'] == 'root' and self.data['password'] == 'root':
        #     result = True
        # else:
        #     result = False

        if result:
            self.show_admin_page()
        else:
            tkinter.messagebox.showwarning("Login page", "The User Name or Password is incorrect.")

    def click_cancel(self):
        msg = tkinter.messagebox.askyesno("Login page", "Are you sure you want to cancel login?")
        if msg:
            exit()

    def __init__(self, master):
        tk.Frame.__init__(self, master)
        self.pack()
        self.admin_frame = tk.Frame(self)
        self.master.title("GO2WORK")
        self.master.geometry('720x480')
        self.show_login_page()


if __name__ == '__main__':
    root = tk.Tk()
    root.configure(background=bgrd_color)
    app = App(root)
    app.mainloop()
