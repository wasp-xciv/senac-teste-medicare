# view/paciente_view.py 
import tkinter as tk
import ttkbootstrap as tb 
from ttkbootstrap.constants import * 
from ttkbootstrap import dialogs, Tableview
from controller.paciente_controller import PacienteController 
from controller.plano_controller import PlanoController 
 
class PacienteView: 
    def __init__(self, parent): 
        self.parent = parent 
        self.id_selecionado = None  # guarda ID ao selecionar na tabela 
        self._criar_tela() 
 
    def _criar_tela(self): 
        # ─── TÍTULO ─────────────────────────────────── 
        tb.Label( 
            self.parent, 
            text='👤  Cadastro de Pacientes', 
            font=('Arial', 16, 'bold') 
        ).pack(anchor='w', pady=(0, 5)) 
        tb.Separator(self.parent, bootstyle='primary').pack(fill='x', 
pady=(0,15)) 
 
        # ─── NOTEBOOK (abas: Cadastrar | Listar) ────── 
        notebook = tb.Notebook(self.parent, bootstyle='primary') 
        notebook.pack(fill='both', expand=True) 
 # Aba 1: Formulário de cadastro 
        aba_form = tb.Frame(notebook, padding=15) 
        notebook.add(aba_form, text='  ➕  Novo Paciente  ') 
        self._criar_formulario(aba_form) 
 
        # Aba 2: Listagem 
        aba_lista = tb.Frame(notebook, padding=15) 
        notebook.add(aba_lista, text='  📋  Lista de Pacientes  ') 
        self._criar_listagem(aba_lista) 
 
    def _criar_formulario(self, parent): 
        """Formulário de cadastro de paciente.""" 
        # Frame principal do formulário 
        frame = tk.LabelFrame(
            parent, text=' Dados do Paciente ', padx=20, pady=20
        )
        frame.pack(fill='x', pady=10) 
 
        # ─── Linha 1: Nome (ocupa toda a largura) ───── 
        tb.Label(frame, text='Nome Completo *', font=('Arial', 10, 
'bold')).grid( 
            row=0, column=0, columnspan=2, sticky='w', padx=5, pady=(5,2) 
        ) 
        self.entry_nome = tb.Entry(frame, width=60, bootstyle='primary', 
font=('Arial',11)) 
        self.entry_nome.grid(row=1, column=0, columnspan=2, padx=5, pady=5, 
sticky='ew') 
 
        # ─── Linha 2: CPF e Telefone ───────────────── 
        tb.Label(frame, text='CPF *', font=('Arial', 10, 'bold')).grid( 
            row=2, column=0, sticky='w', padx=5, pady=(10,2) 
        ) 
        self.entry_cpf = tb.Entry(frame, width=20, bootstyle='primary', 
font=('Arial',11)) 
        self.entry_cpf.grid(row=3, column=0, padx=5, pady=5, sticky='ew') 
 
        tb.Label(frame, text='Telefone', font=('Arial', 10, 'bold')).grid( 
            row=2, column=1, sticky='w', padx=5, pady=(10,2) 
        ) 
        self.entry_tel = tb.Entry(frame, width=20, bootstyle='info', 
font=('Arial',11)) 
        self.entry_tel.grid(row=3, column=1, padx=5, pady=5, sticky='ew') 
 
        # ─── Linha 3: Email e Plano ────────────────── 
        tb.Label(frame, text='E-mail', font=('Arial', 10, 'bold')).grid( 
            row=4, column=0, sticky='w', padx=5, pady=(10,2) 
        ) 
        self.entry_email = tb.Entry(frame, width=35, bootstyle='info', 
font=('Arial',11)) 
        self.entry_email.grid(row=5, column=0, padx=5, pady=5, sticky='ew') 
        tb.Label(frame, text='Plano de Saúde', font=('Arial', 10, 
'bold')).grid( 
            row=4, column=1, sticky='w', padx=5, pady=(10,2) 
        ) 
 
        # Combobox para selecionar o plano 
        self.combo_plano = tb.Combobox( 
            frame, state='readonly', bootstyle='info', font=('Arial',11), 
width=25 
        ) 
        self.combo_plano.grid(row=5, column=1, padx=5, pady=5, sticky='ew') 
        self._carregar_planos()  # popula o combobox 
 
        # Expande as colunas igualmente 
        frame.columnconfigure(0, weight=1) 
        frame.columnconfigure(1, weight=1) 
 
        # ─── Botões ─────────────────────────────────── 
        frame_btn = tb.Frame(parent) 
        frame_btn.pack(fill='x', pady=15) 
 
        tb.Button( 
            frame_btn, text='✅  Salvar Paciente', bootstyle='success', 
            width=20, command=self._salvar 
        ).pack(side='left', padx=5, ipady=5) 
 
        tb.Button( 
            frame_btn, text='🗑️  Limpar Campos', bootstyle='secondary', 
            width=18, command=self._limpar 
        ).pack(side='left', padx=5, ipady=5) 
 
    def _carregar_planos(self): 
        """Popula o Combobox com os planos do banco.""" 
        self.planos_lista = PlanoController.listar() 
        nomes = [p['nome'] for p in self.planos_lista] 
        self.combo_plano['values'] = nomes 
        if nomes: 
            self.combo_plano.current(0)  # seleciona o primeiro 
 
    def _get_plano_id(self): 
        """Retorna o ID do plano selecionado no combobox.""" 
        idx = self.combo_plano.current() 
        if idx >= 0 and self.planos_lista: 
            return self.planos_lista[idx]['id'] 
        return None 
 
    def _salvar(self): 
        """Coleta os dados e chama o controller para salvar.""" 
        nome     = self.entry_nome.get().strip() 
        cpf      = self.entry_cpf.get().strip() 
        telefone = self.entry_tel.get().strip() 
        email    = self.entry_email.get().strip() 
        plano_id = self._get_plano_id() 
         # Chama o controller – ele faz a validação 
        ok, mensagem = PacienteController.salvar(nome, cpf, telefone, 
email, plano_id) 
 
        if ok: 
            dialogs.Messagebox.show_info(mensagem, 'Sucesso') 
            self._limpar() 
        else: 
            dialogs.Messagebox.show_error(mensagem, 'Erro') 
 
    def _limpar(self): 
        """Limpa todos os campos do formulário.""" 
        self.entry_nome.delete(0, 'end') 
        self.entry_cpf.delete(0, 'end') 
        self.entry_tel.delete(0, 'end') 
        self.entry_email.delete(0, 'end') 
        self.entry_nome.focus()  # foca no primeiro campo 
 
    def _criar_listagem(self, parent): 
        """Aba de listagem de pacientes com tabela.""" 
        # Botão para atualizar a lista 
        tb.Button( 
            parent, text='🔄  Atualizar Lista', bootstyle='info-outline', 
            command=self._atualizar_tabela 
        ).pack(anchor='e', pady=(0,10)) 
 
        # Container da tabela 
        self.frame_tabela = tb.Frame(parent) 
        self.frame_tabela.pack(fill='both', expand=True) 
 
        self._atualizar_tabela() 
 
    def _atualizar_tabela(self): 
        """Busca dados no banco e atualiza a tabela.""" 
        # Limpa a tabela anterior 
        for w in self.frame_tabela.winfo_children(): 
            w.destroy() 
 
        # Busca os dados via controller 
        dados = PacienteController.listar() 
 
        # Define colunas 
        colunas = [ 
            {'text': 'ID',       'stretch': False, 'width': 50}, 
            {'text': 'Nome',     'stretch': True,  'width': 200}, 
            {'text': 'CPF',      'stretch': False, 'width': 130}, 
            {'text': 'Telefone', 'stretch': False, 'width': 120}, 
            {'text': 'E-mail',   'stretch': True,  'width': 180}, 
            {'text': 'Plano',    'stretch': True,  'width': 130}, 
        ] 
 
        # Prepara as linhas
        linhas = [( 
            p['id'], p['nome'], p['cpf'], 
            p.get('telefone',''), p.get('email',''), 
            p.get('nome_plano', 'Particular') 
        ) for p in dados] 
 
        Tableview( 
            master=self.frame_tabela, 
            coldata=colunas, 
            rowdata=linhas, 
            paginated=True, 
            searchable=True, 
            bootstyle='primary', 
            stripecolor=('#f0f8ff', None) 
        ).pack(fill='both', expand=True) 
