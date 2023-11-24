class Cliente:
    def __init__(self, cliente_data: dict):
        self.id_cliente = cliente_data['id_cliente']
        self.usuario_cliente = cliente_data['usuario_cliente']
        self.senha_cliente = cliente_data['senha_cliente']
        self.nome_cliente = cliente_data['nome_cliente']
        self.data_nasc_cliente = cliente_data['data_nasc_cliente']
