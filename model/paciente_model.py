# model/paciente_model.py 
from database.conexao import obter_conexao 
 
class PacienteModel: 
 
    @staticmethod # método estático, pode ser chamado sem criar uma instância da classe
    def inserir(nome, cpf, telefone, email, plano_id): 
        """Insere um novo paciente no banco de dados.""" 
        conn = obter_conexao() 
        try: 
            with conn.cursor() as cursor: 
                sql = """ 
                    INSERT INTO pacientes (nome, cpf, telefone, email,plano_id) 
 VALUES (%s, %s, %s, %s, %s) 
                """ 
                # %s são placeholders de segurança (evita SQL Injection!) 
                cursor.execute(sql, (nome, cpf, telefone, email, plano_id)) 
            conn.commit()   # confirma a gravação no banco 
            return True 
        except Exception as e: 
            conn.rollback()  # desfaz em caso de erro 
            raise e # re-levanta a exceção para ser tratada na rota
        finally: 
            conn.close()     # SEMPRE feche a conexão 
 
    @staticmethod 
    def listar_todos(): 
        """Retorna todos os pacientes com nome do plano.""" 
        conn = obter_conexao() 
        try: 
            with conn.cursor() as cursor: 
                sql = """ 
                    SELECT p.*, pl.nome AS nome_plano 
                    FROM pacientes p 
                    LEFT JOIN planos pl ON p.plano_id = pl.id 
                    ORDER BY p.nome 
                """ 
                cursor.execute(sql) 
                return cursor.fetchall()  # retorna lista de dicionários 
        finally: 
            conn.close() 
 
    @staticmethod 
    def buscar_por_id(paciente_id): 
        """Retorna um paciente específico pelo ID.""" 
        conn = obter_conexao() 
        try: 
            with conn.cursor() as cursor: 
                cursor.execute('SELECT * FROM pacientes WHERE id = %s', 
(paciente_id,)) 
                return cursor.fetchone()  # retorna apenas um registro 
        finally: 
            conn.close() 
 
    @staticmethod 
    def atualizar(paciente_id, nome, cpf, telefone, email, plano_id): 
        """Atualiza os dados de um paciente.""" 
        conn = obter_conexao() 
        try: 
            with conn.cursor() as cursor: 
                sql = """ 
                    UPDATE pacientes 
                    SET nome=%s, cpf=%s, telefone=%s, email=%s, plano_id=%s 
                    WHERE id = %s 
                """ 
                cursor.execute(sql, (nome, cpf, telefone, email, plano_id, 
paciente_id))
                conn.commit() 
            return True 
        except Exception as e: 
            conn.rollback() 
            raise e 
        finally: 
            conn.close() 
 
    @staticmethod 
    def deletar(paciente_id): 
        """Remove um paciente do banco.""" 
        conn = obter_conexao() 
        try: 
            with conn.cursor() as cursor: 
                cursor.execute('DELETE FROM pacientes WHERE id = %s', 
(paciente_id,)) 
            conn.commit() 
        finally: 
            conn.close() 