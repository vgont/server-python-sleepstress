class SonoDiarioCliente:
    def __init__(self, sono_data: dict):
        self.id_cliente = sono_data['id_cliente']
        self.duracao_sono = sono_data['duracao_sono']
        self.data_sono = sono_data['data_sono']
        self.qualidade_sono = sono_data['qualidade_sono']
        self.tempo_atividade_fisica = sono_data['tempo_atividade_fisica']
        self.nivel_estresse = sono_data['nivel_estresse']
