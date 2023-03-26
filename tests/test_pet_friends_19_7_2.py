import os
import sys

import pytest
from api import PetFriends
from settings import *


pf = PetFriends(base_url)

# positive tests get_api_key
def test_get_api_key_valid_user(email=valid_email, password=valid_password):
	status, result = pf.get_api_key(email, password)
	assert status == 200
	assert 'key' in result


# negative tests get_api_key
@pytest.mark.parametrize('email, password', [
	(valid_email, 'blabla_pass'),
	('blabla_user', valid_password),
	('None', valid_password),
	(valid_email, 'None')
])
def test_get_api_key_not_valid_user(email, password):
	status, result = pf.get_api_key(email, password)
	assert status != 200
	assert 'Forbidden' in result


# positive tests post_create_pet_simple
@pytest.mark.parametrize('name, animal_type, age', [
	('Murzuk', 'cat', '3'),
	('Tuzuk', 'dog', '8'),
	('Бим', 'Сабакен', '10')
])
def test_post_create_pet_simple_with_valid_data(name, animal_type, age):
	_, auth_key = pf.get_api_key(valid_email, valid_password)
	status, result = pf.post_create_pet_simple(auth_key, name, animal_type, age)
	assert status == 200
	assert result['name'] == name


# negative tests post_create_pet_simple
@pytest.mark.parametrize('name, animal_type, age', [
	('None', 'cat', '3'),
	('Tuzuk', 'None', '8'),
	('Murzuk', 'None', 'None')
])
def test_post_create_pet_simple_with_valid_data(name, animal_type, age):
	_, auth_key = pf.get_api_key(valid_email, valid_password)
	status, result = pf.post_create_pet_simple(auth_key, name, animal_type, age)
	assert status == 400
	assert 'Bad Request' in result


# negative tests create_pet_simple fake token
def test_post_create_pet_simple_with_invalid_key(name='name', animal_type='animal_type', age='age'):
	auth_key = {'key': 'fake_key'}
	status, result = pf.post_create_pet_simple(auth_key, name, animal_type, age)
	assert status == 403
	assert 'Forbidden' in result


# positive tests get_pets
@pytest.mark.parametrize('pets_filter', ['', 'my_pets'])
def test_get_pets_with_valid_data(pets_filter):
	_, auth_key = pf.get_api_key(valid_email, valid_password)
	status, result = pf.get_pets(auth_key, pets_filter)
	assert status == 200
	assert len(result['pets']) > 0


# negative tests get_pets fake token
def test_get_pets_with_invalid_key(pets_filter=''):
	auth_key = {'key': 'fake_key'}
	status, result = pf.get_pets(auth_key, pets_filter)
	assert status == 403
	assert 'Forbidden' in result


# negative tests get_pets
@pytest.mark.parametrize('pets_filter', ['our_pets'])
def test_get_pets_with_invalid_data(pets_filter):
	_, auth_key = pf.get_api_key(valid_email, valid_password)
	status, result = pf.get_pets(auth_key, pets_filter)
	assert status == 500
	assert 'Filter value is incorrect' in result


# positive tests post_pets
@pytest.mark.parametrize('name, animal_type, age, pet_photo', [
	('Murzuk', 'cat', '3', 'images\cat0.jpg'),
	('Tuzuk', 'Котэ', '8', 'images\cat1.jpg'),
	('Бим', 'Сабакен', '12', 'images\cat2.jpg')
])
def test_post_pets_with_valid_data(name, animal_type, age, pet_photo):
	_, auth_key = pf.get_api_key(valid_email, valid_password)
	pet_photo = os.path.join(os.path.dirname(__file__), pet_photo)
	status, result = pf.post_pets(auth_key, name, animal_type, age, pet_photo)
	assert status == 200
	assert result['name'] == name


# negative tests post_pets
@pytest.mark.parametrize('name, animal_type, age, pet_photo', [
	('None', 'cat', '3', 'images\cat0.jpg'),
	('Tuzuk', 'None', '8', 'images\cat1.jpg'),
	('Бим', 'Сабакен', 'None', 'images\cat2.jpg')
])
def test_post_pets_with_invalid_data(name, animal_type, age, pet_photo):
	_, auth_key = pf.get_api_key(valid_email, valid_password)
	pet_photo = os.path.join(os.path.dirname(__file__), pet_photo)
	status, result = pf.post_pets(auth_key, name, animal_type, age, pet_photo)
	assert status == 400
	assert 'Bad Request' in result


# negative tests post_pets fake token
def test_post_pets_with_invalid_key(name='Zevs', animal_type='Cat', age='12', pet_photo='images\cat0.jpg'):
	auth_key = {'key': 'fake_key'}
	pet_photo = os.path.join(os.path.dirname(__file__), pet_photo)
	status, result = pf.post_pets(auth_key, name, animal_type, age, pet_photo)
	assert status == 403
	assert 'Forbidden' in result


# positive tests post_pets_set_photo
def test_post_pets_set_photo_with_valid_data(pet_photo='images\cat1.jpg'):
	_, auth_key = pf.get_api_key(valid_email, valid_password)
	_, result = pf.post_create_pet_simple(auth_key, 'name', 'animal_type', '1')

	status, result = pf.post_pets_set_photo(auth_key, result['id'], pet_photo)
	assert status == 200
	assert 'data:image/jpeg' in result['pet_photo']


# negative tests post_pets_set_photo
def test_post_pets_set_photo_with_invalid_data(pet_photo='images\cat0.jpg'):
	_, auth_key = pf.get_api_key(valid_email, valid_password)
	_, my_pets = pf.get_pets(auth_key, "my_pets")

	status, result = pf.post_pets_set_photo(auth_key, 'fake_id', pet_photo)
	assert status == 500
	assert 'Internal Server Error' in result


# negative tests post_pets_set_photo fake token
def test_post_pets_set_photo_with_invalid_key(pet_photo='images\cat0.jpg'):
	_, auth_key = pf.get_api_key(valid_email, valid_password)
	_, my_pets = pf.get_pets(auth_key, "my_pets")

	auth_key = {'key': 'fake_key'}
	status, result = pf.post_pets_set_photo(auth_key, my_pets['pets'][0]['id'], pet_photo)
	assert status == 403
	assert 'Forbidden' in result


# positive tests delete_pets
def test_delete_pets_with_valid_data():
	_, auth_key = pf.get_api_key(valid_email, valid_password)
	_, my_pets = pf.get_pets(auth_key, "my_pets")

	if len(my_pets['pets']) > 0:
		status, result = pf.delete_pets(auth_key, my_pets['pets'][0]['id'])
		assert status == 200
	else:
		raise Exception("There is no my pets")


# negative tests delete_pets
def test_delete_pets_with_invalid_data():
	_, auth_key = pf.get_api_key(valid_email, valid_password)

	status, result = pf.delete_pets(auth_key, 'fake_id')
	assert status == 200


# negative tests delete_pets fake token
def test_delete_pets_with_invalid_key():
	_, auth_key = pf.get_api_key(valid_email, valid_password)
	_, my_pets = pf.get_pets(auth_key, "my_pets")

	auth_key = {'key': 'fake_key'}
	if len(my_pets['pets']) > 0:
		status, result = pf.delete_pets(auth_key, my_pets['pets'][0]['id'])
		assert status == 403
		assert 'Forbidden' in result
	else:
		raise Exception("There is no my pets")


# positive tests put_pets
def test_put_pets_with_valid_data(name='Новое имя', animal_type='Новая порода', age=100500):
	_, auth_key = pf.get_api_key(valid_email, valid_password)
	_, my_pets = pf.get_pets(auth_key, "my_pets")

	if len(my_pets['pets']) > 0:
		status, result = pf.put_pets(auth_key, my_pets['pets'][0]['id'], name, animal_type, age)
		assert status == 200
		assert result['name'] == name
	else:
		raise Exception("There is no my pets")


# negative tests get_pets fake
def test_put_pets_with_invalid_data(name='Новое имя', animal_type='Новая порода', age=100500):
	_, auth_key = pf.get_api_key(valid_email, valid_password)

	status, result = pf.put_pets(auth_key, 'fake_id', name, animal_type, age)
	assert status == 400
	assert 'Bad Request' in result


# negative tests get_pets fake token
def test_put_pets_with_invalid_key(name='Новое имя', animal_type='Новая порода', age=100500):
	_, auth_key = pf.get_api_key(valid_email, valid_password)
	_, my_pets = pf.get_pets(auth_key, "my_pets")

	auth_key = {'key': 'fake_key'}
	if len(my_pets['pets']) > 0:
		status, result = pf.put_pets(auth_key, my_pets['pets'][0]['id'], name, animal_type, age)
		assert status == 403
		assert 'Forbidden' in result
	else:
		raise Exception("There is no my pets")