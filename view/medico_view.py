# view/medico_view.py 
import tkinter as tk
import ttkbootstrap as tb 
from ttkbootstrap.constants import * 
from ttkbootstrap import dialogs, Tableview
from controller.medico_controller import MedicoController 
 
ESPECIALIDADES = [ 
    'Clínico Geral', 'Cardiologia', 'Ortopedia', 'Neurologia', 
    'Pediatria', 'Ginecologia', 'Dermatologia', 'Oftalmologia', 
    'Psiquiatria', 'Endocrinologia', 'Urologia', 'Oncologia' 
] 
 
class MedicoView: 
    def __init__(self, parent): 
        self.parent = parent 
        self._criar_tela() 
 
    def _criar_tela(self): 
        tb.Label( 
            self.parent, 
            text='👨‍⚕️  Cadastro de Médicos', 
            font=('Arial', 16, 'bold') 
        ).pack(anchor='w', pady=(0,5)) 
        tb.Separator(self.parent, bootstyle='success').pack(fill='x', 
pady=(0,15)) 
 
        notebook = tb.Notebook(self.parent, bootstyle='success') 
        notebook.pack(fill='both', expand=True) 
 
        aba_form = tb.Frame(notebook, padding=15)
        notebook.add(aba_form, text='  ➕  Novo Médico  ') 
        self._criar_formulario(aba_form) 
 
        aba_lista = tb.Frame(notebook, padding=15) 
        notebook.add(aba_lista, text='  📋  Lista de Médicos  ') 
        self._criar_listagem(aba_lista) 
 
    def _criar_formulario(self, parent): 
        frame = tk.LabelFrame(
            parent, text=' Dados do Médico ', padx=20, pady=20
        )
        frame.pack(fill='x', pady=10) 
 
        # Nome completo 
        tb.Label(frame, text='Nome Completo *', 
font=('Arial',10,'bold')).grid( 
            row=0, column=0, columnspan=2, sticky='w', padx=5, pady=(5,2) 
        ) 
        self.entry_nome = tb.Entry(frame, width=50, font=('Arial',11), 
bootstyle='success') 
        self.entry_nome.grid(row=1, column=0, columnspan=2, padx=5, pady=5, 
sticky='ew') 
 
        # Especialidade (Combobox) e CRM 
        tb.Label(frame, text='Especialidade *', 
font=('Arial',10,'bold')).grid( 
            row=2, column=0, sticky='w', padx=5, pady=(10,2) 
        ) 
        self.combo_esp = tb.Combobox( 
            frame, values=ESPECIALIDADES, state='readonly', 
bootstyle='success', width=28 
        ) 
        self.combo_esp.grid(row=3, column=0, padx=5, pady=5, sticky='ew') 
        self.combo_esp.current(0) 
 
        tb.Label(frame, text='CRM *', font=('Arial',10,'bold')).grid( 
            row=2, column=1, sticky='w', padx=5, pady=(10,2) 
        ) 
        self.entry_crm = tb.Entry(frame, width=20, font=('Arial',11), 
bootstyle='success') 
        self.entry_crm.grid(row=3, column=1, padx=5, pady=5, sticky='ew') 
 
        frame.columnconfigure(0, weight=1) 
        frame.columnconfigure(1, weight=1) 
 
        # Botões 
        frame_btn = tb.Frame(parent) 
        frame_btn.pack(fill='x', pady=15) 
 
        tb.Button( 
            frame_btn, text='✅  Salvar Médico', bootstyle='success', 
            width=20, command=self._salvar ).pack(side='left', padx=5, ipady=5) 
 
        tb.Button( 
            frame_btn, text='🗑️  Limpar', bootstyle='secondary', 
            width=15, command=self._limpar 
        ).pack(side='left', padx=5, ipady=5) 
 
    def _salvar(self): 
        nome = self.entry_nome.get().strip() 
        esp  = self.combo_esp.get() 
        crm  = self.entry_crm.get().strip() 
 
        ok, msg = MedicoController.salvar(nome, esp, crm) 
        if ok: 
            dialogs.Messagebox.show_info(msg, 'Sucesso') 
            self._limpar() 
        else: 
            dialogs.Messagebox.show_error(msg, 'Erro') 
 
    def _limpar(self): 
        self.entry_nome.delete(0, 'end') 
        self.entry_crm.delete(0, 'end') 
        self.combo_esp.current(0) 
        self.entry_nome.focus() 
 
    def _criar_listagem(self, parent): 
        tb.Button( 
            parent, text='🔄  Atualizar', 
            bootstyle='success-outline', command=self._atualizar_tabela 
        ).pack(anchor='e', pady=(0,10)) 
        self.frame_tab = tb.Frame(parent) 
        self.frame_tab.pack(fill='both', expand=True) 
        self._atualizar_tabela() 
 
    def _atualizar_tabela(self): 
        for w in self.frame_tab.winfo_children(): w.destroy() 
        dados = MedicoController.listar() 
        colunas = [ 
            {'text': 'ID',            'stretch': False, 'width': 50}, 
            {'text': 'Nome',          'stretch': True,  'width': 200}, 
            {'text': 'Especialidade', 'stretch': True,  'width': 160}, 
            {'text': 'CRM',           'stretch': False, 'width': 120}, 
        ] 
        linhas = [(m['id'], m['nome'], m['especialidade'], m['crm']) for m 
in dados] 
        Tableview( 
            master=self.frame_tab, coldata=colunas, rowdata=linhas, 
            paginated=True, searchable=True, bootstyle='success', 
            stripecolor=('#f0fff0', None) 
        ).pack(fill='both', expand=True) 