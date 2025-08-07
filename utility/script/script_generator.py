import os
from openai import OpenAI
import json

if len(os.environ.get("GROQ_API_KEY")) > 30:
    from groq import Groq
    model = "mixtral-8x7b-32768"
    client = Groq(
        api_key=os.environ.get("GROQ_API_KEY"),
        )
else:
    OPENAI_API_KEY = os.getenv('OPENAI_KEY')
    model = "gpt-4o"
    client = OpenAI(api_key=OPENAI_API_KEY)

def generate_script(topic):
    prompt = (
        """Você é um roteirista profissional de vídeos narrados para YouTube, 
        especializado em criar roteiros virais com narração profunda e impactante, 
        acompanhados de imagens em preto e branco. O foco principal é o estoicismo — 
        filosofia, lições de vida, frases de impacto e reflexões atemporais.

        **Objetivo:** Criar roteiros com tom reflexivo, calmo, intenso e visualmente 
        compatível com vídeos minimalistas e dramáticos, com trilha emocional e voz grave.

        **Instruções:**
        - Duração: aproximadamente 2 minutos (~280 palavras).
        - Linguagem: filosófica, elegante e instigante.
        - Estrutura:
            1. Início com uma frase marcante ou provocativa.
            2. Desenvolvimento com uma lição estoica, reflexão sobre a vida ou história breve.
            3. Final com uma frase poderosa ou pergunta que permaneça na mente.
        - Pode mencionar Sêneca, Epicteto ou Marco Aurélio, mas não é obrigatório.
        - Evite qualquer linguagem informal ou termos modernos. Soe atemporal.
        - Nunca diga "se inscreva", "curta" ou "oi pessoal".
        - Responda **sempre em português**.

        **Exemplo de resposta esperada:**
        {"script": "A maioria das pessoas corre atrás do sucesso, sem saber que já tem o que precisa... [...] (até ~280 palavras)"}

        Gere SOMENTE um objeto JSON válido neste formato:
        {"script": "Aqui vai o roteiro..."}
        """
    )

    response = client.chat.completions.create(
            model=model,
            messages=[
                {"role": "system", "content": prompt},
                {"role": "user", "content": topic}
            ]
        )
    content = response.choices[0].message.content
    try:
        script = json.loads(content)["script"]
    except Exception as e:
        json_start_index = content.find('{')
        json_end_index = content.rfind('}')
        print(content)
        content = content[json_start_index:json_end_index+1]
        script = json.loads(content)["script"]
    return script
