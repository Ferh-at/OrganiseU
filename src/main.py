import customtkinter
from gui.EntryWindow import EntryWindow


def InitialiseApp():
    app = customtkinter.CTk()
    app.title("OrganiseU")
    app.geometry("750x750")

    app.grid_rowconfigure(0, weight=1) 
    app.grid_columnconfigure(0, weight=1)

    entry = EntryWindow(app)
    entry.grid(row=0,column=0, sticky="nsew")
    
    app.mainloop()


if __name__ == "__main__":
    InitialiseApp()