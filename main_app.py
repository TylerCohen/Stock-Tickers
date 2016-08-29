from Lib import *
from tkinter import *
from tkinter import ttk
import urllib
import pypyodbc
import threading
import time

class Main_app:

    def __init__(self, master):    
        
        master.title('Stock Traker Pro')
        master.resizable(False, False)

        notebook = ttk.Notebook(master)
        notebook.pack()

        h,w = 400,500
        self.main_canvas = Canvas(notebook, width=w, height=w)
        self.settings_canvas = Canvas(notebook, width=w, height=h)
        notebook.add(self.main_canvas, text='Main')
        notebook.add(self.settings_canvas, text='Settings')

        ttk.Button(self.main_canvas, text='Place Trade', width=12, command=self.stock_window).place(x=w-20, y=h+70,anchor='se')
        self.account_value = 100000
        self.stock_value = 0
        self.derivatives_value = 0
        self.available_cash = self.account_value - self.stock_value - self.derivatives_value
        self.margin_balance = self.account_value / 2

        self.cash_label = ttk.Label(self.main_canvas,
                                    text='Account Value: ' + '${:,.2f}'.format(self.account_value), font=('calibri', 16, 'bold'))
        self.cash_label.place(x=w/2-130,y=20)
        self.logo = PhotoImage(file='logo.png').subsample(2,2)
        self.main_canvas.create_image(w-30,30,image=self.logo)
        self.main_canvas.create_rectangle(20,75,w-20,h+70)
        self.main_canvas.create_line(w/2,75,w/2,h+70)
        self.balances_frame = Canvas(self.main_canvas, width=w/2-30,height=h-50)
        self.balances_frame.place(x=25,y=80)
        #self.scrollbar = ttk.Scrollbar(self.balances_frame)
        #self.scrollbar.pack(fill=Y, side=RIGHT)
        #self.balances_frame.config(yscrollcommand=self.scrollbar.set)
        #self.scrollbar.config(command=self.balances_frame.yview)
        self.balances_label = ttk.Label(self.balances_frame, 
                                        text='Account value: ' + '${:,.2f}'.format(self.account_value) +
                                        '\nCash balance: '+'${:,.2f}'.format(self.available_cash) +
                                        '\nStock value: ' + '${:,.2f}'.format(self.stock_value) +
                                        '\nDerivatives value: ' + '${:,.2f}'.format(self.derivatives_value) +
                                        '\nAvailable Margin: ' + '${:,.2f}'.format(self.margin_balance),
                                        font=('calibri', 12), wraplength=w/2-30)
        self.balances_label.pack()


    def stock_window(self):
        window = Place_trade(self)


class Place_trade:

    def __init__(self, master):
        self.master = master
        self.top = Toplevel()
        self.top.resizable(False, False)
        w,h = 400,200
        self.canvas = Canvas(self.top, width = w, height = h)
        self.canvas.pack()
        self.canvas.create_line(w/2,0,w/2,h,width=1)

        ttk.Label(self.canvas, text='Real-time Quote',
                  font=('calibri',10,'bold')).place(x=30,y=20)
        self.tickers = ttk.Entry(self.canvas, width=10)
        self.tickers.place(x=30, y=50)
        ttk.Button(self.canvas, text='Fetch Quote', width=12,
                   command=self.stock_quote).place(x=30, y=150)
        self.ticker_quote = ttk.Label(self.canvas, text='',
                                      font=('calibri',10,'bold'))
        self.ticker_quote.place(x=30,y=80)

        ttk.Label(self.canvas,text='Enter number of shares',
                  font=('calibri',10,'bold')).place(x=w/2+30,y=20)
        self.num_shares = ttk.Entry(self.canvas,width=10)
        self.num_shares.bind("<KeyRelease>",self.calc_trade_cost)
        self.num_shares.place(x=w/2+30,y=50)
        ttk.Button(self.canvas,width=13,text='Execute Trade', 
                   command=self.excecute_trade).place(x=w/2+30,y=150)
        self.thread_id = 1
        self.trade_amount = ttk.Label(self.canvas, text='',
                  font=('calibri',10,'bold'), wraplength=w/2-40)
        self.trade_amount.place(x=w/2+30,y=80)
        self.trade_cost = 0

    def stock_quote(self):
        try:
            threading.enumerate().index(self.quotethread)
            self.quotethread.stop()
            self.quotethread = QuoteThread(self.thread_id,'quote_thread',1, 600,
                                           self.tickers.get(),self.ticker_quote)
        except (ValueError, AttributeError):
            self.quotethread = QuoteThread(self.thread_id,'quote_thread',1, 600, 
                                           self.tickers.get(),self.ticker_quote)
        self.quotethread.start()
        self.thread_id += 1

    def calc_trade_cost(self, event):
        try:
            self.trade_cost = int(self.num_shares.get()) * float(last_price(self.tickers.get()))
            self.trade_amount.config(text = 'Estimated Cost: '+ '${:,.2f}'.format(self.trade_cost)
                                     +'\n\nAvailable Cash: '+ '${:,.2f}'.format(self.master.available_cash))
        except ValueError:
            self.trade_amount.config(text = 'Input a positive whole amount')
            self.trade_cost = 0
        except urllib.error.HTTPError:
            self.trade_amount.config(text = 'Input a valid ticker')
            self.trade_cost=0
    
    def excecute_trade(self):
        if self.master.available_cash < self.trade_cost:
            self.trade_amount.config(text = 'Not enough available cash')
        elif self.trade_cost == 0: 
            self.trade_amount.config(text = 'Construct potential trade')
        else:
            self.calc_trade_cost('dummy')
            self.master.available_cash -= self.trade_cost
            self.calc_trade_cost('dummy')


class QuoteThread(threading.Thread):
    def __init__(self, threadID, name, delay, timeout, tickers, label):
        threading.Thread.__init__(self)
        self.threadID = threadID
        self.name = name
        self.timeout = timeout
        self.delay = delay
        self.tickers = tickers
        self.label = label
        self.stop_event = threading.Event()

    def run(self):
        self.label.config(text='Fetching Quote...')
        self.get_stock_quote()

    def stop(self):
        self.stop_event.set()

    def get_stock_quote(self):
        while(self.timeout):
            if self.stop_event.is_set(): break
            if self.tickers == '':
                self.label.config(text='enter a valid\nticker')
                return -1
                break
            else:
                try:
                   self.label.config(text=last_price(self.tickers) + '\n' +
                                last_trade_time(self.tickers) + '\nID: ' + ticker_id(self.tickers))
                except urllib.error.HTTPError:
                    self.label.config(text='ticker does not exist')
                    return -1
                    break
            time.sleep(self.delay)
            self.timeout -= 1


#---------------------------------------------------------------------------------------------------
def main():
    root = Tk()
    app = Main_app(root)
    root.mainloop()
  
if __name__ == "__main__":
    main()
