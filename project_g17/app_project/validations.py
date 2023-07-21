def validate_register(username, password):
  msg = ""
  if username == "":
    msg += "* Por favor ingrese un nombre de usuario.\n"
    
  if password == "":
    msg += "* Por favor ingrese una contraseña.\n"
    
  if len(password) < 6:
    msg += "* Tu contraseña debe de ser de al menos 6 caracteres.\n"
    
  if len(username) > 20:
    msg += "* Tu nombre de usuario no puede tener más de 20 caracteres.\n"
    
  if len(password) > 20:
    msg += "* Tu contraseña no puede tener más de 20 caracteres.\n"
    
  if msg == "":
    return True, msg
  else:
    return False, msg
    