# ORM: Object Relational Map
from flask import Flask, request, Response
from flask import json

from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, String, Integer, ForeignKey
from sqlalchemy.orm import relationship, backref

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker


Base = declarative_base()

class ToJson():
    def to_json(self):
        return json.dumps({col.name: getattr(self, col.name) for col in self.__table__.columns })


class Departamento(Base, ToJson):                   # public class Departamento extends Base {  }
    __tablename__ = 'departamento'
    id = Column(Integer, primary_key=True)
    nombre = Column(String)

    
class Persona(Base, ToJson):
    __tablename__ = 'persona'
    id = Column(Integer, primary_key=True)
    nombre = Column(String)
    apellido = Column(String)
    departamento_id = Column(Integer, ForeignKey('departamento.id'))
    departamento = relationship(
        Departamento,
        backref=backref('personas', uselist=True, cascade='delete,all')
    )

engine = create_engine('sqlite:///base_servido2.sqlite')

session = sessionmaker()
session.configure(bind=engine)

app = Flask(__name__) 

@app.route('/crearbase')
def crear_base():
    Base.metadata.create_all(engine)
    return 'Ok'


@app.route('/departamento', methods=['POST'])
def create_departamento():
    if not 'nombre' in request.form:
        return Response("Nombre no especificado", status=400)

    nombre = request.form['nombre']
    if nombre == '':
        return Response("{'mensaje_error':'Nombre vacio'}", status=400, mimetype='application/json')

    depto = Departamento(nombre=nombre)

    # depto = Departamento()
    # depto.nombre = nombre

    s = session()
    s.add(depto)
    s.commit()

    return Response(str(depto.id), status=201, mimetype='application/json')

@app.route('/departamento/<int:id>')
def get_departamento(id):
    s = session()
    d = s.query(Departamento).filter(Departamento.id==id).one()
    
    return Response(d.to_json(), status=200, mimetype='application/json')

@app.route('/departamento')
def list_departamento():
    s = session()
    dptos = s.query(Departamento)
    return Response(json.dumps([d.to_json() for d in dptos]), status=200, mimetype='application/json')

@app.route('/departamento', methods=['PUT'])
def put_departamento():
    id = request.form['id']
    nombre = request.form['nombre']
    
    s = session()
    d = s.query(Departamento).filter(Departamento.id==id).one()
    d.nombre = nombre
    s.commit()
    
    return Response(status=204)


if __name__ == '__main__':
    app.run(port=9001)