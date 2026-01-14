import os
from openai import OpenAI
from typing import Dict


class GPTService:
    """
    Serviço responsável por gerar textos usando a API da OpenAI.
    """

    def __init__(
        self,
        model: str = "gpt-4o-mini",
        temperature: float = 0.7,
        max_tokens: int = 200,
    ):
        self.client = OpenAI(
            api_key=os.getenv("OPENAI_API_KEY")
        )
        self.model = model
        self.temperature = temperature
        self.max_tokens = max_tokens

    def gerar_mensagem(
        self,
        prompt_usuario: str,
        dados: Dict[str, str],
    ) -> str:
        """
        Gera uma mensagem personalizada com base no prompt do usuário
        e nos dados do colaborador.
        """

        prompt = self._montar_prompt(prompt_usuario, dados)

        response = self.client.chat.completions.create(
            model=self.model,
            temperature=self.temperature,
            max_tokens=self.max_tokens,
            messages=[
                {"role": "user", "content": prompt}
            ],
        )

        return response.choices[0].message.content.strip()

    def _montar_prompt(
        self,
        prompt_usuario: str,
        dados: Dict[str, str],
    ) -> str:
        dados_formatados = "\n".join(
            f"{chave}: {valor}"
            for chave, valor in dados.items()
            if valor
        )

        return f"""
    Você é um assistente especializado em escrever mensagens curtas
    para WhatsApp corporativo.

    O usuário fornecerá:
    1. Um contexto da mensagem
    2. Um conjunto de informações do destinatário (podem variar)

    Regras:
    - Tom profissional e educado
    - Mensagem curta e objetiva
    - Sem emojis
    - Utilize apenas as informações fornecidas
    - Não invente dados
    - Varie levemente a forma de escrita
    - Não explique o que está fazendo

    Contexto do usuário:
    "{prompt_usuario}"

    Informações disponíveis do destinatário:
    {dados_formatados}

    Retorne apenas o texto final da mensagem.
    """

