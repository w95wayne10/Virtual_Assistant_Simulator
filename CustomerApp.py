import tkinter as tk
from  tkinter  import ttk
import time
import json

class CustomerApp(tk.Tk):
    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)
        self.title('Dialog Box')
        self.geometry('400x750')
        self.resizable(0, 0)
        self.first_time = True
        self.listener = open("log.txt","r",encoding="utf8")
        with open("EXAMPLE.json","r") as json_file:
            DBS_json_temp = json_file.read()
            self.DBS = json.loads(DBS_json_temp)
        
        self.chat_window_init()

        self.bside = tk.Frame(self,height=250)
        self.bside.pack(fill="both",padx=10, pady=(5,5))
        
        self.input_area_init()
        
        self.comvalue=tk.StringVar()#窗体自带的文本，新建一个值
        self.comboxlist=ttk.Combobox(self,textvariable=self.comvalue,font=('微軟正黑體',10),height=20,width=150) #初始化
        self.comboxlist["values"]=tuple(["",*self.DBS.keys()])
        self.comboxlist.current(0)  #选择第一个
        self.comboxlist.bind("<<ComboboxSelected>>",self.go)  #绑定事件,(下拉列表框被选中时，绑定go()函数)
        self.comboxlist.pack(side="bottom",padx=10, pady=(5,10))
        
        self.update_chat_window()
        
    def chat_window_init(self):
        self.chat_window = tk.Text(self,height=30,width=40,font=('微軟正黑體',12))
        self.chat_window.pack(padx=10, pady=(10,5),expand=True)
        self.chat_window.tag_configure("right", justify="right")
        self.chat_window.tag_configure("left", justify="left")
        
        mes = self.listener.readline()
        while mes!="":
            if mes[:5]=="<agt>":
                side = "right"
                self.chat_window.insert('end',"Agent Sheep:\n",side)
                mes_time = mes[6:14]
                mes = mes[15:]
                self.change_opt = False
            elif mes[:5]=="<ctm>":
                side = "left"
                self.chat_window.insert('end',"Customer 1:\n",side)
                mes_time = mes[6:14]
                mes = mes[15:]
                self.change_opt = True
                
            
            temp = self.listener.readline()
            while temp!= "" and temp[:5]!="<agt>" and temp[:5]!="<ctm>":
                mes+=temp
                temp = self.listener.readline()

            self.chat_window.insert('end',mes,side)
            self.chat_window.insert('end',mes_time+"\n\n",side)
            if self.change_opt:
                self.lastQ = mes[:-1]
            mes=temp
        self.chat_window.config(state=tk.DISABLED)
        return None
            
    def input_area_init(self):
        self.input_title = tk.Label(self.bside,text='Typing Box',font=('微軟正黑體', 16))
        self.input_title.pack(pady=(10,5))
        

        self.input_text = tk.Text(self.bside,width=30,height=1,font=('微軟正黑體',14))
        self.input_text.pack(side='left',padx=(0,1), pady=5)
        
        self.send_button = tk.Button(self.bside, text='送出',font=('微軟正黑體',8), width=5, height=1, command=self.send) # 點選按鈕式執行的命令
        self.send_button.pack(side='right',padx=(1,0), pady=5)
        return None
        
    def send(self):
        if not self.input_text.get("1.0",tk.END).isspace():
            with open("log.txt","a+",encoding="utf8") as ag_mes:
                ag_mes.write("<ctm><"+time.strftime("%H:%M:%S" , time.localtime())+">"+self.input_text.get("1.0",tk.END))
        else:
            pass
        self.input_text.delete("1.0",tk.END)
        return None
            
    def update_chat_window(self):
        mes = self.listener.readline()
        if mes!="":
            self.chat_window.config(state=tk.NORMAL)
            if mes[:5]=="<agt>":
                side = "left"
                self.chat_window.insert('end',"Agent Sheep:\n",side)
            else:
                side = "right"
                self.chat_window.insert('end',"Customer 1:\n",side)
            mes_time = mes[6:14]
            mes = mes[15:]
            temp = self.listener.readline()
            while temp:
                mes+=temp
                temp = self.listener.readline()
            self.chat_window.insert('end',mes,side)
            self.chat_window.insert('end',mes_time+"\n\n",side)
            self.chat_window.config(state=tk.DISABLED)
            self.chat_window.yview_moveto(1)
        self.after(1000, self.update_chat_window)
        return None
           
    def go(self,*args):   
        self.input_text.insert('end',self.comboxlist.get())
        self.comboxlist.current(0)
        return None
        
    def __exit__(self):
        self.listener.close()
        return None
    
app = CustomerApp()
app.mainloop()