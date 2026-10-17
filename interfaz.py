""" Interfaz Tkinter del diseñador y validador."""
import tkinter as tk
from tkinter import ttk, messagebox, filedialog
from pathlib import Path
import math
from core.lexico import leer_alfabeto
from core.regex_parser import convertir_postfija
from core.thompson import construir_afn
from core.subconjuntos import convertir_afd
from core.minimizacion import minimizar
from core.simulador import simular
from core.visualizador import generar_dot

class Aplicacion:
    def __init__(self, root: tk.Tk):
        self.root=root; root.title('Diseñador y Validador de Lenguajes Formales'); root.geometry('980x710')
        self.automatas={}
        cont=ttk.Frame(root,padding=16); cont.pack(fill='both',expand=True)
        ttk.Label(cont,text='Diseñador y Validador de Lenguajes Formales',font=('Arial',17,'bold')).pack(anchor='w',pady=8)
        entradas=ttk.Frame(cont); entradas.pack(fill='x')
        self.campos={}
        for fila,(etiqueta,valor) in enumerate([('Alfabeto Σ (ej. 0,1)','0,1'),('Regex (ej. (0|1)*01)','(0|1)*01'),('Cadena a validar','1001')]):
            ttk.Label(entradas,text=etiqueta).grid(row=fila,column=0,sticky='w',pady=6)
            v=tk.StringVar(value=valor); self.campos[fila]=v
            ttk.Entry(entradas,textvariable=v,width=65).grid(row=fila,column=1,padx=10,sticky='ew')
        entradas.columnconfigure(1,weight=1)
        botones=ttk.Frame(cont); botones.pack(fill='x',pady=12)
        ttk.Button(botones,text='Generar autómatas y validar',command=self.ejecutar).pack(side='left',padx=3)
        ttk.Button(botones,text='Exportar grafo .dot',command=self.exportar).pack(side='left',padx=3)
        self.tipo=tk.StringVar(value='AFN')
        ttk.Combobox(botones,textvariable=self.tipo,values=['AFN','AFD','AFD mínimo'],state='readonly',width=14).pack(side='left',padx=8)
        self.resultado=ttk.Label(cont,text='Pendiente de evaluación',font=('Arial',12,'bold'))
        self.resultado.pack(anchor='w',pady=8)
        self.tabs=ttk.Notebook(cont); self.tabs.pack(fill='both',expand=True)
        self.textos={}
        self.lienzos={}
        for nombre in ['AFN','AFD','AFD mínimo','Simulación']:
            marco=ttk.Frame(self.tabs); self.tabs.add(marco,text=nombre)
            if nombre != 'Simulación':
                canvas=tk.Canvas(marco,height=250,bg='#f8fafc',highlightthickness=0)
                canvas.pack(fill='x',padx=4,pady=4)
                self.lienzos[nombre]=canvas
            cuadro=tk.Text(marco,font=('Consolas',10),wrap='none')
            barra=ttk.Scrollbar(marco,orient='vertical',command=cuadro.yview)
            cuadro.configure(yscrollcommand=barra.set)
            barra.pack(side='right',fill='y'); cuadro.pack(side='left',fill='both',expand=True)
            self.textos[nombre]=cuadro
    def ejecutar(self):
        try:
            alfabeto=leer_alfabeto(self.campos[0].get())
            postfija=convertir_postfija(self.campos[1].get(),alfabeto)
            afn=construir_afn(postfija,alfabeto)
            afd=convertir_afd(afn)
            minimo=minimizar(afd)
            aceptada,pasos=simular(minimo,self.campos[2].get())
            self.automatas={'AFN':afn,'AFD':afd,'AFD mínimo':minimo}
            for nombre,automata in self.automatas.items():
                self.escribir(nombre,automata.tabla()+'\n\nGrafo (formato DOT):\n'+generar_dot(automata,nombre))
                self.dibujar(nombre,automata)
            self.escribir('Simulación','\n'.join(pasos))
            self.resultado.configure(text=('✓ ACEPTADA' if aceptada else '✗ RECHAZADA')+f'  |  Postfija: {" ".join(postfija)}')
            self.tabs.select(3)
        except ValueError as exc:
            self.resultado.configure(text='Error: '+str(exc))
            messagebox.showerror('Entrada inválida',str(exc))
    def escribir(self,nombre,contenido):
        texto=self.textos[nombre]; texto.delete('1.0','end');texto.insert('end',contenido)
    def exportar(self):
        nombre=self.tipo.get()
        if nombre not in self.automatas:
            messagebox.showinfo('Aviso','Genere primero los autómatas.');return
        ruta=filedialog.asksaveasfilename(defaultextension='.dot',filetypes=[('Graphviz DOT','*.dot')],initialfile=nombre.replace(' ','_')+'.dot')
        if ruta:
            Path(ruta).write_text(generar_dot(self.automatas[nombre],nombre),encoding='utf-8')
            messagebox.showinfo('Exportado','Grafo guardado. Para convertirlo a PNG puede usar: dot -Tpng archivo.dot -o archivo.png')

    def dibujar(self, nombre, automata):
        """Representación visual simplificada; DOT exporta el grafo completo."""
        canvas=self.lienzos[nombre]; canvas.delete('all')
        estados=sorted(automata.estados)
        if len(estados)>24:
            canvas.create_text(440,110,text='Grafo grande: consulta la tabla o exporta el archivo DOT.',fill='#334155')
            return
        canvas.update_idletasks()
        ancho=max(canvas.winfo_width(),750); alto=240
        cx,cy=ancho/2,120; rx=max(120,min(ancho/2-85,330)); ry=72
        posiciones={q:(cx+rx*math.cos(2*math.pi*i/len(estados)),cy+ry*math.sin(2*math.pi*i/len(estados))) for i,q in enumerate(estados)}
        radio=21
        for (origen,simbolo),destinos in sorted(automata.transiciones.items()):
            x1,y1=posiciones[origen]
            for destino in sorted(destinos):
                x2,y2=posiciones[destino]
                if origen==destino:
                    canvas.create_arc(x1-17,y1-42,x1+17,y1-8,start=20,extent=300,style='arc',outline='#64748b',width=1.5)
                    canvas.create_text(x1,y1-51,text=simbolo,fill='#0f766e',font=('Arial',9,'bold'))
                    continue
                dx,dy=x2-x1,y2-y1;dist=max(1,math.hypot(dx,dy));ux,uy=dx/dist,dy/dist
                canvas.create_line(x1+ux*radio,y1+uy*radio,x2-ux*radio,y2-uy*radio,arrow='last',fill='#94a3b8',width=1.4)
                canvas.create_text((x1+x2)/2-uy*10,(y1+y2)/2+ux*10,text=simbolo,fill='#0f766e',font=('Arial',9,'bold'))
        for q,(x,y) in posiciones.items():
            canvas.create_oval(x-radio,y-radio,x+radio,y+radio,fill='#e0f2fe',outline='#0369a1',width=2)
            if q in automata.finales:
                canvas.create_oval(x-radio+5,y-radio+5,x+radio-5,y+radio-5,outline='#0369a1',width=1)
            canvas.create_text(x,y,text=f'q{q}',font=('Arial',10,'bold'),fill='#0f172a')
            if q==automata.inicial:
                canvas.create_text(x-29,y-25,text='Inicio',font=('Arial',8),fill='#334155')
