from fastapi import FastAPI, UploadFile, File, HTTPException, status
import os
import shutil

app = FastAPI(title="Processador de Áudio Digital API")

# Cria a pasta para salvar os áudios, caso não exista
UPLOAD_DIR = "uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)

# Definição das restrições do requisito [NF005]
MAX_FILE_SIZE = 20 * 1024 * 1024  # 20 MB
ALLOWED_EXTENSIONS = {".wav", ".mp3"}

@app.post("/upload/")
async def upload_audio(file: UploadFile = File(...)):
    ext = os.path.splitext(file.filename)[1].lower()
    if ext not in ALLOWED_EXTENSIONS:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Formato inválido. Apenas arquivos WAV e MP3 são suportados."
        )

    # Lê o conteúdo para validar o tamanho de 20 MB[cite: 2]
    file_content = await file.read()
    if len(file_content) > MAX_FILE_SIZE:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="O arquivo excede o limite máximo permitido de 20 MB."
        )

    # Retorna o ponteiro para o início do arquivo após a leitura
    await file.seek(0)

    