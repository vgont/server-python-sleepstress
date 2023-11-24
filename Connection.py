import oracledb as odb
from Cliente import Cliente
from SonoCliente import SonoDiarioCliente
from typing import List


class Connection:
    def __init__(self, user, password):
        self.user = user
        self.password = password
        self.conn = None

    def __enter__(self):
        try:
            self.conn = odb.connect(user=self.user, password=self.password,
                                    dsn="oracle.fiap.com.br/orcl")
            return self.conn
        except Exception as e:
            print(e)

    def __exit__(self, exc_type, exc_val, exc_tb):
        if self.conn:
            self.conn.close()

    def inserir_cliente(cliente_dict: dict):
        cliente = Cliente(cliente_dict)
        with Connection('rm99069', '171103') as conn:
            sql = '''
            INSERT INTO t_ht_cliente 
            (id_cliente, nome_cliente, data_nasc_cliente, usuario_cliente, senha_cliente) 
            VALUES 
            (sq_id_cliente.nextval, :nome_cliente, to_date(:data_nasc_cliente, 'dd/mm/yyyy'), :usuario_cliente, :senha_cliente)
            '''

            cursor = conn.cursor()
            try:
                cursor.execute(sql, {
                    'nome_cliente': cliente.nome_cliente,
                    'data_nasc_cliente': cliente.data_nasc_cliente,
                    'usuario_cliente': cliente.usuario_cliente,
                    'senha_cliente': cliente.senha_cliente
                })
                conn.commit()
            except Exception as e:
                print(f"Erro ao inserir novo cliente: {e}")

    def alterar_cliente(cliente):
        print(cliente)
        with Connection('rm99069', '171103') as conn:
            sql = f'''
            update t_ht_cliente
            set altura_cliente = {cliente['altura_cliente']}, peso_cliente = {cliente['peso_cliente']}, classificacao_bmi = '{cliente['classificacao_bmi']}'
            where id_cliente = {cliente['id_cliente']}'''

            cursor = conn.cursor()
            try:
                cursor.execute(sql)
                conn.commit()
            except Exception as e:
                print(f"Erro ao alterar cliente: {e}")

    def excluir_cliente(id_cliente: int):
        with Connection('rm99069', '171103') as conn:
            sql = f'''delete from t_ht_cliente where id_cliente = {id_cliente}'''
            cursor = conn.cursor()
            try:
                cursor.execute(sql)
                conn.commit()
            except Exception as e:
                print(f"Erro ao excluir cliente: {e}")

    def buscar_cliente_by_user(user: str):
        with Connection('rm99069', '171103') as conn:
            sql = f'''select senha_cliente from t_ht_cliente where usuario_cliente = '{user}' '''
            cursor = conn.cursor()
            try:
                cursor.execute(sql)
                row = cursor.fetchone()
                if row:
                    senha = row[0]
                    return senha
            except Exception as e:
                print(f"Erro ao  cliente: {e}")

    def get_id_cliente_by_user(user_cliente: str) -> int or None:
        sql = f'''select id_cliente, to_char(data_nasc_cliente, 'dd/mm/yyyy') as data from t_ht_cliente where usuario_cliente = '{user_cliente}' '''
        with Connection('rm99069', '171103') as conn:
            cursor = conn.cursor()
            try:
                cursor.execute(sql)
                row = cursor.fetchone()

                if row:
                    id_cliente = row[0]
                    data_nasc = row[1]

                    return {"id": id_cliente, "data": data_nasc}
                else:
                    print('Nenhum id encontrado')
                    return None

            except Exception as e:
                print(f"Erro ocorreu ao buscar id do cliente: {e}")
                return None

    def inserir_sono_cliente(sono_dict: dict):
        sono_cliente = SonoDiarioCliente(sono_dict)
        with Connection('rm99069', '171103') as conn:
            sql = f'''
            insert into t_ht_sono_diario_cliente (id_sono, id_cliente, DURACAO_SONO, DATA_SONO, QUALIDADE_SONO, nivel_estresse, tempo_atividade_fisica) 
            values (sq_id_sono_cliente.nextval,{sono_cliente.id_cliente}, {sono_cliente.duracao_sono}, to_date('{sono_cliente.data_sono}', 'dd/mm/yyyy'), '{sono_cliente.qualidade_sono}', '{sono_cliente.nivel_estresse}', {sono_cliente.tempo_atividade_fisica})'''

            cursor = conn.cursor()
            try:
                cursor.execute(sql)
                conn.commit()
                print("inserido")
            except Exception as e:
                print(f"Erro ao inserir novo sono do cliente: {e}")

    def excluir_sono_cliente(id_sono):
        with Connection('rm99069', '171103') as conn:
            sql = f'''delete from t_ht_sono_diario_cliente where id_sono = {id_sono}'''
            cursor = conn.cursor()
            try:
                cursor.execute(sql)
                conn.commit()
                return True
            except Exception as e:
                print(f"Erro ao excluir sono: {e}")
                return False

    def find_all_sono_by_id_cliente(id_cliente):
        sql = f'''select id_sono, duracao_sono, to_char(data_sono, 'dd/mm/yyyy'), qualidade_sono, tempo_atividade_fisica, nivel_estresse from t_ht_sono_diario_cliente where id_cliente = {id_cliente}'''
        with Connection('rm99069', '171103') as conn:
            cursor = conn.cursor()
            try:
                cursor.execute(sql)
                sonos = []

                for row in cursor:
                    sono_data = {
                        'id_sono': row[0],
                        'duracao_sono': row[1],
                        'data_sono': row[2],
                        'qualidade_sono': row[3],
                        'tempo_atividade_fisica': row[4],
                        'nivel_estresse': row[5]
                    }
                    sonos.append(sono_data)

                return sonos
            except Exception as e:
                print(f"Erro ocorreu ao buscar sonos: {e}")
                return None


def none_to_null(value):
    if (value):
        return value
    return 'null'
