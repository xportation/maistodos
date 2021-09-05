from fastapi import FastAPI

app = FastAPI()


@app.get('/')
async def read_index():
    return {'Hello': 'World'}
