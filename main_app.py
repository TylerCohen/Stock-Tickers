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
        notebook.add(self.main_canvas, text='main')
        notebook.add(self.settings_canvas, text='settings')

        ttk.Button(self.main_canvas, text='Place Trade', width=12, command=self.stock_window).place(x=50, y=150)
        self.cash = 100000
        self.cash_label = ttk.Label(self.main_canvas,
                                    text='Account Value: ' + '${:,.2f}'.format(self.cash), font=('calibri', 16, 'bold'))
        self.cash_label.place(x=w/2-130,y=20)
        self.logo = PhotoImage(file='logo.png').subsample(2,2)
        self.main_canvas.create_image(w-30,30,image=self.logo)


    def stock_window(self):
        window = Place_trade()


class Place_trade:

    def __init__(self):
        self.top = Toplevel()
        self.top.resizable(False, False)
        w,h = 400,200
        self.canvas = Canvas(self.top, width = w, height = h)
        self.canvas.pack()
        self.canvas.create_line(w/2,0,w/2,h,width=1)

        ttk.Label(self.canvas, text='Real-time Quote',font=('calibri',10,'bold')).place(x=30,y=20)
        self.tickers = ttk.Entry(self.canvas, width=10)
        self.tickers.place(x=30, y=50)
        ttk.Button(self.canvas, text='Fetch Quote', width=12, command=self.stock_quote).place(x=30, y=150)
        self.ticker_quote = ttk.Label(self.canvas, text='',font=('calibri',10,'bold'))
        self.ticker_quote.place(x=30,y=80)

        ttk.Label(self.canvas,text='Enter number of shares',font=('calibri',10,'bold')).place(x=w/2+30,y=20)
        self.num_shares = ttk.Entry(self.canvas,width=10)
        self.num_shares.place(x=w/2+30,y=50)
        #self.num_shares.event_add(
        ttk.Button(self.canvas,width=13,text='Execute Trade').place(x=w/2+30,y=150)
        self.thread_list, self.thread_id = [], 1

    def stock_quote(self):
        if len(self.thread_list) >= 1: self.quotethread.stop()
        self.quotethread = QuoteThread(self.thread_id,'current_thread',5, 20, self.tickers.get(),self.ticker_quote)
        self.quotethread.start()
        self.thread_list.append(self.thread_id)
        self.thread_id +=1


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
