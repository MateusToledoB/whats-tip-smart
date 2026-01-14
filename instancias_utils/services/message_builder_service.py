from instancias_utils.services.gpt_service import GPTService


class MessageBuilderService:
    """
    Responsável por gerar a mensagem final a partir
    do prompt do usuário e dos dados da linha.
    """

    def __init__(self):
        self.gpt_service = GPTService()

    def gerar_mensagem(self, prompt_usuario: str, dados_linha: dict) -> str:
        return self.gpt_service.gerar_mensagem(
            prompt_usuario=prompt_usuario,
            dados=dados_linha
        )
