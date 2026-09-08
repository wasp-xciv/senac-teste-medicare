# controller/medico_controller.py 
from model.medico_model import MedicoModel 
 
class MedicoController: 
 
    @staticmethod 
    def salvar(nome, especialidade, crm): 
        if not nome.strip(): 
            return False, 'Nome do médico é obrigatório!' 
        if not especialidade: 
            return False, 'Especialidade é obrigatória!' 
        if not crm.strip() or len(crm.strip()) < 5: 
            return False, 'CRM inválido! Mínimo 5 caracteres.' 
        try: 
            MedicoModel.inserir(nome, especialidade, crm) 
            return True, f'Médico {nome} cadastrado com sucesso!' 
        except ValueError as e: 
            return False, str(e) 
        except Exception as e: 
            return False, f'Erro: {e}' 
 
    @staticmethod 
    def listar(): 
        return MedicoModel.listar_todos() 