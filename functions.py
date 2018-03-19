import configuration
import tkinter as tk
import tkinter.messagebox
import defineCommands
import json
import connection
import validate_address

############################
# additional functions file#
############################

# set frame uvisible
# set frame unvisible
def forget_frames(self):
    for frame in configuration.active_frame:
        frame.pack_forget()
    configuration.active_frame.clear()

# select/unselect all employees on main employee page
def select_all(self, select_btn):
    if configuration.select_text:
        self.listbox1.select_set(0, configuration.num_of_employees)
        configuration.select_text = False
    else:
        self.listbox1.selection_clear(0, configuration.num_of_employees)
        configuration.select_text = True   

# update shift and delete workers from db operations
def update_shift_or_delete_worker(self, set_shift, employees):
    selection = self.listbox1.curselection()
    if len(selection) == 0:
        tkinter.messagebox.showinfo("Update", "No one is selected")
        return
    message = ""
    sub_message = ['unselected for tomorrow', 'selected for tomorrow', 'deleted']
    shift_data = []
    
    for index, each in enumerate(selection):
        message = message + employees[each]['firstname'] + ' ' + employees[each]['lastname'] + "\n"
        shift_data.append({})
        shift_data[index]['empID'] = employees[each]['empID']
        shift_data[index]['status'] = set_shift
    
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
        for i in selection:
            if set_shift == 2:
                configuration.employees_dict.pop(i)
            else:
                configuration.employees_dict[i]['status'] = set_shift

    else:
        tkinter.messagebox.showinfo("Update", "We got some error...\nApparently aliens stole your data")
    self.employees_page(0)

# update employee data
# function perfoms check if all entries have been field and that address is valid by sending request to Google API
def make_update(self, selection, window):
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
        configuration.employees_dict[selection[0]] = add_data
        self.employees_page(0)
        window.destroy()
    else:
        tkinter.messagebox.showinfo("Update", "Error")

# send search request to server and get the answer from server
def search_send_to_db(self, var):
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
        self.employees_page(result)
    else:
        tkinter.messagebox.showinfo("Search", "Not Found")

# send data of new employee to server
# the function performs check of the data
# sets default working status to 0
# performs checking if the address is valid by sending request to Google API
def add_send_to_db(self):
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
        get_data = str(defineCommands.GET_EMPLOYEE_LIST) + ';{}'
        configuration.employees_dict = connection.send_request_to_server(get_data)
        if not configuration.employees_dict:
            tkinter.messagebox.showinfo("Add Employee", 'Error when updating employee list.\nLogged out.')
            self.logout()
        configuration.employees_dict = json.loads(configuration.employees_dict)

    if result:
        tkinter.messagebox.showinfo("Add Employee", "Employee {} {} successfully added.".format(add_data['firstname'], add_data['lastname']))
    else:
        tkinter.messagebox.showinfo("Add Employee", "Failed to add employee, try later or contact your help desc")

# count how many workers are in the system with working status 1
def count_workers(self):
    configuration.employees_to_work = 0
    configuration.num_of_employees = len(configuration.employees_dict)
    for worker in configuration.employees_dict:
        if worker['status'] == 1:
            configuration.employees_to_work += 1

# logout from the system and show login page
def logout(self):
    msg = tkinter.messagebox.askyesno("Logout", "Are you sure to logout?")
    if msg:
        self.show_login_page()

# ok on login page - send request to db and check password and user name
def click_ok(self):
    
    if self.user_input.get() == "" or self.pass_input.get() == "":
        tkinter.messagebox.showwarning("Login page", "The User Name or Password is empty.")
        return
    configuration.data['username'] = self.user_input.get()
    configuration.data['password'] = self.pass_input.get()
    self.pass_input.delete(0, len(configuration.data['password']))
   
    if configuration.debug:
        if self.ip.get() != '':
            connection.ip = self.ip.get()
    json_str = json.dumps(configuration.data)
    json_str = str(defineCommands.LOGIN) + ';' + json_str
    result = connection.send_request_to_server(json_str)

    if result:
        get_data = str(defineCommands.GET_EMPLOYEE_LIST) + ';{}'
        received_data = connection.send_request_to_server(get_data)
        configuration.employees_dict = json.loads(received_data)
        count_workers(self)
        self.main_buttons_panel()
    else:
        tkinter.messagebox.showwarning("Login page", "The User Name or Password is incorrect.")

# cancel login and exit the program
def click_cancel(self):
    msg = tkinter.messagebox.askyesno("Login page", "Are you sure you want to cancel login?")
    if msg:
        exit()

# send request to server to kill the running algorithm
def kill_process(self):
    kill_msg = tk.messagebox.askokcancel("Stop", "Are you sure to stop running?")
    if not kill_msg:
        return
    kill_data = str(defineCommands.KILL_PROCESS) + ';{}'
    result = connection.send_request_to_server(kill_data)
    if result:
        tkinter.messagebox.showinfo("Check route status", "Stoped")
        self.kill_lbl.forget()
        self.kill_btn.forget()

# send request to server to run algorithm that creates the routes
def run(self, var):
    quality = ['low', 'medium', 'high']
    
    if self.num_of_vehicles.get() == "" or self.vehicle_capacity.get() == "":
        tkinter.messagebox.showinfo("Create Routes", "Please, enter number of vehicles and vehicle capacity.")
        return
    
    if not self.num_of_vehicles.get().isdigit() or not self.vehicle_capacity.get().isdigit():
        tkinter.messagebox.showinfo("Create Routes", "Please, enter only digits.")
        return
    
    if configuration.employees_to_work == 0:
        tkinter.messagebox.showinfo("Create Routes", "You need to choose at least one employee")
        return 
        
    if  (configuration.employees_to_work / int(self.num_of_vehicles.get())) > int(self.vehicle_capacity.get()):
        tkinter.messagebox.showinfo("Create Routes", "You need more vehicles!")
        return
    
    alg_data = {
        'numofvehicles': int(self.num_of_vehicles.get()),
        'routequality' : quality[var.get()],
        'vehiclecapacity': int(self.vehicle_capacity.get())
    }
    json_str = json.dumps(alg_data)
    json_str = str(defineCommands.RUN_ALGORITHM) + ';' + json_str
    result = connection.send_request_to_server(json_str)
    
    if result:
        tkinter.messagebox.showinfo("Create Routes", "Creating in process.")
    else:
        tkinter.messagebox.showinfo("Create Routes", "Creating fail.")
            
