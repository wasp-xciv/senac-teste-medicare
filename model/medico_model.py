# model/medico_model.py 
import pymysql
from database.conexao import obter_conexao 
 
class MedicoModel: 
 
    @staticmethod 
    def inserir(nome, especialidade, crm): 
        conn = obter_conexao() 
        try: 
            with conn.cursor() as cursor: 
                sql = 'INSERT INTO medicos (nome, especialidade, crm) VALUES (%s, %s, %s)' 
                cursor.execute(sql, (nome, especialidade, crm)) 
            conn.commit() 
            return True 
        except pymysql.err.IntegrityError: 
            # CRM duplicado – o banco rejeita pois é UNIQUE 
            raise ValueError('CRM já cadastrado no sistema!') 
        finally: 
            conn.close() 
 
    @staticmethod 
    def listar_todos(): 
        conn = obter_conexao() 
        try: 
            with conn.cursor() as cursor: 
                cursor.execute('SELECT * FROM medicos WHERE ativo=1 ORDER BY nome') 
                return cursor.fetchall() 
        finally: 
            conn.close() 
 
    @staticmethod 
    def listar_nomes_ids(): 
        """Retorna lista simples (id, nome) para preencher Combobox.""" 
        conn = obter_conexao() 
        try: 
            with conn.cursor() as cursor: 
                cursor.execute('SELECT id, nome FROM medicos WHERE ativo=1 ORDER BY nome') 
                return cursor.fetchall() 
        finally: 
            conn.close() 
