from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import psycopg

app = FastAPI()
# Rodar a API no terminal para ip externo: uvicorn main:app --host 0.0.0.0 --port 8000 --reload
# Configuração do CORS para permitir que o Front-end converse com o Back-end no Localhost
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Configuração da conexão com o PostgreSQL local
DB_CONFIG = "dbname=To_DOList user=postgres password=98912032 host=localhost port=5432"


class UsuarioSchema(BaseModel):
    usuario: str
    senha: str


@app.post("/register")
def registrar_usuario(dados: UsuarioSchema):
    # Regra da Sprint: o nome de usuário deve conter apenas letras
    if not dados.usuario.isalpha():
        raise HTTPException(
            status_code=400,
            detail="O nome de usuário deve conter apenas letras."
        )

    try:
        with psycopg.connect(DB_CONFIG) as conn:
            with conn.cursor() as cur:
                cur.execute(
                    "INSERT INTO users (username, password_hash) VALUES (%s, %s)",
                    (dados.usuario, dados.senha)
                )
                conn.commit()
        return {"status": "sucesso", "mensagem": "Usuário cadastrado com sucesso!"}
    except Exception as e:
        raise HTTPException(
            status_code=400,
            detail=f"Erro ao cadastrar (o usuário já pode existir): {str(e)}"
        )


@app.post("/login")
def logar_usuario(dados: UsuarioSchema):
    try:
        with psycopg.connect(DB_CONFIG) as conn:
            with conn.cursor() as cur:
                cur.execute(
                    "SELECT password_hash FROM users WHERE username = %s",
                    (dados.usuario,)
                )
                resultado = cur.fetchone()

                if not resultado or resultado[0] != dados.senha:
                    raise HTTPException(status_code=401, detail="Usuário ou senha inválidos.")

        return {"status": "sucesso", "mensagem": "Login realizado com sucesso!"}
    except HTTPException as he:
        raise he
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Erro interno no servidor: {str(e)}"
        )