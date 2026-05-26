import sender_stand_request
import data

def get_user_body(first_name):
    current_body = data.user_body.copy()
    current_body["firstName"] = first_name
    #current_body["phone"] = phone
    #current_body["address"] = address
    return current_body

def positive_assert(first_name):
    # El cuerpo de la solicitud actualizada se guarda en la variable user_body
    user_body = get_user_body(first_name)
    # El resultado de la solicitud para crear un nuevo usuario o usuaria se guarda en la variable response
    user_response = sender_stand_request.post_new_user(user_body)

def negative_assert_symbol(first_name):
    user_body = get_user_body(first_name)
    response = sender_stand_request.post_new_user(user_body)
    assert response.status_code == 400
    assert response.json()["code"] == 400
    assert response.json()["message"] == "Has introducido un nombre de usuario no válido. " \
                                         "El nombre solo puede contener letras del alfabeto latino, "\
                                         "la longitud debe ser de 2 a 15 caracteres."

def negative_assert_no_firstname(user_body):
    response = sender_stand_request.post_new_user(user_body)
    assert response.status_code == 400
    assert response.json()["code"] == 400
    assert response.json()["message"] == "No se han aprobado todos los parámetros requeridos"

#Prueba 1. Usuario de 2 caracteres

def test_create_user_2_letter_in_first_name_get_success_response():
    user_body = get_user_body("Aa")
    user_response = sender_stand_request.post_new_user(user_body)
    assert user_response.status_code == 201
    assert user_response.json()["authToken"] != ""

    users_table_response = sender_stand_request.get_users_table()
    str_user = user_body["firstName"] + "," + user_body["phone"] + "," \
               + user_body["address"] + ",,," + user_response.json()["authToken"]

    assert users_table_response.text.count(str_user) == 1

#Prueba 2. Usuario de 15 caracteres

def test_create_user_15_letter_in_first_name_get_success_response():
    user_body = get_user_body("Aaaaaaaaaaaaaaa")
    user_response = sender_stand_request.post_new_user(user_body)
    assert user_response.status_code == 201
    assert user_response.json()["authToken"] != ""

    users_table_response = sender_stand_request.get_users_table()
    str_user = user_body["firstName"] + "," + user_body["phone"] + "," \
               + user_body["address"] + ",,," + user_response.json()["authToken"]

    assert users_table_response.text.count(str_user) == 1

#Pruebas Negativas
# Prueba Negativa 3: Un caracracter en primer nombre

def test_create_user_1_letter_in_first_name_get_error_response():
    negative_assert_symbol("A")

#Prueba Negativa 4: 16 Caracteres en primer nombre
def test_create_user_16_letter_in_first_name_get_error_response():
    negative_assert_symbol("Aaaaaaaaaaaaaaaa")


# Prueba Negativa 5: Un espacio en el primer Nombre
def test_create_user_has_space_in_first_name_get_error_response():
    negative_assert_symbol("A Aaa")

# Prueba Negativa 6: Un caracracter especial en primer nombre
def test_create_user_has_special_symbol_in_first_name_get_error_response():
    negative_assert_symbol("\"№%@\",")

# Prueba Negativa 7: Un numero en primer nombre
def test_create_user_has_number_in_first_name_get_error_response():
    negative_assert_symbol("123")

#No se pasa el parametro en la solicitud

# Prueba Negativa 8: Un campo vacio en primer nombre

def test_create_user_no_first_name_get_error_response():
    user_body = data.user_body.copy()
    user_body.pop("firstName")
    negative_assert_no_firstname(user_body)

# Prueba Negativa 9: Un campo vacio se envio en primer nombre
def test_create_user_no_last_name_get_error_response():
    user_body = get_user_body("")
    negative_assert_no_firstname(user_body)

def test_create_user_number_type_first_name_get_error_response():
    user_body = get_user_body(12)
    response = sender_stand_request.post_new_user(user_body)
    assert response.json()["code"] == 400





