# controller/agendamento_controller.py 
from model.agendamento_model import AgendamentoModel 
from datetime import datetime 
 
class AgendamentoController: 
 
    @staticmethod 
    def agendar(paciente_id, medico_id, data_str, hora_str, observacao=''): 
        """ 
        Valida e cria um agendamento. 
        data_str: '25/12/2025'  (formato brasileiro) 
        hora_str: '14:30' 
        """ 
 
        # Validação dos campos obrigatórios 
        if not paciente_id: 
            return False, 'Selecione um paciente!' 
        if not medico_id: 
            return False, 'Selecione um médico!' 
        if not data_str: 
            return False, 'Informe a data!' 
        if not hora_str: 
            return False, 'Informe o horário!' 
 
        # Converte data e hora para o formato do MySQL 
        try: 
            data_hora = datetime.strptime( 
                f'{data_str} {hora_str}', 
                '%d/%m/%Y %H:%M' 
            ) 
        except ValueError: 
            return False, 'Data ou hora inválida! Use DD/MM/AAAA e HH:MM' 
 
        # Verifica se a consulta é no futuro 
        if data_hora <= datetime.now(): 
            return False, 'Não é possível agendar para datas passadas!' 
 
        # Verifica conflito de horário do médico 
        if AgendamentoModel.verificar_conflito(medico_id, data_hora): 
            return False, 'Médico já tem consulta neste horário!' 
 
        try: 
            AgendamentoModel.inserir(paciente_id, medico_id, data_hora, 
observacao) 
            return True, 'Consulta agendada com sucesso! ✅' 
        except Exception as e: 
            return False, f'Erro ao agendar: {e}' 
 
    @staticmethod 
    def listar(): 
        return AgendamentoModel.listar_todos() 