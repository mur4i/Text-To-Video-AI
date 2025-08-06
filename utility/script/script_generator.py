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
        """Você é um roteirista profissional especializado em vídeos curtos para canais "dark" do YouTube, 
        focados em conspirações, mistérios inexplicáveis e segredos ocultos. 
        Seu objetivo é prender a atenção do espectador desde a primeira frase, gerando suspense e curiosidade.

        **Instruções:**
        - Duração: até 50 segundos (~140 palavras).
        - Linguagem: direta, intrigante e misteriosa, que desperte emoções fortes.
        - Estrutura: 
            1. Frase inicial impactante que chame a atenção.
            2. Desenvolvimento rápido com fatos ou teorias surpreendentes.
            3. Final com suspense ou pergunta aberta para estimular comentários.
        - Evite introduções genéricas como "Olá pessoal".
        - Não cite fontes; o tom deve parecer uma descoberta secreta.
        - Responda **sempre em português**.

        **Exemplo de roteiro:**

        "Existe uma teoria sombria que poucas pessoas conhecem… 
        dizem que civilizações antigas possuíam tecnologia capaz de manipular o clima. 
        Documentos secretos do século passado sugerem que isso foi escondido da humanidade 
        para manter o controle global. E se eu te disser que até hoje existem máquinas 
        misteriosas que podem criar tempestades em qualquer lugar do planeta? 
        Acha que isso é apenas ficção ou estamos vivendo uma mentira bem planejada?"

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
