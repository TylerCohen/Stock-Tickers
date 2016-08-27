from Libr import *
from tkinter import *
from tkinter import ttk
import urllib


class Main_app:

    def __init__(self, master):    
        
        master.title('Stock Traker Pro')
        master.resizable(False, False)

        notebook = ttk.Notebook(master)
        notebook.pack()
        
        self.main_canvas = Canvas(notebook, width=500, height=600)
        self.main_canvas.pack()

        ttk.Button(self.main_canvas, text='get quote', width=10, command=self.stock_quote).place(x=50, y=110)

        ttk.Label(self.main_canvas, text='Pull stock data',font=('calibri',10,'bold')).place(x=50,y=20)
        self.tickers = ttk.Entry(self.main_canvas, width=20)
        self.tickers.place(x=50, y=50)

        self.current_quote = ''
        self.ticker_quote = ttk.Label(self.main_canvas, text=self.current_quote,font=('calibri',10,'bold'))
        self.ticker_quote.place(x=50,y=80)
        
    
    def stock_quote(self):
       entries = self.tickers.get()
       if entries == '': self.ticker_quote.config(text='no ticker')
       else:
            try:
               prices = str(last_price(entries))
               self.ticker_quote.config(text=prices)
            except urllib.error.HTTPError:
                self.ticker_quote.config(text='ticker does not exist')

        


#---------------------------------------------------------------------------------------------------
def main():
    root = Tk()
    app = Main_app(root)
    root.mainloop()
  
if __name__ == "__main__":
    main()
