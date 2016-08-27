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
        notebook.add(self.main_canvas, text='main')

        ttk.Button(self.main_canvas, text='Place trade', width=10, command=self.stock_window).place(x=50, y=150)

    def stock_window(self):
        window = Get_quote()


class Get_quote:

    def __init__(self):
        self.top = Toplevel()
        self.top.resizable(False, False)
        self.canvas = Canvas(self.top, width = 220, height = 200)
        self.canvas.pack()
        ttk.Label(self.canvas, text='Get Real-time Quote',font=('calibri',10,'bold')).place(x=50,y=20)
        self.tickers = ttk.Entry(self.canvas, width=10)
        self.tickers.place(x=50, y=50)
        ttk.Button(self.canvas, text='Pull Data', width=10, command=self.stock_quote).place(x=50, y=150)

        self.ticker_quote = ttk.Label(self.canvas, text='',font=('calibri',10,'bold'))
        self.ticker_quote.place(x=50,y=80)       
    
    def stock_quote(self):
       tickers = self.tickers.get()
       if tickers == '': self.ticker_quote.config(text='no ticker')
       else:
            try:
               full_quote = last_price(tickers) + '\n' + last_trade_time(tickers) + '\nID: ' + ticker_id(tickers)
               self.ticker_quote.config(text=full_quote)
            except urllib.error.HTTPError:
                self.ticker_quote.config(text='ticker does not exist')

        


#---------------------------------------------------------------------------------------------------
def main():
    root = Tk()
    app = Main_app(root)
    root.mainloop()
  
if __name__ == "__main__":
    main()
