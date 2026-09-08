# view/plano_view.py 
import tkinter as tk
import ttkbootstrap as tb 
from ttkbootstrap.constants import * 
from ttkbootstrap import dialogs, Tableview
from controller.plano_controller import PlanoController 
 
class PlanoView: 
    def __init__(self, parent): 
        self.parent = parent 
        self._criar_tela() 
 
    def _criar_tela(self): 
        tb.Label( 
            self.parent, text='💊  Cadastro de Planos de Saúde', 
            font=('Arial', 16, 'bold') 
        ).pack(anchor='w', pady=(0,5)) 
        tb.Separator(self.parent, bootstyle='warning').pack(fill='x', 
pady=(0,15)) 
 
        notebook = tb.Notebook(self.parent, bootstyle='warning') 
        notebook.pack(fill='both', expand=True) 
 
        aba_form = tb.Frame(notebook, padding=20) 
        notebook.add(aba_form, text='  ➕  Novo Plano  ') 
 
        frame = tk.LabelFrame(
            aba_form, text=' Dados do Plano ', padx=25, pady=25
        )
        frame.pack(fill='x') 
 
        tb.Label(frame, text='Nome do Plano *', 
font=('Arial',10,'bold')).grid( 
            row=0, column=0, sticky='w', padx=5, pady=(5,2) 
        ) 
        self.entry_nome = tb.Entry(frame, width=35, font=('Arial',11), 
bootstyle='warning') 
        self.entry_nome.grid(row=1, column=0, padx=5, pady=5, sticky='ew') 
 
        tb.Label(frame, text='Código *', font=('Arial',10,'bold')).grid( 
            row=0, column=1, sticky='w', padx=5, pady=(5,2) 
        ) 
        self.entry_cod = tb.Entry(frame, width=20, font=('Arial',11), 
bootstyle='warning') 
        self.entry_cod.grid(row=1, column=1, padx=5, pady=5, sticky='ew') 
 
        frame.columnconfigure(0, weight=2) 
        frame.columnconfigure(1, weight=1) 
 
        tb.Button( aba_form, text='✅  Salvar Plano', bootstyle='warning', 
            width=18, command=self._salvar 
        ).pack(pady=15, ipady=5) 
 
        aba_lista = tb.Frame(notebook, padding=15) 
        notebook.add(aba_lista, text='  📋  Lista de Planos  ') 
        self._criar_listagem(aba_lista) 
 
    def _salvar(self): 
        nome = self.entry_nome.get().strip() 
        cod  = self.entry_cod.get().strip() 
        ok, msg = PlanoController.salvar(nome, cod) 
        if ok: 
            dialogs.Messagebox.show_info(msg, 'Sucesso') 
            self.entry_nome.delete(0,'end') 
            self.entry_cod.delete(0,'end') 
        else: 
            dialogs.Messagebox.show_error(msg, 'Erro') 
 
    def _criar_listagem(self, parent): 
        tb.Button( 
            parent, text='🔄  Atualizar', 
            bootstyle='warning-outline', command=self._atualizar_tabela 
        ).pack(anchor='e', pady=(0,10)) 
        self.frame_tab = tb.Frame(parent) 
        self.frame_tab.pack(fill='both', expand=True) 
        self._atualizar_tabela() 
 
    def _atualizar_tabela(self): 
        for w in self.frame_tab.winfo_children(): w.destroy() 
        dados = PlanoController.listar() 
        colunas = [ 
            {'text': 'ID',     'stretch': False, 'width': 60}, 
            {'text': 'Nome',   'stretch': True,  'width': 250}, 
            {'text': 'Código', 'stretch': False, 'width': 120}, 
        ] 
        linhas = [(p['id'], p['nome'], p['codigo']) for p in dados] 
        Tableview( 
            master=self.frame_tab, coldata=colunas, rowdata=linhas, 
            paginated=True, searchable=True, bootstyle='warning', 
        ).pack(fill='both', expand=True) 