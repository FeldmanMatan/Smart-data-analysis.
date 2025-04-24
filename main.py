import tkinter as tk
from gui import CSVLoaderApp

def main():
    """
    Main entry point for the application.
    Initializes the GUI and starts the Tkinter main loop.
    """
    root = tk.Tk()
    app = CSVLoaderApp(root)
    root.mainloop()

if __name__ == "__main__":
    main()
