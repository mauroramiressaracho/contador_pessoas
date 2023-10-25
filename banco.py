import mysql.connector

# Informações de conexão ao banco de dados
config = {
    'user': 'wanderley',
    'password': 'Java&claudio',
    'host': 'bdcontador-pessoas.mysql.database.azure.com',
    'port': 3306,  # Porta padrão para MySQL é 3306
    'database': 'contadorpessoas',
}

def insere_dados(data_entrada):
    try:
        # Tenta estabelecer uma conexão com o banco de dados
        conn = mysql.connector.connect(**config)
        print("Conexão ao banco de dados MySQL no Azure bem-sucedida!")

        # Cria um cursor para interagir com o banco de dados
        cursor = conn.cursor()

        # Exemplo de inserção de dados na tabela
        # 'id_date' é auto incrementado, então você não precisa inserir um valor para ele
        data_hora = str(data_entrada)  # Substitua isso pelo valor que deseja inserir

        # Query SQL para realizar a inserção
        sql_insert = "INSERT INTO registroPython (data_hora) VALUES (%s)"

        # Executa a query de inserção
        cursor.execute(sql_insert, (data_hora,))

        # Commit para confirmar a transação
        conn.commit()

        print("Inserção bem-sucedida!")

    except mysql.connector.Error as err:
        print(f"Erro: {err}")

    finally:
        # Certifique-se de sempre fechar o cursor e a conexão
        if 'cursor' in locals() and cursor:
            cursor.close()
        if 'conn' in locals() and conn.is_connected():
            conn.close()
            print("Conexão ao banco de dados MySQL no Azure fechada.")
