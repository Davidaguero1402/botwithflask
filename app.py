from app import create_app

app = create_app()

if __name__ == '__main__':
    print("ESTA CORRIENDO LA APLICACION")
    app.run()