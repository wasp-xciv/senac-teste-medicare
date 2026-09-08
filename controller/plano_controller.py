# controller/plano_controller.py 
from model.plano_model import PlanoModel 
 
class PlanoController: 
 
    @staticmethod 
    def salvar(nome, codigo): 
        if not nome.strip(): 
            return False, 'Nome do plano é obrigatório!' 
        if not codigo.strip(): 
            return False, 'Código do plano é obrigatório!' 
        try: 
            PlanoModel.inserir(nome, codigo) 
            return True, f'Plano "{nome}" cadastrado com sucesso!' 
        except Exception as e: 
            return False, f'Erro: {e}' 
 
    @staticmethod 
    def listar(): 
        return PlanoModel.listar_todos()    