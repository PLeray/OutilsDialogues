import tkinter as tk

window = tk.Tk()
window.title("Test Tkinter")
window.geometry("400x200")
label = tk.Label(window, text="Fenêtre tkinter fonctionnelle !", font=("Arial", 16))
label.pack(pady=20)
window.mainloop()

