import tkinter as tk
from tkinter import ttk
from tkinter import messagebox 

def main_layout(root):
    label = ttk.Label(root, text="Welcome!", font=("Ariel", 16))
    label.pack(pady=20)

    def handle_click():
        user_text = entry_field.get()
        messagebox.showinfo("Alert", f"You typed: {user_text}")
    
    entry_field = ttk.Entry(root)
    entry_field.pack(pady=10)
    
    action_btn = ttk.Button(root, text="Submit", command=handle_click)
    action_btn.pack()

def main():
    root = tk.Tk()
    root.title("Workflow Organising Tool")
    root.geometry("400x200")
    main_layout(root)
    print("Python project initialized successfully!")
    root.mainloop()

if __name__ == "__main__":
    main()
