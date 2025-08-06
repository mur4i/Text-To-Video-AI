import edge_tts

async def generate_audio(text,outputFilename):
    communicate = edge_tts.Communicate(text,"pt-BR-AntonioNeural")
    await communicate.save(outputFilename)





