import tkinter as tk
import time
import json

class AgentApp(tk.Tk):
    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)
        self.title('Virtual Assistant Simulator')
        self.geometry('900x750')
        self.resizable(0, 1)
        self.change_opt = False
        self.lastQ = ""
        self.listener = open("log.txt","r",encoding="utf8")
        with open("EXAMPLE.json","r") as json_file:
            DBS_json_temp = json_file.read()
            self.DBS = json.loads(DBS_json_temp)
        
        self.lside = tk.Frame(self,width=350)
        self.lside.pack(side='left',fill="both",padx=(10,5), pady=10)
        
        self.chat_window_init()
        
        self.rside = tk.Frame(self)
        self.rside.pack(side='right',fill="both",expand=True,padx=(5,10), pady=10)
        
        self.ruside = tk.Frame(self.rside,height=500)
        self.ruside.pack(side='top',fill="both",padx=0, pady=(0,5))
        
        self.options_area_init()
        
        self.rbside = tk.Frame(self.rside,height=250)
        self.rbside.pack(side='bottom',fill="both",padx=0, pady=(5,0))
        
        self.input_area_init()
        
        self.update_chat_window()
        
    def chat_window_init(self):
        self.chat_window = tk.Text(self.lside,height=50,width=40,font=('微軟正黑體',12))
        self.chat_window.pack()
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
    
    def options_area_init(self):
        self.options_title = tk.Label(self.ruside,text='Oracle Agent',font=('微軟正黑體', 16))
        self.options_title.pack(pady=(20,10))
        
        self.options_var=[]
        self.select_var = tk.StringVar()
        self.radio_bts = []
        for i in range(5):
            self.options_var.append(tk.StringVar())
            if self.change_opt and self.DBS.get(self.lastQ,""):
                temp = self.DBS[self.lastQ][i]
                n = 20
                self.options_var[i].set('\n'.join([temp[i:i+n] for i in range(0, len(temp), n)]))
            else:
                self.options_var[i].set("option "+chr(ord('A')+i))
                
            self.radio_bts.append(tk.Radiobutton(self.ruside,
                                                 textvariable=self.options_var[i],
                                                 variable=self.select_var,
                                                 value=i,
                                                 command=self.print_selection,
                                                 font=('微軟正黑體', 14)))
            self.radio_bts[i].pack()
            self.radio_bts[i].deselect()
        return None
    
    def input_area_init(self):
        self.input_title = tk.Label(self.rbside,text='Typing Box',font=('微軟正黑體', 16))
        self.input_title.pack(pady=(20,10))
        

        self.input_text = tk.Text(self.rbside,width=42,height=1,font=('微軟正黑體',14))
        self.input_text.pack(side='left',padx=(0,1), pady=10)
        
        self.send_button = tk.Button(self.rbside, text='送出',font=('微軟正黑體',8), width=5, height=1, command=self.send) # 點選按鈕式執行的命令
        self.send_button.pack(side='right',padx=(1,0), pady=9)
        return None
    
    def print_selection(self):
        self.input_text.delete("1.0", tk.END)
        if self.change_opt and self.DBS.get(self.lastQ,""):
            temp = self.DBS[self.lastQ][int(self.select_var.get())]
            n = 20
            self.input_text.insert('end', '\n'.join([temp[i:i+n] for i in range(0, len(temp), n)]))
        else:
            self.input_text.insert('end', "Option "+chr(ord('A')+int(self.select_var.get())))
        return None
    
    def send(self):
        if not self.input_text.get("1.0",tk.END).isspace():
            with open("log.txt","a+",encoding="utf8") as ag_mes:
                ag_mes.write("<agt><"+time.strftime("%H:%M:%S" , time.localtime())+">"+self.input_text.get("1.0",tk.END))
            for i in range(5):
                self.radio_bts[i].deselect()
        else:
            pass
        self.input_text.delete("1.0",tk.END)
        return None
    
    def update_chat_window(self):
        mes = self.listener.readline()
        if mes!="":
            self.chat_window.config(state=tk.NORMAL)
            if mes[:5]=="<agt>":
                side = "right"
                self.chat_window.insert('end',"Agent Sheep:\n",side)
                self.change_opt = False
            else:
                side = "left"
                self.chat_window.insert('end',"Customer 1:\n",side)
                self.change_opt = True
            mes_time = mes[6:14]
            mes = mes[15:]
            temp = self.listener.readline()
            while temp:
                mes+=temp
                temp = self.listener.readline()
            self.chat_window.insert('end',mes,side)
            
            if self.change_opt:
                self.lastQ = mes[:-1]
            for i in range(5):   
                if self.change_opt and self.DBS.get(self.lastQ,""):
                    temp = self.DBS[self.lastQ][i]
                    n = 20
                    self.options_var[i].set('\n'.join([temp[i:i+n] for i in range(0, len(temp), n)]))
                else:
                    self.options_var[i].set("option "+chr(ord('A')+i))
            
            self.chat_window.insert('end',mes_time+"\n\n",side)
            self.chat_window.config(state=tk.DISABLED)
            self.chat_window.yview_moveto(1)
        self.after(1000, self.update_chat_window)
        return None
    
    def __exit__(self):
        self.listener.close()
        return None
    
app = AgentApp()
app.mainloop()