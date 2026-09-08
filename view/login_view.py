# view/login_view.py 
import ttkbootstrap as tb 
from ttkbootstrap.constants import * 
from ttkbootstrap import dialogs 
 
class LoginView: 
    def __init__(self): 
        self.app = tb.Window(themename='litera') #temas: darkly, flatly, superhero, journal, litera, cosmo, pulse, simplex, yeti, sandstone, lumen, minty, morph, solar, cyborg, darkly
        self.app.title('MediCare+ – Login') 
        self.app.geometry('420x520') 
        self.app.resizable(False, False) 
        self._centralizar_janela(420, 520) 
        self._criar_tela() 
 
    def _centralizar_janela(self, w, h): 
        """Coloca a janela no centro da tela.""" 
        screen_w = self.app.winfo_screenwidth() 
        screen_h = self.app.winfo_screenheight() 
        x = (screen_w // 2) - (w // 2) 
        y = (screen_h // 2) - (h // 2) 
        self.app.geometry(f'{w}x{h}+{x}+{y}') 
 
    def _criar_tela(self): 
        # ─── CABEÇALHO AZUL ─────────────────────────── 
        header = tb.Frame(self.app, bootstyle='primary', padding=30) 
        header.pack(fill='x')
        tb.Label( 
            header, 
            text='🏥', 
            font=('Arial', 40), 
            bootstyle='inverse-primary' 
        ).pack() 
 
        tb.Label( 
            header, 
            text='MediCare+', 
            font=('Arial', 22, 'bold'), 
            bootstyle='inverse-primary' 
        ).pack() 
 
        tb.Label( 
            header, 
            text='Sistema de Agendamento Médico', 
            font=('Arial', 10), 
            bootstyle='inverse-primary' 
        ).pack() 
 
        # ─── FORMULÁRIO DE LOGIN ────────────────────── 
        frame_form = tb.Frame(self.app, padding=30) 
        frame_form.pack(fill='both', expand=True) 
 
        tb.Label(frame_form, text='Usuário', font=('Arial', 
11)).pack(anchor='w', pady=(10,2)) 
        self.entry_usuario = tb.Entry( 
            frame_form, width=30, bootstyle='primary', font=('Arial', 12) 
        ) 
        self.entry_usuario.pack(fill='x', ipady=5) 
        self.entry_usuario.insert(0, 'admin')  # valor padrão para teste 
 
        tb.Label(frame_form, text='Senha', font=('Arial', 
11)).pack(anchor='w', pady=(15,2)) 
        self.entry_senha = tb.Entry( 
            frame_form, width=30, bootstyle='primary', 
            font=('Arial', 12), show='●'   # oculta a senha 
        ) 
        self.entry_senha.pack(fill='x', ipady=5) 
        self.entry_senha.insert(0, '1234') 
 
        # Bind Enter para fazer login 
        self.entry_senha.bind('<Return>', lambda e: self._fazer_login()) 
 
        tb.Button( 
            frame_form, 
            text='🔐  Entrar', 
            bootstyle='primary', 
            width=20, 
            command=self._fazer_login 
        ).pack(pady=20, ipady=8) 
    def _fazer_login(self): 
        usuario = self.entry_usuario.get() 
        senha   = self.entry_senha.get() 

        # Validação simples (em sistema real, verificar no banco!) 
        if usuario == 'admin' and senha == '1234':
            try:
                self.app.destroy()  # oculta a janela de login sem destruir o loop principal
                from view.main_view import MainView
                sistema = MainView()
                sistema.app.focus_force()
            except Exception as exc:
                self.app.deiconify()
                dialogs.Messagebox.show_error(
                    f'Erro ao abrir o sistema: {exc}',
                    'Erro ao iniciar'
                )
        else:
            dialogs.Messagebox.show_error(
                'Usuário ou senha incorretos!',
                'Erro de Login'
            )
            self.entry_senha.delete(0, 'end')  # limpa a senha
 
    def iniciar(self): 
        self.app.mainloop() 