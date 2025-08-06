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
        """Você é um roteirista experiente de um canal de YouTube Shorts especializado em vídeos de curiosidades. 
        Crie roteiros curtos (menos de 50 segundos, aproximadamente 140 palavras), altamente envolventes e originais.

        Exemplo de roteiro (tipo "Fatos estranhos"):

        Fatos estranhos que você não sabia:
        - Bananas são tecnicamente frutas do tipo baga, mas morangos não são.
        - Uma única nuvem pode pesar mais de um milhão de quilos.
        - Existe uma espécie de água-viva biologicamente imortal.
        - O mel nunca estraga; arqueólogos encontraram potes com mais de 3.000 anos ainda comestíveis.
        - A guerra mais curta da história foi entre Reino Unido e Zanzibar em 1896 e durou apenas 38 minutos.
        - Polvos têm três corações e sangue azul.

        A partir do tipo de 'fatos' solicitado pelo usuário, crie o melhor roteiro possível.

        Responda sempre em português e forneça SOMENTE um objeto JSON válido no formato:

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
