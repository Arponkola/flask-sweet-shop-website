import app

mapp = app.create_app()

if __name__=="__main__":
    mapp.run(debug=True)