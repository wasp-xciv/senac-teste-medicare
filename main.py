# Forma de executar: python main.py 
 
from view.login_view import LoginView 
 
if __name__ == '__main__': 
    # Ponto de entrada do sistema 
    app = LoginView() 
    app.iniciar()