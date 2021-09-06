import uvicorn

from cashback import application

app = application.create_app()

if __name__ == '__main__':
    uvicorn.run(app)
