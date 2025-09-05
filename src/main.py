import tkinter as tk

def main():
    root = tk.Tk()
    root.title("My Tkinter App")
    root.geometry("400x300")

    label = tk.Label(root, text="Hello, Tkinter!")
    label.pack(pady=20)

    button = tk.Button(root, text="Click Me", command=lambda: label.config(text="Button Clicked!"))
    button.pack()

    root.mainloop()

if __name__ == "__main__":
    main()
