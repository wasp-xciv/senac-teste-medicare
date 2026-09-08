# view/inicio_view.py 
import ttkbootstrap as tb 
from ttkbootstrap.constants import * 
from datetime import datetime 
from controller.paciente_controller import PacienteController 
from controller.medico_controller import MedicoController 
from controller.agendamento_controller import AgendamentoController 
 
class InicioView: 
    def __init__(self, parent): 
        self.parent = parent 
        self._criar_dashboard() 
 
    def _criar_dashboard(self): 
        """Painel inicial com resumo do sistema.""" 
        # Saudação 
        hora = datetime.now().hour 
        if hora < 12:   saudacao = 'Bom dia' 
        elif hora < 18: saudacao = 'Boa tarde' 
        else:           saudacao = 'Boa noite' 
        tb.Label( 
            self.parent, 
            text=f'{saudacao}! Bem-vindo ao MediCare+', 
            font=('Arial', 18, 'bold') 
        ).pack(anchor='w', pady=(0,5)) 
        tb.Separator(self.parent, bootstyle='primary').pack(fill='x', 
pady=(0,25)) 
 
        # ─── Cards de Resumo ────────────────────────── 
        frame_cards = tb.Frame(self.parent) 
        frame_cards.pack(fill='x', pady=10) 
 
        # Busca totais do banco 
        total_pac  = len(PacienteController.listar()) 
        total_med  = len(MedicoController.listar()) 
        total_age  = len(AgendamentoController.listar()) 
 
        # Função para criar cada card 
        def card(parent, icone, titulo, valor, cor): 
            f = tb.Frame(parent, bootstyle=cor, padding=20) 
            f.pack(side='left', fill='both', expand=True, padx=8) 
            tb.Label(f, text=icone, font=('Arial',30), bootstyle=f'inverse {cor}').pack() 
            tb.Label(f, text=str(valor), font=('Arial',32,'bold'), 
bootstyle=f'inverse-{cor}').pack() 
            tb.Label(f, text=titulo, font=('Arial',12), 
bootstyle=f'inverse-{cor}').pack() 
 
        card(frame_cards, '👤', 'Pacientes',    total_pac, 'primary') 
        card(frame_cards, '👨‍⚕️', 'Médicos',      total_med, 'success') 
        card(frame_cards, '📅', 'Agendamentos', total_age, 'info') 
 
        # Dica do dia 
        tb.Label( 
            self.parent, 
            text='💡  Use o menu lateral para navegar entre as telas.', 
            font=('Arial', 11), 
            foreground='gray' 
        ).pack(anchor='w', pady=30) 
