from flask_app import app #Importamos la app de la carpeta flask_app

from flask_app.controllers import usuarios, misiones



if __name__=="__main__": #Ejecutamos la aplicación

   app.run(debug=True)