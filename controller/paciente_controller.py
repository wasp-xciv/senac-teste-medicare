# controller/paciente_controller.py 
from model.paciente_model import PacienteModel 
 
class PacienteController: 
 
    @staticmethod 
    def salvar(nome, cpf, telefone, email, plano_id): 
        """Valida os dados e chama o Model para inserir.""" 
 
        # ─── VALIDAÇÕES ────────────────────────────── 
        if not nome.strip(): 
            return False, 'Nome do paciente é obrigatório!' 
 
        if not cpf.strip(): 
            return False, 'CPF é obrigatório!' 
 
        if len(cpf.replace('.','').replace('-','')) != 11: 
            return False, 'CPF deve ter 11 dígitos!' 
        # ───────────────────────────────────────────── 
        try: 
            PacienteModel.inserir(nome, cpf, telefone, email, plano_id) 
            return True, 'Paciente cadastrado com sucesso!' 
        except Exception as e: 
            return False, f'Erro ao cadastrar: {e}' 
 
    @staticmethod 
    def listar(): 
        """Retorna todos os pacientes.""" 
        return PacienteModel.listar_todos() 
 
    @staticmethod 
    def atualizar(paciente_id, nome, cpf, telefone, email, plano_id): 
        if not nome.strip(): 
            return False, 'Nome é obrigatório!' 
        try: 
            PacienteModel.atualizar(paciente_id, nome, cpf, telefone, 
email, plano_id) 
            return True, 'Paciente atualizado com sucesso!' 
        except Exception as e: 
            return False, f'Erro: {e}'