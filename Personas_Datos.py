import conexion as con

#Crear una persona
def save (persona):
  persona=dict(persona)
  try:
    db= con.conectar()
    cursor=db.cursor()
    columnas=tuple(persona.keys())
    valores= tuple(persona.values())
    sql= """
     INSERT INTO personas{campos} VALUES(?,?,?,?,?,?)
     """.format(campos=columnas)
    cursor.execute(sql,(valores))
    creada=cursor.rowcount>0
    db.commit()
    if creada:
      return {'Respuesta':creada,'Mensaje':'Persona Registrada con exito'}
    else:
      return {'Respuesta':creada,'Mensaje':'Persona Registrada sin exito'}
  except Exception as ex:
    if 'UNIQUE' in str(ex) and "dni" in str(ex):
      mensaje='Ya existe una persona con este DNI'
    elif 'UNIQUE' in str(ex) and "correo" in str(ex):
      mensaje='Ya existe una persona con este correo'   
    else: 
     mensaje= str(ex)
    return {'Respuesta':False,'Mensaje':mensaje }
  finally:
   cursor.close()
   db.close()

# Leer todas las personas
def findAll():
  try:
    db=con.conectar()
    cursor=db.cursor()
    cursor.execute("SELECT * FROM personas")
    total_personas= cursor.fetchall()
    if total_personas:
      return {"Respuesta":True,"Total_personas":total_personas,"Mensaje":"Pesonas listadas"}
    return {"Respuesta":False,"Mensaje":"No hay personas listadas aun"}
  except Exception as ex:
    return{"Respuesta":False,"ERROR":str(ex)}
  finally:
    cursor.close()
    db.close()
  
# Leer una persona en especificon con su DNI
def find(dni):
  try:
    db=con.conectar()
    cursor=db.cursor()
    cursor.execute("SELECT * FROM personas WHERE dni='{dniPersona}'"
    .format(dniPersona=dni))
    res= cursor.fetchall()
    if res:
      info=res[0]
      persona={"Id":info[0],"Dni":info[1],"Edad":info[2],"Nombre":info[3],"Apellido":info[4],"Direccion":info[5],"Correo":info[6]}
      return {'Respuesta':True,"Persona":persona,'Mensaje':'Persona encontrada con exito'}
    return {'Respuesta':False,'Mensaje':'No existe la persona'}
  except Exception as ex:
    return{'Respuesta':False,'ERROR':str(ex)}
  finally:
    cursor.close()
    db.close()

# Actualizar una persona

def update(persona):
  try:
    db=con.conectar()
    cursor=db.cursor()
    persona=dict(persona)
    dniPersona=persona.get('dni')
    persona.pop('dni')
    valores=tuple(persona.values())
    sql="""
    UPDATE personas 
    SET edad=?,nombre=?,apellido=?,direccion=?,correo=?
    WHERE dni='{dni}'
    """.format(dni=dniPersona)
    cursor.execute(sql,(valores))
    modificada=cursor.rowcount>0
    db.commit()
    if modificada:
     return{'respuesta':modificada,'mensaje':'Persona modificada con exito'}
    else:
      return{'respuesta':modificada,'mensaje':'No existe una persona con ese DNI'}
  
  except Exception as ex:
   return{'Mensaje':"No se pudo modificar la persona",'Error':str(ex)} 

  finally:
    cursor.close()
    db.close()

# Eliminar una persona con su id  
def delete(idPersona):
  try:
    db=con.conectar()
    cursor=db.cursor()
    sql="""
    DELETE FROM personas 
    WHERE id={id}
    """.format(id=idPersona)
    cursor.execute(sql)
    eliminada=cursor.rowcount>0
    db.commit()
    if eliminada:
     return{'respuesta':eliminada,'mensaje':'Persona eliminada con exito'}
    else:
      return{'respuesta':eliminada,'mensaje':'No existe una persona con ese ID'}
  
  except Exception as ex:
   return{'Mensaje':"No se pudo eliminar la persona",'Error':str(ex)} 

  finally:
    cursor.close()
    db.close() 
 