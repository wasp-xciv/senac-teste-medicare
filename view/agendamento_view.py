# view/agendamento_view.py 
import tkinter as tk
import ttkbootstrap as tb 
from ttkbootstrap.constants import * 
from ttkbootstrap import dialogs, Tableview
from ttkbootstrap.dialogs import Querybox
from datetime import datetime
from controller.agendamento_controller import AgendamentoController 
from controller.paciente_controller import PacienteController 
from controller.medico_controller import MedicoController 
 
class AgendamentoView: 
    def __init__(self, parent): 
        self.parent = parent 
        self.pacientes = []  # lista de pacientes do banco 
        self.medicos   = []  # lista de médicos do banco 
        self._criar_tela() 
 
    def _criar_tela(self): 
        tb.Label( 
            self.parent, text='📅  Agendamento de Consultas', 
            font=('Arial', 16, 'bold') 
        ).pack(anchor='w', pady=(0,5)) 
        tb.Separator(self.parent, bootstyle='info').pack(fill='x', 
pady=(0,15)) 
 
        notebook = tb.Notebook(self.parent, bootstyle='info') 
        notebook.pack(fill='both', expand=True) 
 
        aba_form = tb.Frame(notebook, padding=15) 
        notebook.add(aba_form, text='  📅  Nova Consulta  ') 
        self._criar_formulario(aba_form) 
 
        aba_lista = tb.Frame(notebook, padding=15) 
        notebook.add(aba_lista, text='  📋  Todos os Agendamentos  ') 
        self._criar_listagem(aba_lista) 
 
    def _criar_formulario(self, parent): 
        # ─── Frame: Selecionar Paciente ─────────────── 
        frame_pac = tk.LabelFrame(
            parent, text=' 👤 Paciente ', padx=15, pady=15
        )
        frame_pac.pack(fill='x', pady=5) 
 
        tb.Label(frame_pac, text='Selecione o Paciente *', 
font=('Arial',10,'bold')).pack(anchor='w') 
        self.combo_pac = tb.Combobox( 
            frame_pac, state='readonly', bootstyle='primary', 
font=('Arial',11), width=50 
        ) 
        self.combo_pac.pack(fill='x', pady=5) 
        self._carregar_pacientes() 
 
        # ─── Frame: Selecionar Médico ───────────────── 
        frame_med = tk.LabelFrame(
            parent, text=' 👨‍⚕️ Médico ', padx=15, pady=15
        )
        frame_med.pack(fill='x', pady=5)
        tb.Label(frame_med, text='Selecione o Médico *', 
font=('Arial',10,'bold')).pack(anchor='w') 
        self.combo_med = tb.Combobox( 
            frame_med, state='readonly', bootstyle='success', 
font=('Arial',11), width=50 
        ) 
        self.combo_med.pack(fill='x', pady=5) 
        self._carregar_medicos() 
 
        # ─── Frame: Data e Horário ──────────────────── 
        frame_dt = tk.LabelFrame(
            parent, text=' 📅 Data e Horário ', padx=15, pady=15
        )
        frame_dt.pack(fill='x', pady=5) 
 
# Data com calendário (seleção por popup) 
        tb.Label(frame_dt, text='Data da Consulta *', 
font=('Arial',10,'bold')).grid( 
            row=0, column=0, sticky='w', padx=5, pady=(5,2) 
        ) 
        self.date_entry = tb.Entry(
            frame_dt, width=20, bootstyle='info', font=('Arial', 11)
        )
        self.date_entry.grid(row=1, column=0, padx=(5, 0), pady=5, sticky='ew')
        self.date_entry.insert(0, datetime.now().strftime('%d/%m/%Y'))

        tb.Button(
            frame_dt,
            text='📅',
            bootstyle='info-outline',
            width=3,
            command=self._abrir_calendario
        ).grid(row=1, column=1, padx=(5, 5), pady=5, sticky='w')

        # Horário com Combobox (horários disponíveis) 
        tb.Label(frame_dt, text='Horário *', 
font=('Arial',10,'bold')).grid( 
            row=0, column=2, sticky='w', padx=5, pady=(5,2) 
        ) 
        horarios = [f'{h:02d}:{m:02d}' 
                    for h in range(7, 19)   # das 07h às 18h 
                    for m in [0, 30]]        # a cada 30 minutos 
        self.combo_hora = tb.Combobox( 
            frame_dt, values=horarios, state='readonly', 
            bootstyle='info', width=10 
        ) 
        self.combo_hora.grid(row=1, column=2, padx=5, pady=5, sticky='ew') 
        self.combo_hora.current(4)  # padrão: 09:00 
 
        frame_dt.columnconfigure(0, weight=2) 
        frame_dt.columnconfigure(1, weight=0) 
        frame_dt.columnconfigure(2, weight=1) 
 
        # Observação 
        tb.Label(frame_dt, text='Observações', 
font=('Arial',10,'bold')).grid( 
            row=2, column=0, columnspan=2, sticky='w', padx=5, pady=(10,2) 
        ) 
        self.text_obs = tb.Text( frame_dt, height=3, width=60, font=('Arial',10) 
        ) 
        self.text_obs.grid(row=3, column=0, columnspan=2, padx=5, pady=5, 
sticky='ew') 
 
        # ─── Botão Agendar ──────────────────────────── 
        tb.Button( 
            parent, 
            text='✅  CONFIRMAR AGENDAMENTO', 
            bootstyle='success', 
            width=30, 
            command=self._agendar 
        ).pack(pady=20, ipady=8) 
 
    def _carregar_pacientes(self): 
        """Popula o combobox com os pacientes do banco.""" 
        self.pacientes = PacienteController.listar() 
        nomes = [f"{p['id']} – {p['nome']}" for p in self.pacientes] 
        self.combo_pac['values'] = nomes 
        if nomes: self.combo_pac.current(0) 
 
    def _carregar_medicos(self): 
        """Popula o combobox com os médicos do banco.""" 
        self.medicos = MedicoController.listar() 
        nomes = [f"{m['nome']} – {m['especialidade']}" for m in 
self.medicos] 
        self.combo_med['values'] = nomes 
        if nomes: self.combo_med.current(0) 
 
    def _abrir_calendario(self):
        """Abre um seletor de data estável via Querybox."""
        valor_atual = self.date_entry.get().strip()
        try:
            data_inicial = datetime.strptime(valor_atual, '%d/%m/%Y').date() if valor_atual else datetime.now().date()
        except ValueError:
            data_inicial = datetime.now().date()

        pai = self.parent.winfo_toplevel() if hasattr(self.parent, 'winfo_toplevel') else self.parent
        nova_data = Querybox.get_date(
            parent=pai,
            title='Selecione a data da consulta',
            startdate=data_inicial,
            firstweekday=6,
            bootstyle='info',
        )
        if nova_data:
            self.date_entry.delete(0, END)
            self.date_entry.insert(0, nova_data.strftime('%d/%m/%Y'))

    def _agendar(self): 
        """Coleta dados e chama o controller para agendar.""" 
        # Pega IDs selecionados nos comboboxes 
        idx_pac = self.combo_pac.current() 
        idx_med = self.combo_med.current() 
 
        if idx_pac < 0 or not self.pacientes: 
            dialogs.Messagebox.show_error('Selecione um paciente!', 
'Atenção') 
            return 
        if idx_med < 0 or not self.medicos: 
            dialogs.Messagebox.show_error('Selecione um médico!', 
'Atenção') 
            return 
 
        paciente_id = self.pacientes[idx_pac]['id'] 
        medico_id   = self.medicos[idx_med]['id'] 
 
        # Pega data e hora selecionadas 
        data_str = self.date_entry.get() 
        hora_str = self.combo_hora.get() 
        obs      = self.text_obs.get('1.0', 'end').strip() 
 
        # Chama o controller – ele valida e salva  
        ok, msg = AgendamentoController.agendar(paciente_id, medico_id, data_str, hora_str, obs) 
 
        if ok: 
            dialogs.Messagebox.show_info(msg, '🏥 Agendamento Confirmado') 
            self.text_obs.delete('1.0', 'end') 
        else: 
            dialogs.Messagebox.show_error(msg, '❌ Erro no Agendamento') 
 
    def _criar_listagem(self, parent): 
        """Aba com todos os agendamentos.""" 
        frame_topo = tb.Frame(parent) 
        frame_topo.pack(fill='x', pady=(0,10)) 
 
        tb.Label(frame_topo, text='Todos os Agendamentos', 
font=('Arial',13,'bold')).pack(side='left') 
        tb.Button( 
            frame_topo, text='🔄  Atualizar', 
            bootstyle='info-outline', command=self._atualizar_tabela 
        ).pack(side='right') 
 
        self.frame_tab = tb.Frame(parent) 
        self.frame_tab.pack(fill='both', expand=True) 
        self._atualizar_tabela() 
 
    def _atualizar_tabela(self): 
        for w in self.frame_tab.winfo_children(): w.destroy() 
        dados = AgendamentoController.listar() 
        colunas = [ 
            {'text': 'ID',          'stretch': False, 'width': 50}, 
            {'text': 'Paciente',    'stretch': True,  'width': 180}, 
            {'text': 'Médico',      'stretch': True,  'width': 180}, 
            {'text': 'Especialidade','stretch': True, 'width': 140}, 
            {'text': 'Data/Hora',   'stretch': False, 'width': 150}, 
            {'text': 'Status',      'stretch': False, 'width': 100}, 
        ] 
        linhas = [( 
            a['id'], a['paciente'], a['medico'], 
            a['especialidade'], 
            str(a['data_hora']).replace('T',' ')[:16], 
            a['status'].upper() 
        ) for a in dados] 
        Tableview( 
            master=self.frame_tab, coldata=colunas, rowdata=linhas, 
            paginated=True, searchable=True, bootstyle='info', 
            stripecolor=('#e8f4f8', None) 
        ).pack(fill='both', expand=True) 