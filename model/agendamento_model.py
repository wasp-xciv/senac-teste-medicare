# model/agendamento_model.py 
from database.conexao import obter_conexao 
 
class AgendamentoModel: 
 
    @staticmethod 
    def inserir(paciente_id, medico_id, data_hora, observacao=''): 
        conn = obter_conexao() 
        try: 
            with conn.cursor() as cursor: 
                sql = """ 
                    INSERT INTO agendamentos 
                        (paciente_id, medico_id, data_hora, observacao) 
                    VALUES (%s, %s, %s, %s) 
                """ 
                cursor.execute(sql, (paciente_id, medico_id, data_hora, 
observacao)) 
            conn.commit() 
            return True 
        finally: 
            conn.close() 
 
    @staticmethod 
    def listar_todos(): 
        """Lista todos os agendamentos com JOIN nas tabelas 
relacionadas.""" 
        conn = obter_conexao() 
        try: 
            with conn.cursor() as cursor: 
                sql = """ 
                    SELECT 
                        a.id, 
                        p.nome AS paciente, 
                        m.nome AS medico, 
                        m.especialidade, 
                        a.data_hora, 
                        a.status, 
                        a.observacao 
                    FROM agendamentos a 
                    JOIN pacientes p ON a.paciente_id = p.id 
                    JOIN medicos   m ON a.medico_id   = m.id ORDER BY a.data_hora DESC 
                """ 
                cursor.execute(sql) 
                return cursor.fetchall() 
        finally: 
            conn.close() 
 
    @staticmethod 
    def verificar_conflito(medico_id, data_hora): 
        """Verifica se o médico já tem consulta neste horário.""" 
        conn = obter_conexao() 
        try: 
            with conn.cursor() as cursor: 
                sql = """ 
                    SELECT COUNT(*) AS total FROM agendamentos 
                    WHERE medico_id = %s 
                      AND data_hora = %s 
                      AND status = 'agendado' 
                """ 
                cursor.execute(sql, (medico_id, data_hora)) 
                resultado = cursor.fetchone() 
                return resultado['total'] > 0  # True se tiver conflito 
        finally: 
            conn.close()
