import mysql.connector

# Informações de conexão ao banco de dados
config = {
    'user': 'wanderley',
    'password': 'Java&claudio',
    'host': 'bdcontador-pessoas.mysql.database.azure.com',
    'port': 3306,  # Porta padrão para MySQL é 3306
    'database': 'contadorpessoas',
}

try:
    # Tenta estabelecer uma conexão com o banco de dados
    conn = mysql.connector.connect(**config)
    print("Conexão ao banco de dados MySQL no Azure bem-sucedida!")

    # Aqui você pode executar consultas e operações no banco de dados

except mysql.connector.Error as err:
    print(f"Erro: {err}")

finally:
    # Certifique-se de sempre fechar a conexão, independentemente de ela ser bem-sucedida ou não
    if 'conn' in locals() and conn.is_connected():
        conn.close()
        print("Conexão ao banco de dados MySQL no Azure fechada.")
