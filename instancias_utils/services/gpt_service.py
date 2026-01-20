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
    Você é um assistente especializado em redigir mensagens curtas
    para comunicação corporativa via WhatsApp, com foco em naturalidade
    e linguagem humana.

    Objetivo:
    Gerar mensagens que não aparentem automação ou envio em massa.

    O usuário fornecerá:
    1. Um contexto da mensagem
    2. Um conjunto de informações do destinatário (podem variar)

    Diretrizes importantes:
    - Escreva como uma pessoa real escreveria
    - Evite frases genéricas ou padronizadas
    - Varie naturalmente a construção das frases
    - Não use linguagem publicitária
    - Não use emojis
    - Não use chamadas agressivas ou imperativas
    - Não utilize palavras que indiquem envio automático ou sistema
    - Mantenha tom profissional, cordial e respeitoso
    - Mensagem curta, clara e contextual
    - Utilize apenas as informações fornecidas
    - Nunca invente dados
    
    Contexto do usuário:
    "{prompt_usuario}"

    Informações disponíveis do destinatário:
    {dados_formatados}

    Retorne apenas o texto final da mensagem.
    """

