# view/main_view.py 
import ttkbootstrap as tb 
from ttkbootstrap.constants import * 
 
class MainView: 
    def __init__(self): 
        # Cria a janela principal com tema médico 
        self.app = tb.Window(themename='flatly') 
        self.app.title('🏥 MediCare+ – Sistema de Agendamento') 
        self.app.geometry('1100x680') 
        self.app.resizable(True, True) 
        self._hora_job = None
        self.app.protocol('WM_DELETE_WINDOW', self.fechar)

        self._criar_header() 
        self._criar_layout() 
        self._criar_sidebar() 
        self._criar_area_conteudo() 
 
        # Mostra tela inicial ao abrir 
        self.mostrar_inicio() 
 
    def _criar_header(self): 
        """Barra superior com nome do sistema.""" 
        header = tb.Frame(self.app, bootstyle='primary', padding=(10, 8)) 
        header.pack(fill='x', side='top') 
 
        tb.Label( 
            header, 
            text='🏥  MediCare+ – Sistema de Agendamento de Consultas', 
            font=('Arial', 14, 'bold'), 
            bootstyle='inverse-primary'  # texto branco no fundo azul 
        ).pack(side='left') 
 
        # Mostra data/hora no canto direito 
        self.label_hora = tb.Label( 
            header, 
            text='',
            font=('Arial', 11), 
            bootstyle='inverse-primary' 
        ) 
        self.label_hora.pack(side='right', padx=10) 
        self._atualizar_hora()  # inicia o relógio 
 
    def _atualizar_hora(self): 
        """Atualiza o relógio a cada segundo.""" 
        if not self.app.winfo_exists() or not self.label_hora.winfo_exists():
            return

        from datetime import datetime 
        agora = datetime.now().strftime('%d/%m/%Y  %H:%M:%S') 
        self.label_hora.config(text=agora) 
        # Agenda nova atualização em 1 segundo (1000ms) 
        self._hora_job = self.app.after(1000, self._atualizar_hora)

    def fechar(self):
        """Encerra a aplicação limpando callbacks pendentes."""
        if self._hora_job is not None:
            try:
                self.app.after_cancel(self._hora_job)
            except Exception:
                pass
            self._hora_job = None
        self.app.destroy()
 
    def _criar_layout(self): 
        """Frame principal que divide sidebar e conteúdo.""" 
        self.frame_main = tb.Frame(self.app) 
        self.frame_main.pack(fill='both', expand=True) 
 
    def _criar_sidebar(self): 
        """Menu lateral com botões de navegação.""" 
        sidebar = tb.Frame( 
            self.frame_main, 
            bootstyle='light', 
            width=200, 
            padding=(5, 10) 
        ) 
        sidebar.pack(side='left', fill='y') 
        sidebar.pack_propagate(False)  # impede que o frame encolha 
 
        # Logo/título do menu 
        tb.Label( 
            sidebar, 
            text='MENU', 
            font=('Arial', 10, 'bold'), 
            foreground='gray' 
        ).pack(pady=(10, 5)) 
 
        tb.Separator(sidebar).pack(fill='x', pady=5) 
 
        # Definição dos botões do menu 
        # (texto, ícone, função a chamar) 
        menu_items = [ 
            ('🏠  Início',     self.mostrar_inicio), 
            ('👤  Pacientes',  self.mostrar_pacientes), 
            ('👨‍⚕️  Médicos',    self.mostrar_medicos), 
            ('💊  Planos',     self.mostrar_planos), 
            ('📅  Agendamentos', self.mostrar_agendamentos), 
        ] 
 
        # Cria cada botão do menu 
        self.botoes_menu = []
        for texto, comando in menu_items: 
            btn = tb.Button( 
                sidebar, 
                text=texto, 
                bootstyle='outline-primary',  # borda azul, fundo branco 
                width=20, 
                command=comando 
            ) 
            btn.pack(pady=3, padx=5, fill='x') 
            self.botoes_menu.append(btn) 
 
        # Separador e botão de sair 
        tb.Separator(sidebar).pack(fill='x', pady=15) 
        tb.Button( 
            sidebar, 
            text='🚪  Sair', 
            bootstyle='danger-outline', 
            width=20, 
            command=self.app.quit 
        ).pack(pady=3, padx=5, fill='x') 
 
    def _criar_area_conteudo(self): 
        """Área onde as telas aparecem.""" 
        self.frame_conteudo = tb.Frame( 
            self.frame_main, 
            bootstyle='default', 
            padding=20 
        ) 
        self.frame_conteudo.pack(side='left', fill='both', expand=True) 
 
    def _limpar_conteudo(self): 
        """Remove todos os widgets da área de conteúdo.""" 
        for widget in self.frame_conteudo.winfo_children(): 
            widget.destroy() 
 
    # ─── FUNÇÕES DE NAVEGAÇÃO ───────────────────────── 
    def mostrar_inicio(self): 
        self._limpar_conteudo()
        try:
            from view.inicio_view import InicioView
            InicioView(self.frame_conteudo)
        except Exception as exc:
            tb.Label(
                self.frame_conteudo,
                text=f'Erro ao carregar a tela inicial: {exc}',
                font=('Arial', 11),
                foreground='red'
            ).pack(anchor='w')
 
    def mostrar_pacientes(self): 
        self._limpar_conteudo() 
        from view.paciente_view import PacienteView 
        PacienteView(self.frame_conteudo) 
 
    def mostrar_medicos(self): 
        self._limpar_conteudo() 
        from view.medico_view import MedicoView 
        MedicoView(self.frame_conteudo) 
 
    def mostrar_planos(self): 
        self._limpar_conteudo() 
        from view.plano_view import PlanoView 
        PlanoView(self.frame_conteudo) 
 
    def mostrar_agendamentos(self): 
        self._limpar_conteudo() 
        from view.agendamento_view import AgendamentoView 
        AgendamentoView(self.frame_conteudo) 
 
    def iniciar(self): 
        self.app.mainloop()
