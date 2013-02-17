from Tkinter import *
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2TkAgg
from matplotlib.figure import Figure
import matplotlib.pyplot as plt
from numpy import arange

class BasGUI:
    def __init__(self,master):

        #Create frames
        
        self.frmMain = Frame(master)
        self.frmMain.pack()
        self.frmBtns = Frame(self.frmMain,borderwidth=5,relief=RIDGE,height=100,width=250)
        self.frmBtns.pack(side=TOP,expand=YES,fill=Y,ipadx='5m',ipady='3m',padx='2m',pady='2m')

        #Create Buttons
        self.btnPlot = Button(self.frmBtns, text = 'Plot',command = self.btnPlotClick)
        self.btnClear = Button(self.frmBtns, text = 'Clear',command = self.btnClearClick)
        self.btnPlot.configure(width=6,padx='2m',pady='1m')
        self.btnClear.configure(width=6,padx='2m',pady='1m')
        self.btnPlot.pack(side=LEFT)
        self.btnClear.pack(side=RIGHT)

        #Create Figure
        self.fig = Figure(figsize=(5,5),dpi=100)
        self.ax = self.fig.add_subplot(111)
        self.ax.set_ylim(0,5)
        self.ax.set_xlim(-5,5)
        self.xdata = [0]
        self.ydata = [0]
        

        #Create Canvas

        self.canvas = FigureCanvasTkAgg(self.fig,master=master)
        self.canvas.show()
        self.canvas.get_tk_widget().pack(side=BOTTOM,fill=BOTH,expand=1)
        
    def btnPlotClick(self):
        self.ax.set_ylim(0,5)
        self.ax.set_xlim(-5,5)
        self.xdata = arange(-5,5,0.01)
        self.ydata = self.xdata**2
        self.ax.plot(self.xdata,self.ydata)
        self.canvas.show()
        
        return

    def btnClearClick(self):
        self.ax.clear()
        self.ax.set_ylim(0,5)
        self.ax.set_xlim(-5,5)
        self.xdata = 0
        self.ydata = 0
        self.ax.plot(self.xdata,self.ydata)
        self.canvas.show()
        return
root = Tk()
basgui = BasGUI(root)


root.mainloop()
