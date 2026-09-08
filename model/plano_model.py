# model/plano_model.py 
from database.conexao import obter_conexao 
 
class PlanoModel: 
 
    @staticmethod 
    def inserir(nome, codigo): 
        conn = obter_conexao() 
        try: 
            with conn.cursor() as cursor: 
                cursor.execute( 
                    'INSERT INTO planos (nome, codigo) VALUES (%s, %s)', 
                    (nome, codigo) 
                ) 
            conn.commit() 
            return True 
        finally: 
            conn.close() 
 
    @staticmethod 
    def listar_todos(): 
        conn = obter_conexao() 
        try: 
            with conn.cursor() as cursor: 
                cursor.execute('SELECT * FROM planos WHERE ativo=1 ORDER BY nome') 
                return cursor.fetchall() 
        finally: 
            conn.close() 
