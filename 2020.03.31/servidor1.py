from flask import Flask, request, Response

app = Flask(__name__)

@app.route('/')     # Por default es GET
def saludar():
    return 'Hola mundo'

@app.route('/', methods=['POST'])
def saludar_servidor():
    print('me saludan')
    return 'Salude'

@app.route('/', methods=['DELETE'])
def borrar():
    print('me borran')
    return 'Borrado'

@app.route('/', methods=['PUT'])
def modificar():
    print('me modificaron')
    return 'Modificado'

@app.route('/mezclar', methods=['GET', 'POST'])
def mezcla():
    print('El cliente me pidio un : ', request.method)
    if request.method == 'GET':
        return 'Es un get\n'

    return 'Es un post\n'

@app.route('/arg')
def recibir_argumentos():
    print(request.args)
    
    if 'param1' in request.args:        # Busca param1 en las claves del diccionario
        print('El param1 es: ' + request.args['param1'])

    return 'Recibido'

@app.route('/arg/<param1>/<param2>')
def recibir_amistoso(param1, param2):
    print('Recibi ' + param1)
    print('Recibi ' + param2)
    
    return 'ok'


@app.route('/clientes', methods=['POST'])
def recibir_form():
    print(request.form)
    if 'apellido' in request.form:
        print('El apellido es ' + request.form['apellido'])

        return Response('Cliente creado', status=201)
    
    return Response('Falta apellido', status=400)


app.run()
