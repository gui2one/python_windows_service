import customtkinter as ctk


class ControlWindow(ctk.CTk):
    def __init__(self, master=None, **kwargs):
        super().__init__(master, **kwargs)

        self.title("Control Window")
        self.geometry("300x200")
        self.resizable(False, False)


if __name__ == "__main__":
    window = ControlWindow()
    window.mainloop()
