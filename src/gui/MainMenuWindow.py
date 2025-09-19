import customtkinter


class MainMenu(customtkinter.CTkFrame):
    def __init__(self, parent):
        super().__init__(parent)

        self.parent = parent
    

    def FadeOut(self, step=0.05):
        alpha = self.parent.attributes("-alpha")
        if alpha > 0:
            alpha = max(0, alpha - step)
            self.parent.attributes("-alpha", alpha)
            self.after(20, self.FadeOut, step)
        else:
            self.destroy()
            login = MainMenu(self.parent)
            login.grid(row=0, column=0, sticky="nsew")
            login.FadeIn()
    def FadeIn(self, step=0.05):
        alpha = self.parent.attributes("-alpha")
        if alpha < 1:
            alpha = min(1, alpha + step)
            self.parent.attributes("-alpha", alpha)
            self.after(20, self.FadeIn, step)

    def SlideOut(self, x=0):
        if x <= 750:
            self.place(x=-x, y=0)
            self.parent.update()
            self.after(3, self.SlideOut, x+15)
        else:
            self.destroy()
            login = LoginWindow(self.parent)
            login.place(x=750, y=0) 
            login.SlideIn()

    def SlideIn(self, x=750):
        if x >= 0:
            self.place(x=x, y=0)
            self.parent.update()
            self.after(3, self.SlideIn, x-15)