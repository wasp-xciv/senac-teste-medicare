# database/conexao.py 
import pymysql 
 
# ─── CONFIGURAÇÕES ──────────────────────────────── 
# Altere abaixo com os dados do SEU MySQL 
HOST     = 'localhost' 
USUARIO  = 'root' 
SENHA    = ''          # sua senha do MySQL 
BANCO    = 'medicare_db' 
# ────────────────────────────────────────────────── 
 
def obter_conexao(): 
    """ 
    Cria e retorna uma conexão com o banco MySQL. 
    Sempre que precisar do banco, chame essa função. 
    """ 
    conexao = pymysql.connect( 
        host=HOST, 
        user=USUARIO, 
        password=SENHA,
        database=BANCO,
        charset='utf8mb4', 
        cursorclass=pymysql.cursors.DictCursor  # retorna dicionários 
    ) 
    return conexao 
 
 
def testar_conexao(): 
    """Testa se a conexão está funcionando. Use para depurar.""" 
    try: 
        conn = obter_conexao() 
        print('✅ Conexão com MySQL OK!') 
        conn.close() 
    except Exception as e: 
        print(f'❌ Erro na conexão: {e}') 
 

# Teste ao rodar o arquivo diretamente 
if __name__ == '__main__': 
    testar_conexao()  