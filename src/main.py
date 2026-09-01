import tkinter as tk

def main():
    root = tk.Tk()
    root.title("Workflow Organising Tool")
    root.geometry("400x200")
    print("Python project initialized successfully!")
    label = tk.Label(root, text="Welcome!", font=("Ariel", 16))
    label.pack(pady=20)
    root.mainloop()

if __name__ == "__main__":
    main()
