import tkinter as tk
import tkinter.messagebox
import json
import connection
import defineCommands
import validate_address
import openmap


# employees = ['Igor Mamorski', 'Elad Hezi', 'Alex Melnic', 'Benny Mounits', 'Bibi Netaniahu', 'Oren Hazan', 'Jim Carrey',
#              'Guy Cohen', 'Gidi Cohen', 'Gidi Bucks', 'Pamela Anderson', 'Chuck Norris', 'Bill Gates', 'Omer Adam',
#              'Bred Pit',
#              'Johny Depp', 'Orlando Bloom', 'Penelope Cruz']


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
            json_str = json.dumps(shift_data)
            json_str = str(defineCommands.REMOVE_EMPLOYEE) + ';' + json_str
            result = connection.send_request_to_server(json_str)
        if result:
            tkinter.messagebox.showinfo("Update", message + sub_message[set_shift])
        else:
            tkinter.messagebox.showinfo("Update", "We got some error...\nApparently aliens stole your data")
        self.get_employees(0)

    def run_algorithm(self):
        self.forget_frames()
        alg_data = str(defineCommands.RUN_ALGORITHM) + ';{}'
        result = connection.send_request_to_server(alg_data)
        if result:
            tkinter.messagebox.showinfo("Create Routes", "Creating in process.")
        else:
            tkinter.messagebox.showinfo("Create Routes", "Creating fail.")

    def get_employees(self, employee_list):
        self.forget_frames()
        self.show_employee_frame = tk.Frame(self)
        self.show_employee_frame.pack(fill = 'both')
        self.active_frame.append(self.show_employee_frame)
        self.show_employee_frame.configure(background = 'NavajoWhite3', pady=50)
        self.scrollbar_V = tk.Scrollbar(self.show_employee_frame)
        self.listbox1 = tk.Listbox(self.show_employee_frame, yscrollcommand = self.scrollbar_V.set, height = 15,
                                   width = 40, selectmode = 'multiple')
        if employee_list == 0:
            get_data = str(defineCommands.GET_EMPLOYEE_LIST) + ';{}'
            result = connection.send_request_to_server(get_data)
            received_data = result.decode("utf-8")
        else:
            received_data = employee_list
        if received_data != '':
            received_data = json.loads(received_data)
        for employee in received_data:
            self.listbox1.insert('end', employee['firstname'] + ' ' + employee['lastname'] + ' - Status ' + str(
                employee['status']))
        self.listbox1.grid(rowspan = 5, row = 0, column = 1, sticky = 'w', pady = 50)
        self.scrollbar_V.grid(row = 0, rowspan = 5, column = 2, sticky = 'w')
        self.scrollbar_V.config(command = self.listbox1.yview)
        tk.Button(self.show_employee_frame, bg = 'light blue', text = 'Set Shift', default = 'active',
                  command = lambda: self.update_shift_or_delete_worker(1, received_data)).grid(row = 0, column = 0,
                                                                                               sticky = 'w',
                                                                                               ipady = 10,
                                                                                               ipadx = 20, pady = 20, padx=50)
        tk.Button(self.show_employee_frame, bg = 'light blue', text = 'Unset Shift', default = 'active',
                  command = lambda: self.update_shift_or_delete_worker(0, received_data)).grid(row = 1,
                                                                                               column = 0, sticky = 'w',
                                                                                               ipady = 10,
                                                                                               ipadx = 12, pady=20, padx=50)
        tk.Button(self.show_employee_frame, bg = 'light blue', text = 'Remove', default = 'active',
                  command = lambda: self.update_shift_or_delete_worker(2, received_data)).grid(row = 2,
                                                                                               column = 0, sticky = 'w',
                                                                                               pady = 20,
                                                                                               ipady = 10,
                                                                                               ipadx = 20, padx=50)
        tk.Button(self.show_employee_frame, bg = 'light blue', text = 'Update', default = 'active',
                  command = lambda: self.update_worker(received_data)).grid(row = 3, column = 0, sticky = 'w',
                                                                            ipady = 10,
                                                                            ipadx = 20, pady=20, padx=50)

    def update_worker(self, employees):
        selection = self.listbox1.curselection()
        if len(selection) == 0:
            tkinter.messagebox.showinfo("Update", "No one is selected")
            return
        if len(selection) > 1:
            tkinter.messagebox.showinfo("Update", "You should select only one person")
            return
        window = tk.Toplevel(root)
        window.configure(background = 'NavajoWhite3')
        self.add_name = tk.Entry(window, background = 'white', width = 24)
        self.add_name.insert('end', employees[selection[0]]['firstname'])
        self.add_name.grid(row = 0, column = 1, sticky = 'w', padx = 20)
        self.add_last_name = tk.Entry(window, background = 'white', width = 24)
        self.add_last_name.grid(row = 1, column = 1, sticky = 'w', padx = 20)
        self.add_last_name.insert('end', employees[selection[0]]['lastname'])
        self.add_address = tk.Entry(window, background = 'white', width = 24)
        self.add_address.grid(row = 2, column = 1, sticky = 'w', padx = 20)
        self.add_address.insert('end', employees[selection[0]]['address'])
        self.add_id = tk.Entry(window, background = 'white', width = 24)
        self.add_id.grid(row = 3, column = 1, sticky = 'w', padx = 20)
        self.add_id.insert('end', employees[selection[0]]['empID'])
        self.add_status = tk.Entry(window, background = 'white', width = 24)
        self.add_status.grid(row = 4, column = 1, sticky = 'w', padx = 20)
        self.add_status.insert('end', employees[selection[0]]['status'])
        tk.Label(window, text = 'Name', bg = 'NavajoWhite3', fg = 'snow', font = ("Times New Roman", 16)).grid(row = 0,
                                                                                                               column = 0,
                                                                                                               sticky = 'w')
        tk.Label(window, text = 'Last Name', bg = 'NavajoWhite3', fg = 'snow', font = ("Times New Roman", 16)).grid(
            row = 1, column = 0, sticky = 'w')
        tk.Label(window, text = 'Address', bg = 'NavajoWhite3', fg = 'snow', font = ("Times New Roman", 16)).grid(
            row = 2, column = 0, sticky = 'w')
        tk.Label(window, text = 'Id', bg = 'NavajoWhite3', fg = 'snow', font = ("Times New Roman", 16)).grid(row = 3,
                                                                                                             column = 0,
                                                                                                             sticky = 'w')
        tk.Label(window, text = 'Status', bg = 'NavajoWhite3', fg = 'snow', font = ("Times New Roman", 16)).grid(
            row = 4, column = 0, sticky = 'w')
        tk.Button(window, text = 'Update', bg = 'light blue', font = ("Times New Roman", 10),
                  command = lambda: make_update()).grid(row = 5,
                                                        column = 0,
                                                        sticky = 'w',
                                                        padx = 20,
                                                        pady = 20)
        tk.Button(window, text = 'Cancel', bg = 'light blue', font = ("Times New Roman", 10),
                  command = lambda: window.destroy()).grid(row = 5,
                                                           column = 1,
                                                           sticky = 'w',
                                                           pady = 20)

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
            add_data = {
                'firstname': self.add_name.get(),
                'lastname':  self.add_last_name.get(),
                'address':   self.add_address.get(),
                'empID':     self.add_id.get(),
                'status':    self.add_status.get()
            }
            json_str = json.dumps(add_data)
            json_str = str(defineCommands.UPDATE) + ';' + json_str
            result = connection.send_request_to_server(json_str)
            if result:
                tkinter.messagebox.showinfo("Update", "Success")
                window.destroy()
            else:
                tkinter.messagebox.showinfo("Update", "Error")

    def search_employee(self):
        self.forget_frames()
        self.search_frame = tk.Frame(self)
        self.search_frame.configure(background = 'NavajoWhite3', pady=70, padx=130)
        self.search_frame.pack(fill='both')
        self.active_frame.append(self.search_frame)
        var = tk.IntVar()
        var.set(0)
        tk.Radiobutton(self.search_frame, bg='NavajoWhite3', text = "By name", font = ("Times New Roman", 14), variable = var, value = 1).grid(row = 0, column = 0,
                                                                                            sticky = 'w',
                                                                                            pady = 10)
        tk.Radiobutton(self.search_frame, bg='NavajoWhite3',text = "By id", font = ("Times New Roman", 14), variable = var, value = 2).grid(row = 1, column = 0,
                                                                                          sticky = 'w',
                                                                                          pady = 10)
        tk.Radiobutton(self.search_frame, bg='NavajoWhite3', text = "By address", font = ("Times New Roman", 14), variable = var, value = 3).grid(row = 2, column = 0,
                                                                                               sticky = 'w',
                                                                                               pady = 10)
        self.search_input = tk.Entry(self.search_frame, background = 'white', width = 24)
        self.search_input.grid(row = 1, column = 1, sticky = 'w')
        tk.Button(self.search_frame, bg = 'light blue', text = 'Search', font = ("Times New Roman", 10),
                  command = lambda: send_to_db()).grid(row = 3,
                                                       column = 1,
                                                       sticky = 'w',
                                                       pady = 20)

        def send_to_db():
            if self.search_input.get() == "":
                tkinter.messagebox.showinfo("Search", "Search field is empty")
                return
            if var == 0:
                tkinter.messagebox.showinfo("Search", "Please, check one parameter")
                return
            search_types = ['firstname', 'empID', 'address']
            search_data = {
                'searchby':                  search_types[var.get() - 1],
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
        self.add_employee_frame.configure(background = 'NavajoWhite3')
        self.add_employee_frame.pack(padx = 50, pady = 100, anchor = 'n')
        self.active_frame.append(self.add_employee_frame)
        self.add_name = tk.Entry(self.add_employee_frame, background = 'white', width = 24)
        self.add_name.grid(row = 0, column = 1, sticky = 'w', padx = 20)
        self.add_last_name = tk.Entry(self.add_employee_frame, background = 'white', width = 24)
        self.add_last_name.grid(row = 1, column = 1, sticky = 'w', padx = 20)
        self.add_address = tk.Entry(self.add_employee_frame, background = 'white', width = 24)
        self.add_address.grid(row = 2, column = 1, sticky = 'w', padx = 20)
        self.add_id = tk.Entry(self.add_employee_frame, background = 'white', width = 24)
        self.add_id.grid(row = 3, column = 1, sticky = 'w', padx = 20)
        tk.Label(self.add_employee_frame, bg = 'NavajoWhite3', fg = 'snow', text = 'Name',
                 font = ("Times New Roman", 16)).grid(row = 0, column = 0,
                                                      sticky = 'w')
        tk.Label(self.add_employee_frame, bg = 'NavajoWhite3', fg = 'snow', text = 'Last Name',
                 font = ("Times New Roman", 16)).grid(row = 1, column = 0,
                                                      sticky = 'w')
        tk.Label(self.add_employee_frame, bg = 'NavajoWhite3', fg = 'snow', text = 'Address',
                 font = ("Times New Roman", 16)).grid(row = 2, column = 0,
                                                      sticky = 'w')
        tk.Label(self.add_employee_frame, bg = 'NavajoWhite3', fg = 'snow', text = 'Id',
                 font = ("Times New Roman", 16)).grid(row = 3, column = 0,
                                                      sticky = 'w')
        tk.Button(self.add_employee_frame, bg = 'light blue', text = 'Add', font = ("Times New Roman", 10),
                  command = lambda: send_to_db()).grid(row = 5, column = 1, sticky = 'w')

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
            add_data = {
                'firstname': self.add_name.get(),
                'lastname':  self.add_last_name.get(),
                'address':   self.add_address.get(),
                'empID':     self.add_id.get(),
                'status':    0
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
        self.dialog_frame.configure(background = 'NavajoWhite3')
        self.user_input = tk.Entry(self.dialog_frame, background = 'white', width = 24)
        self.pass_input = tk.Entry(self.dialog_frame, background = 'white', width = 24, show = '*')
        self.dialog_frame.pack()
        self.active_frame.append(self.dialog_frame)
        tk.Label(self.dialog_frame, text = "Login to GO2WORK system", bg = 'NavajoWhite3', fg = 'snow',
                 font = ("Times New Roman", 22)).grid(row = 0,
                                                      columnspan = 3,
                                                      sticky = 'n',
                                                      pady = 60)
        tk.Label(self.dialog_frame, text = 'Username:', bg = 'NavajoWhite3', fg = 'snow',
                 font = ("Times New Roman", 16)).grid(row = 1, column = 0,
                                                      sticky = 'w',
                                                      padx = 20)
        self.user_input = tk.Entry(self.dialog_frame, background = 'white', width = 24)
        self.user_input.grid(row = 1, column = 1, sticky = 'w', padx = 20)
        self.user_input.focus_set()
        tk.Label(self.dialog_frame, text = 'Password:', bg = 'NavajoWhite3', fg = 'snow',
                 font = ("Times New Roman", 16)).grid(row = 2, column = 0,
                                                      sticky = 'w',
                                                      padx = 20)
        self.pass_input.grid(row = 2, column = 1, sticky = 'w', padx = 20)
        tk.Button(self.dialog_frame, text = 'OK', default = 'active', bg = 'light blue',
                  command = lambda: self.click_ok()).grid(row = 3,
                                                          column = 0,
                                                          sticky = 'w',
                                                          padx = 20,
                                                          pady = 50,
                                                          ipady = 10,
                                                          ipadx = 20)
        tk.Button(self.dialog_frame, text = 'Cancel', default = 'active', bg = 'light blue',
                  command = lambda: self.click_cancel()).grid(
            row = 3, column = 1, sticky = 'w', padx = 100, pady = 50, ipady = 10, ipadx = 10)

    def show_route_page(self):
        self.forget_frames()
        self.route_frame = tk.Frame(self)
        self.route_frame.pack(fill = 'both')
        self.route_frame.configure(background = 'NavajoWhite3', pady=50)
        self.active_frame.append(self.route_frame)
        route_data = str(defineCommands.GET_ROUTES) + ';{}'
        # json_str = json.dumps(route_data)
        # json_str = str(defineCommands.ADD_EMPLOYEE) + json_str
        result = connection.send_request_to_server(route_data)
        received_data = result.decode("utf-8")
        received_data = json.loads(received_data)
        index = 0
        routes = []
        print(received_data)
        # for vehicle in received_data:
        #     tk.Button(self.route_frame, bg = 'light blue', text='Route {}'.format(index), font = ("Times New Roman", 10),
        #               command=lambda :openmap.openmap(routes[index])).grid(row)
        #     index += 1
        #     for employee in vehicle:

    def show_admin_page(self):
        self.forget_frames()
        self.admin_frame.pack()
        tk.Button(self.admin_frame, text = 'Show Employee List', bg = 'light blue', font = ("Times New Roman", 10),
                  command = lambda: self.get_employees(0)).grid(row = 0, column = 0)
        tk.Button(self.admin_frame, bg = 'light blue', text = 'Create Routes', font = ("Times New Roman", 10),
                  command = lambda: self.run_algorithm()).grid(row = 0, column = 2)
        tk.Button(self.admin_frame, bg = 'light blue', text = 'Search Employee', font = ("Times New Roman", 10),
                  command = lambda: self.search_employee()).grid(row = 0, column = 3)
        tk.Button(self.admin_frame, bg = 'light blue', text = 'Add Employee', font = ("Times New Roman", 10),
                  command = lambda: self.add_employee()).grid(row = 0, column = 4)
        tk.Button(self.admin_frame, bg = 'light blue', text = 'Logout', font = ("Times New Roman", 10),
                  command = lambda: self.logout()).grid(row = 0, column = 6)
        tk.Button(self.admin_frame, bg = 'light blue', text = 'Get Routes', font = ("Times New Roman", 10),
                  command = lambda: self.show_route_page()).grid(row = 0, column = 5)

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
        self.admin_frame.configure(background = 'NavajoWhite3')
        self.master.title("GO2WORK")
        self.master.geometry('720x480')
        self.show_login_page()


if __name__ == '__main__':
    root = tk.Tk()
    root.configure(background = 'NavajoWhite3')
    app = App(root)
    app.mainloop()
