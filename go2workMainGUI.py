import tkinter as tk
import tkinter.messagebox
import connection
import json

LARGE_FONT = ("Verdana", 12)
SMALL_FONT = ("Verdana", 10)


class SeaofBTCapp(tk.Tk):

    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)
        container = tk.Frame(self)
        container.pack(side = "top", fill = "both", expand = True)
        container.grid_rowconfigure(0, weight = 1)
        container.grid_columnconfigure(0, weight = 1)
        self.frames = {}

        for F in (LoginPage, AdminMainPage, PageTwo):
            frame = F(container, self)
            self.frames[F] = frame
            frame.grid(row = 0, column = 0, sticky = tk.N + tk.E + tk.W + tk.S)

        self.show_frame(LoginPage)

    def show_frame(self, cont):
        frame = self.frames[cont]
        frame.tkraise()


class LoginPage(tk.Frame):

    def login(self):
        name = self.txtUserName.get()
        password = self.txtPassword.get()

        data = {
            'username': name,
            'password': password,
        }
        json_str = json.dumps(data)
        json_str = '1;' + json_str
        result = connection.send_request_to_server(json_str)
        print(result)

        if result:
            tkinter.messagebox.showinfo("Login page", "Hello, " + name)
            self.my_controller.show_frame(AdminMainPage)
        else:
            tkinter.messagebox.showwarning("Login page", "Wrong details!")

    def cancel_login(self):
        msg = tkinter.messagebox.askyesno("Login page", "Are you sure you want to cancel login?")
        if msg:
            exit()

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.my_controller = controller
        self.label = tk.Label(self, text = "GO2WORK", font = LARGE_FONT)
        self.label.pack(pady = 10, padx = 10)

        self.lblUserName = tk.Label(self, text = "User Name", font = LARGE_FONT)
        self.lblUserName.place(relx = 0.08, rely = 0.21, height = 60, width = 100)

        self.txtUserName = tk.Entry(self)
        self.txtUserName.place(relx = 0.35, rely = 0.23, height = 30, width = 300)

        self.lblPassword = tk.Label(self, text = "Password", font = LARGE_FONT)
        self.lblPassword.place(relx = 0.073, rely = 0.41, height = 60, width = 100)

        self.txtPassword = tk.Entry(self, show = '*')
        self.txtPassword.place(relx = 0.35, rely = 0.43, height = 30, width = 300)

        self.btnLogin = tk.Button(self, text = "Login", command = lambda: self.login())
        self.btnLogin.place(relx = 0.25, rely = 0.7, height = 60, width = 100)

        self.btnCancel = tk.Button(self, text = "Cancel", command = lambda: self.cancel_login())
        self.btnCancel.place(relx = 0.7, rely = 0.7, height = 60, width = 100)


class AdminMainPage(tk.Frame):

    def run_algorithm(self):
        data = '5;{}'
        connection.send_request_to_server(data)

    def get_employee_list(self):
        pass

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.my_controller = controller
        self.label = tk.Label(self, text = "Hello, Admin", font = LARGE_FONT)
        self.label.pack(pady = 10, padx = 10)

        self.btnLogin = tk.Button(self, text = "Run Route", command = lambda: self.run_algorithm())
        self.btnLogin.place(relx = 0.25, rely = 0.7, height = 60, width = 100)

        self.btnCancel = tk.Button(self, text = "Get Employee List", command = lambda: self.get_employee_list())
        self.btnCancel.place(relx = 0.7, rely = 0.7, height = 60, width = 100)


class PageTwo(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        label = tk.Label(self, text = "Page Two!!!", font = LARGE_FONT)
        label.pack(pady = 10, padx = 10)

        button1 = tk.Button(self, text = "Back to Home",
                            command = lambda: controller.show_frame(LoginPage))
        button1.pack()

        button2 = tk.Button(self, text = "Page One",
                            command = lambda: controller.show_frame(PageOne))
        button2.pack()


if __name__ == '__main__':
    app = SeaofBTCapp()
    app.geometry('720x480')
    app.mainloop()
