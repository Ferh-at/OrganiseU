import customtkinter
from gui.EntryWindow import EntryWindow
from winotify import Notification
import os


base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
icon_path = os.path.join(base_dir, "assets", "QubeLogo.ico")
    
notification = Notification(
    app_id="OrganiseU",
    title="Welcome to OrganiseU!",
    msg="Hope you enjoy your time here!",
    duration="short",
    icon=icon_path)

notification.show()




def InitialiseApp():
    app = customtkinter.CTk()
    app.title("OrganiseU")
    app.geometry("750x750")

    app.grid_rowconfigure(0, weight=1) 
    app.grid_columnconfigure(0, weight=1)

    entry = EntryWindow(app)
    entry.grid(row=0,column=0, sticky="nsew")
   

    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    icon_path = os.path.join(base_dir, "assets", "QubeLogo.ico")
    app.iconbitmap(icon_path)
    
    app.mainloop()


if __name__ == "__main__":
    InitialiseApp()

 #the code is great - emilijano hoxha