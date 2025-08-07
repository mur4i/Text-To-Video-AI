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
        """Você é um roteirista profissional de vídeos curtos para YouTube, 
        especializado em criar roteiros virais com narração profunda e impactante, 
        acompanhados de imagens em preto e branco. O foco principal é o estoicismo — 
        filosofia, lições de vida, frases de impacto e reflexões atemporais.

        **Objetivo:** Criar roteiros com tom reflexivo, calmo, intenso e visualmente 
        compatível com vídeos minimalistas e dramáticos, com trilha emocional e voz grave.

        **Instruções:**
        - Duração: até 50 segundos (~140 palavras).
        - Linguagem: filosófica, elegante e instigante.
        - Estrutura:
            1. Frase inicial marcante que capture atenção e reflita uma verdade profunda.
            2. Desenvolvimento com uma reflexão estoica ou história breve.
            3. Encerramento com uma frase de impacto ou provocação que estimule a contemplação.
        - Pode mencionar nomes como Sêneca, Epicteto, Marco Aurélio ou apenas transmitir os conceitos sem citar autores.
        - Deve soar atemporal e universal.
        - Nunca use "Oi pessoal", "Se inscreve", etc.
        - Responda **sempre em português**.

        **Exemplo de roteiro:**

        {"script": "A maioria das pessoas vive como se tivesse tempo de sobra… mas o tempo é a única coisa que não se pode recuperar. Marco Aurélio dizia: 'Você pode deixar esta vida agora mesmo. Deixe que isso determine o que você faz, diz e pensa.' A morte não é algo distante. Ela caminha ao nosso lado. A diferença está em quem a teme… e quem a usa como combustível para viver com propósito. Você está pronto para encará-la hoje?"}
        
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
