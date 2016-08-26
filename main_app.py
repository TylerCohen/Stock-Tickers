#import googlefinance
from tkinter import *
from tkinter import ttk


class CalcApp:

    def __init__(self, master):    
        
        master.title('Stock Ticker Pro')
        master.resizable(False, False)

        notebook = ttk.Notebook(master)
        notebook.pack()
        
        self.main_canvas = Canvas(notebook, width=500, height=600)
        self.main_canvas.pack()

#---------------------------------------------------------------------------------------------------
def main():
    root = Tk()
    app = CalcApp(root)
    root.mainloop()
  
if __name__ == "__main__":
    main()
