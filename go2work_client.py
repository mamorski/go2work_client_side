import tkinter as tk
import tkinter.messagebox
import json
import connection
import defineCommands
import validate_address
import openmap
import os
from tkinter import ttk
import configuration 
from functions import *


######################### GUI class of go2work client program###########################
# noinspection PyAttributeOutsideInit
class Go2workClientGUI(tk.Frame):
    ############################## employee operations #############################################
    # main employee page
    # show list of all employees in the db
    # options: set and unset shift, delete employee, add enployee, update info
    def employees_page(self, employee_list):
        forget_frames(self)
        configuration.select_text = True
        self.show_employee_frame = tk.Frame(self)
        self.show_employee_frame.pack(anchor='n', expand=False, side='top', fill='y', pady=130)
        configuration.active_frame.append(self.show_employee_frame)
        self.show_employee_frame.configure(bg=configuration.bgrd_color)
        self.scrollbar_V = tk.Scrollbar(self.show_employee_frame, orient='vertical')
        self.listbox1 = tk.Listbox(self.show_employee_frame, yscrollcommand=self.scrollbar_V.set, height=15, width=40, selectmode='multiple')
        
        if employee_list == 0:
            if configuration.employees_dict:
                received_data = configuration.employees_dict
            else:
                get_data = str(defineCommands.GET_EMPLOYEE_LIST) + ';{}'
                received_data = connection.send_request_to_server(get_data)
                configuration.employees_dict = json.loads(received_data)
                received_data = json.loads(received_data)
        else:
            received_data = employee_list
            received_data = json.loads(received_data)

        for employee in received_data:
            self.listbox1.insert('end', employee['firstname'] + ' ' + employee['lastname'] + ' - Status ' + str(employee['status']))

        count_workers(self)
        self.scrollbar_V.grid(row=0, rowspan=4, column=2, sticky='sn', pady=50)
        self.listbox1.grid(row=0, column=1, rowspan=4, sticky='nesw', pady=50)
        tk.Label(self.show_employee_frame, text='You have {} employees tomorrow'.format(configuration.employees_to_work), bg=configuration.lbl_bg_color, fg=configuration.lbl_color, font=configuration.lbl_font).grid(row=8, column=1, sticky='nesw')
        self.scrollbar_V.config(command=self.listbox1.yview)
        tk.Button(self.show_employee_frame, bg=configuration.btn_bg_color, text='Set Shift', font=configuration.employee_btn_font, 
                  command=lambda: update_shift_or_delete_worker(self, 1, received_data)).grid(row=0, column=0, sticky='w', ipady=10, ipadx=20, pady=20, padx=30)
        tk.Button(self.show_employee_frame, bg=configuration.btn_bg_color, text='Unset Shift', font=configuration.employee_btn_font, 
                  command=lambda: update_shift_or_delete_worker(self, 0, received_data)).grid(row=1, column=0, sticky='w', ipady=10, ipadx=12, pady=20, padx=30)
        tk.Button(self.show_employee_frame, bg=configuration.btn_bg_color, text='Remove', font=configuration.employee_btn_font, 
                  command=lambda: update_shift_or_delete_worker(self, 2, received_data)).grid(row=2, column=0, sticky='w', pady=20, ipady=10, ipadx=22, padx=30)
        tk.Button(self.show_employee_frame, bg=configuration.btn_bg_color, text='Update', font=configuration.employee_btn_font, 
                  command=lambda: self.update_worker(received_data)).grid(row=3, column=0, sticky='w', ipady=10, ipadx=25, pady=20, padx=30)
        tk.Button(self.show_employee_frame, bg=configuration.btn_bg_color, text='Search Employee', font=configuration.employee_btn_font, 
                  command=lambda: self.search_employee()).grid(row=0, column=4, ipady=10, padx=30)
        tk.Button(self.show_employee_frame, bg=configuration.btn_bg_color, text='Add Employee', font=configuration.employee_btn_font, 
                  command=lambda: self.add_employee()).grid(row=1, column=4, ipady=10, ipadx=10, padx=30)
        select_btn = tk.Button(self.show_employee_frame, bg=configuration.btn_bg_color, text='Select All', font=configuration.employee_btn_font, 
                  command=lambda: select_all(self, select_btn))
        select_btn.grid(row=2, column=4, ipady=10, ipadx=30, padx=30)           

    # update worker information
    # throw new additional window with employee data
    def update_worker(self, employees):
        selection = self.listbox1.curselection()
        if len(selection) == 0:
            tkinter.messagebox.showinfo("Update", "No one is selected")
            return
        if len(selection) > 1:
            tkinter.messagebox.showinfo("Update", "You should select only one person")
            return
        window = tk.Toplevel(root)
        window.configure(bg=configuration.bgrd_color)
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
        tk.Label(window, text='Name', bg=configuration.lbl_bg_color, fg=configuration.lbl_color, 
                 font=configuration.lbl_font).grid(row=0, column=0, sticky='w')
        tk.Label(window, text='Last Name', bg=configuration.lbl_bg_color, fg=configuration.lbl_color, 
                 font=configuration.lbl_font).grid( row=1, column=0, sticky='w')
        tk.Label(window, text='Address', bg=configuration.lbl_bg_color, fg=configuration.lbl_color, 
                 font=configuration.lbl_font).grid(row=2, column=0, sticky='w')
        tk.Label(window, text='Id', bg=configuration.lbl_bg_color, fg=configuration.lbl_color, 
                 font=configuration.lbl_font).grid(row=3, column=0, sticky='w')
        tk.Label(window, text='Status', bg=configuration.lbl_bg_color, fg=configuration.lbl_color, 
                 font=configuration.lbl_font).grid(row=4, column=0, sticky='w')
        tk.Button(window, text='Update', bg=configuration.btn_bg_color, font=("Times New Roman", 10), 
                  command=lambda: make_update(self, selection, window)).grid(row=5, column=0, sticky='w', padx=20, pady=20)
        tk.Button(window, text='Cancel', bg=configuration.btn_bg_color, font=("Times New Roman", 10), 
                  command=lambda: window.destroy()).grid(row=5, column=1, sticky='w', pady=20)

    # frame to search employee
    # search options:
    # by name - search if name or last name contains searched field
    # the same for id
    # address - search by full address
    def search_employee(self):
        forget_frames(self)
        self.search_frame = tk.Frame(self)
        self.search_frame.pack(anchor='n', expand=False, side='top', fill='y', pady=150)
        self.search_frame.configure(bg=configuration.bgrd_color)
        configuration.active_frame.append(self.search_frame)
        var = tk.IntVar()
        var.set(0)
        tk.Radiobutton(self.search_frame, bg=configuration.lbl_bg_color, fg=configuration.radio_color, text="By name", 
                       font=configuration.radio_font, variable=var, value=1).grid(row=0, column=0, sticky='w', pady=10)
        tk.Radiobutton(self.search_frame, bg=configuration.lbl_bg_color, fg=configuration.radio_color, text="By id", 
                       font=configuration.radio_font, variable=var, value=2).grid(row=1, column=0, sticky='w', pady=10)
        tk.Radiobutton(self.search_frame, bg=configuration.lbl_bg_color, fg=configuration.radio_color, text="By address", 
                       font=configuration.radio_font, variable=var, value=3).grid(row=2, column=0, sticky='w', pady=10)
        self.search_input = tk.Entry(self.search_frame, background='white', width=24)
        self.search_input.grid(row=1, column=1, sticky='w')
        tk.Button(self.search_frame, bg=configuration.btn_bg_color, text='Search', font=("Times New Roman", 10), 
                  command=lambda: search_send_to_db(self, var)).grid(row=3, column=0, sticky='w', pady=20, ipady=5, ipadx=20)
        tk.Button(self.search_frame, bg=configuration.btn_bg_color, text='Back', font=("Times New Roman", 10), 
                  command=lambda: self.employees_page(0)).grid(row=3, column=1, sticky='w', pady=20, ipady=5, ipadx=20)

    # frame to add new employee to db
    def add_employee(self):
        forget_frames(self)
        self.add_employee_frame = tk.Frame(self)
        self.add_employee_frame.pack(anchor='n', expand=False, side='top', fill='y', pady=150)
        self.add_employee_frame.configure(bg=configuration.bgrd_color)
        configuration.active_frame.append(self.add_employee_frame)
        self.add_name = tk.Entry(self.add_employee_frame, background='white', width=24)
        self.add_name.grid(row=0, column=1, sticky='w', padx=20)
        self.add_last_name = tk.Entry(self.add_employee_frame, background='white', width=24)
        self.add_last_name.grid(row=1, column=1, sticky='w', padx=20)
        self.add_address = tk.Entry(self.add_employee_frame, background='white', width=24)
        self.add_address.grid(row=2, column=1, sticky='w', padx=20)
        self.add_id = tk.Entry(self.add_employee_frame, background='white', width=24)
        self.add_id.grid(row=3, column=1, sticky='w', padx=20)
        tk.Label(self.add_employee_frame, bg=configuration.lbl_bg_color, fg=configuration.lbl_color, text='Name', 
                 font=configuration.lbl_font).grid(row=0, column=0, sticky='w')
        tk.Label(self.add_employee_frame, bg=configuration.lbl_bg_color, fg=configuration.lbl_color, text='Last Name', 
                 font=configuration.lbl_font).grid(row=1, column=0, sticky='w')
        tk.Label(self.add_employee_frame, bg=configuration.lbl_bg_color, fg=configuration.lbl_color, text='Address', 
                 font=configuration.lbl_font).grid(row=2, column=0, sticky='w')
        tk.Label(self.add_employee_frame, bg=configuration.lbl_bg_color, fg=configuration.lbl_color, text='Id', 
                 font=configuration.lbl_font).grid(row=3, column=0, sticky='w')
        tk.Button(self.add_employee_frame, bg=configuration.btn_bg_color, text='Add', font=("Times New Roman", 10), 
                  command=lambda: add_send_to_db(self)).grid(row=5, column=0, sticky='w', pady=20, ipady=5, ipadx=20)
        tk.Button(self.add_employee_frame, bg=configuration.btn_bg_color, text='Back', font=("Times New Roman", 10), 
                  command=lambda: self.employees_page(0)).grid(row=5, column=1, sticky='w', pady=20, ipady=5, ipadx=20)
    ############################## end of employee operations #############################################
    
    
    ############################## algorithm operations #############################################
    # page with algorithm configurations and option to run the algorithm
    # option to enter max vehicle capacity - default is 6
    # option to enter number of free vehicles - default is 4
    def algorithm_page(self):
        forget_frames(self)
        self.run_algo_frame = tk.Frame(self)
        self.run_algo_frame.pack(anchor='n', expand=False, side='top', fill='y', pady=150)
        self.run_algo_frame.configure(bg=configuration.bgrd_color)
        configuration.active_frame.append(self.run_algo_frame)
        var = tk.IntVar()
        var.set(1)
        tk.Label(self.run_algo_frame, text='Number of vehicles:', bg=configuration.lbl_bg_color, fg=configuration.lbl_color, 
                 font=configuration.lbl_font).grid(row=0, column=0, sticky='w', pady=10, padx=50)
        tk.Label(self.run_algo_frame, text='Max vehicle capacity:', bg=configuration.lbl_bg_color, fg=configuration.lbl_color, 
                 font=configuration.lbl_font).grid(row=1, column=0, sticky='w', pady=10, padx=50)
        self.vehicle_capacity = tk.Entry(self.run_algo_frame, background='white', width=5)
        self.vehicle_capacity.insert('end', 6)
        self.vehicle_capacity.grid(row=1, column=1, sticky='w', pady=10)
        self.num_of_vehicles = tk.Entry(self.run_algo_frame, background='white', width=5)
        self.num_of_vehicles.insert('end', 4)
        self.num_of_vehicles.grid(row=0, column=1, sticky='w', pady=10)
        tk.Label(self.run_algo_frame, text='Speed of creation:', bg=configuration.lbl_bg_color, fg=configuration.lbl_color, 
                 font=configuration.lbl_font).grid(row=2, column=0, sticky='w', pady=30, padx=50)
        tk.Radiobutton(self.run_algo_frame, bg=configuration.lbl_bg_color, text="fast", fg=configuration.radio_color, 
                       font=configuration.radio_font, variable=var, value=0).grid(row=2, column=1, sticky='w')
        tk.Radiobutton(self.run_algo_frame, bg=configuration.lbl_bg_color, text="medium", fg=configuration.radio_color, 
                       font=configuration.radio_font, variable=var, value=1).grid(row=2, column=2, sticky='w')
        tk.Radiobutton(self.run_algo_frame, bg=configuration.lbl_bg_color, text="slow", fg=configuration.radio_color, 
                       font=configuration.radio_font, variable=var, value=2).grid(row=2, column=3, sticky='w')
        tk.Button(self.run_algo_frame, bg=configuration.btn_bg_color, text='   Create   ', font=configuration.employee_btn_font, 
                  default='active', command=lambda: run(self, var)).grid(row=3, column=1)

    # check algorithm running status
    # show message if the algorithm is running
    # if running show button to stop it
    def check_algorithm_status(self):
        forget_frames(self)
        self.check_frame = tk.Frame(self)
        self.check_frame.pack(anchor='n', expand=False, side='top', fill='y', pady=150)
        self.check_frame.configure(bg=configuration.bgrd_color)
        configuration.active_frame.append(self.check_frame)
        request = str(defineCommands.CHECK_ALGORITHM_STATUS) + ';{}'
        result = connection.send_request_to_server(request)
        
        if result:
            tkinter.messagebox.showinfo("Check route status", "Creating in process.")
        else:
            tkinter.messagebox.showinfo("Check route status", "No process found")
        
        if result:
            self.kill_lbl = tk.Label(self.check_frame, text='You have running process', bg=configuration.lbl_bg_color, 
                                     fg=configuration.lbl_color, font=configuration.lbl_font)
            self.kill_lbl.pack()
            self.kill_btn = tk.Button(self.check_frame, text='Stop Process of Creating Routes', default='active', font=configuration.main_btn_font, 
                                      bg=configuration.btn_bg_color, command=lambda: kill_process(self))
            self.kill_btn.pack()

    # show all available routes from last running
    # frame that show all available routes with buttons that opens the route on Google Maps
    def show_route_page(self):
        forget_frames(self)
        self.route_frame = tk.Frame(self)
        self.route_frame.pack(anchor='n', expand=False, side='top', fill='y', pady=20)
        self.route_frame.configure(bg=configuration.bgrd_color)
        configuration.active_frame.append(self.route_frame)
        route_data = str(defineCommands.GET_ROUTES) + ";{}"
        received_data = connection.send_request_to_server(route_data)
        received_data = json.loads(received_data)
        index = 0
        routes = []
        for index, vehicle in enumerate(received_data):
            i = 1
            tk.Button(self.route_frame, bg=configuration.btn_bg_color, text='Route {}'.format(index+1), font=("Times New Roman", 10), 
                      command=lambda j=index:openmap.openmap(routes, j)).grid(row=0, column=index, sticky='w', pady=15)
            for employee in received_data[vehicle]:
                routes.append([])
                routes[index].append(received_data[vehicle][employee]["address"])
                my_str = received_data[vehicle][employee]['firstname'] + ' ' + received_data[vehicle][employee]['lastname']
                tk.Label(self.route_frame, text=my_str, bg=configuration.lbl_bg_color, fg=configuration.lbl_color, 
                         font=("Times New Roman", 14)).grid(row=i, column=index, sticky='w')
                i += 1
    ############################## end of algorithm operations #############################################
    
    
    ############################## login, help and buttons panel #################################################
    # login page
    # start login frame with user name and password
    # connect to db to check the data and get list of employees
    def show_login_page(self):
        forget_frames(self)
        self.admin_frame.pack_forget()
        self.dialog_frame = tk.Frame(self)
        self.dialog_frame.configure(bg=configuration.bgrd_color)
        self.user_input = tk.Entry(self.dialog_frame, background='white', width=24)
        self.pass_input = tk.Entry(self.dialog_frame, background='white', width=24, show='*')
        self.user_input.insert('end', 'root')
        self.pass_input.insert('end', 'root')
        self.dialog_frame.pack(anchor='center', pady=100)
        configuration.active_frame.append(self.dialog_frame)
        tk.Label(self.dialog_frame, text="Login to GO2WORK system", bg=configuration.lbl_bg_color, fg=configuration.lbl_color, 
                 font=("Times New Roman", 22)).grid(row=0, columnspan=3, sticky='n', pady=80)
        tk.Label(self.dialog_frame, text='Username:', bg=configuration.lbl_bg_color, fg=configuration.lbl_color, 
                 font=configuration.lbl_font).grid(row=1, column=0, sticky='w')
        self.user_input = tk.Entry(self.dialog_frame, background='white', width=24)
        self.user_input.grid(row=1, column=1, sticky='w', padx=20)
        self.user_input.focus_set()
        tk.Label(self.dialog_frame, text='Password:', bg=configuration.lbl_bg_color, fg=configuration.lbl_color, 
                 font=configuration.lbl_font).grid(row=2, column=0, sticky='w')
        self.pass_input.grid(row=2, column=1, sticky='w', padx=20)
        tk.Button(self.dialog_frame, text='   Ok    ', default='active', bg=configuration.btn_bg_color, 
                  command=lambda: click_ok(self)).grid(row=1, column=2, sticky='w', ipadx=30)
        tk.Button(self.dialog_frame, text='Cancel', default='active', bg=configuration.btn_bg_color, 
                  command=lambda: click_cancel(self)).grid(row=2, column=2, sticky='w', ipadx=30)
        if configuration.debug:
            tk.Label(self.dialog_frame, text='ip:', bg=configuration.lbl_bg_color, fg=configuration.lbl_color, 
                     font=configuration.lbl_font).grid(row=3, column=0, sticky='w')
            self.ip = tk.Entry(self.dialog_frame, background='white', width=24)
            self.ip.grid(row=3, column=1, sticky='w', padx=20)

    def open_help(self):
        window = tk.Toplevel(root)
        window.configure(bg=configuration.bgrd_color)
        var = tk.StringVar()
        help_msg = tk.Message(window, textvariable=var, relief='raised')
        my_str = '      GO2WORK Help System     \n'
        my_str += 'To see employee list and employee options click on Employee Page\n'
        my_str += 'On the employee page you can see the list of all employees in the\nsystem '
        my_str += 'and you can perfome:\n       -Set\\Unset shift for selected employees\n'
        my_str += '       -Remove selected employees\n       -Update info of one selected employee\n'
        my_str += '       -Search employee in the system\n       -Add new employee to the system\n'
        my_str += 'To create routes for employees with status 1 click on Create Routes\n'
        my_str += 'On the create routes page you can:\n'
        my_str += '       -Enter the number of vehicles (Default is 4)\n'
        my_str += '       -Enter the maximum capacity of the vehicle (Default is 6)\n'
        my_str += '       -Choose the speed of routes creation\n'
        # my_str +=

    # panel of main buttons (always appear)
    # create and put main navigation buttons on the top of the page
    def main_buttons_panel(self):
        forget_frames(self)
        self.admin_frame.pack(anchor='n', expand=False, side='top', fill='y', padx=200)
        self.admin_frame.configure(bg=configuration.bgrd_color)
        tk.Button(self.admin_frame, bg=configuration.btn_bg_color, text='Employee Page', font=configuration.main_btn_font, 
                  command=lambda: self.employees_page(0)).grid(row=0, column=0, sticky='nwse')
        tk.Button(self.admin_frame, bg=configuration.btn_bg_color, text='Create Routes', font=configuration.main_btn_font, 
                  command=lambda: self.algorithm_page()).grid(row=0, column=1, sticky='nwse')
        tk.Button(self.admin_frame, bg=configuration.btn_bg_color, text='Get Routes', font=configuration.main_btn_font, 
                  command=lambda: self.show_route_page()).grid(row=0, column=2, sticky='nwse')
        tk.Button(self.admin_frame, bg=configuration.btn_bg_color, text='Check Running \nStatus', font=configuration.main_btn_font, 
                  command=lambda: self.check_algorithm_status()).grid(row=0, column=3, sticky='nwse')
        tk.Button(self.admin_frame, bg=configuration.btn_bg_color, text='      Help      ', font=configuration.main_btn_font, 
                  command=lambda: self.open_help()).grid(row=0, column=4, sticky='nwse')
        tk.Button(self.admin_frame, bg=configuration.btn_bg_color, text='      Logout      ', font=configuration.main_btn_font, 
                  command=lambda: logout(self)).grid(row=0, column=5, sticky='nwse')
    ############################## end of login and buttons panel #############################################

    
    ############################## init class ##############################################
    # constructor of GUI class
    def __init__(self, master):
        tk.Frame.__init__(self, master)
        self.pack(anchor='w', expand=True, fill='both')
        self.configure(bg=configuration.bgrd_color)
        self.admin_frame = tk.Frame(self, bg=configuration.bgrd_color)
        self.master.configure(bg=configuration.bgrd_color)
        self.master.title("GO2WORK")
        self.master.geometry('960x720')
        self.show_login_page()
    ############################## end of init class ########################################


############################## main #############################################
# create main tk window and start infinite loop
if __name__ == '__main__':
    root = tk.Tk()
    root.configure(background=configuration.bgrd_color)
    app = Go2workClientGUI(root)
    app.mainloop()
