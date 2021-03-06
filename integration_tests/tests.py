import requests
import random
import string

####################################################
# Global vars that will be used for testing purposes
####################################################

valid_carroceiro_1 = {"name": "carroceiro_test", "type": "carroceiro", "phone": "999111111",
                                             "address": "Av test, 9999", "latitude": -11.11, "longitude": -22.22}

# same carroceiro, including phone, but different address for example, this would be his house addresss
valid_carroceiro_2 = {"name": "carroceiro_test", "type": "carroceiro", "phone": "999111111",
                                             "address": "Av test, 1111", "latitude": -22.22, "longitude": -22.11}

# carroceiro's id(s)
ids = []

token = "2ad7cd83134a4908f8277c058a7b7da23b2876bc"

class TestCarroceirosListViews():
    """
    Class designed for testing the CarroceirosList class, which belongs to carroceiro.views
    """


    def test_get(self):

        try:
            r = requests.get('http://localhost:8000/carroceiro/')
            assert r.status_code == 200
            assert not r.json() == [], "The carroceiro_carroceiro table is empty! \
            You're supposed to run these tests with some entries in the database"
        except ConnectionError:
            assert False, "It couldn't connect to the database, make sure the database exists and authentication is ok"


    def test_post_valid_carroceiro(self):

        try:
            r = requests.post('http://localhost:8000/carroceiro/', json=valid_carroceiro_1, headers={'Authorization': 'Token {0}'.format(token)})
            assert r.status_code == 201

            r = requests.post('http://localhost:8000/carroceiro/', json=valid_carroceiro_2, headers={'Authorization': 'Token {0}'.format(token)})
            assert r.status_code == 201

        except ConnectionError:
            assert False, "It couldn't connect to the database, make sure the database exists and authentication is ok"


    def test_post_invalid_carroceiro(self):

        try:
            # post same carroceiro again who was used on test_post_valid_carroceiro
            data = {"name": "carroceiro_test", "phone": "999111111",
                                             "address": "Av test, 9999", "latitude": -11.11, "longitude": -22.22}
            r = requests.post('http://localhost:8000/carroceiro/', json=data, headers={'Authorization': 'Token {0}'.format(token)})
            assert not r.status_code == 201

            # invalid phone with less than 8 digits
            data = {"name": "carroceiro_test", "phone": "8411122",
                                             "address": "Av test, 9999", "latitude": -11.11, "longitude": -22.22}
            r = requests.post('http://localhost:8000/carroceiro/', json=data, headers={'Authorization': 'Token {0}'.format(token)})
            assert not r.status_code == 201

            # invalid phone with more than 15 digits
            data['phone'] = "9991111111111111"
            r = requests.post('http://localhost:8000/carroceiro/', json=data, headers={'Authorization': 'Token {0}'.format(token)})
            assert not r.status_code == 201

            # invalid phone with letters
            data['phone'] = "asdf"
            r = requests.post('http://localhost:8000/carroceiro/', json=data, headers={'Authorization': 'Token {0}'.format(token)})
            assert not r.status_code == 201

            # name can't be null in our DB!
            data['name'] = ''
            r = requests.post('http://localhost:8000/carroceiro/', json=data, headers={'Authorization': 'Token {0}'.format(token)})
            assert not r.status_code == 201

        except ConnectionError:
            assert False, "It couldn't connect to the database, make sure the database exists and authentication is ok"

class TestCarroceiroFilter():
    """
    Class designed for testing the CarroceirosList class filter, which belongs to carroceiro.views
    """

    def test_get_filter_by_phone(self):
        try:
            r = requests.get('http://localhost:8000/carroceiro/?phone={0}'.format(valid_carroceiro_1['phone']))
            assert r.status_code == 200
        except ConnectionError:
            assert False, "It couldn't connect to the database, make sure the database exists and authentication is ok"


class TestCarroceiroDetail():
    """
    Class designed for testing the CarroceiroDetail class, which belongs to carroceiro.views
    """

    def test_valid_get(self):

        try:
            # Before we test we need their ids which can be obtained with findbyphone view.
            r = requests.get('http://localhost:8000/carroceiro/?phone={0}'.format(valid_carroceiro_1['phone']))
            assert r.status_code == 200
            my_data = r.json()

            for my_dict in my_data:
                # ids is a global var
                ids.append(my_dict['id'])  # saving on this list for other next tests like put and delete.
                r = requests.get('http://localhost:8000/carroceiro/{0}/'.format(my_dict['id']))
                assert r.status_code == 200

        except ConnectionError:
            assert False, "It couldn't connect to the database, make sure the database exists and authentication is ok"

    def test_invalid_get(self):

        try:
            r = requests.get('http://localhost:8000/carroceiro/99999999999/')
            assert r.status_code == 404

        except ConnectionError:
            assert False, "It couldn't connect to the database, make sure the database exists and authentication is ok"

    def test_put(self):

        if not ids:
            assert False, "By now ids weren't supposed to be null"

        try:
            # since one carroceiro can have multiple ids..
            for id in ids:
                # this put will change their names to a random name and their phone.
                # I have to change their phone too because you can't have two different carroceiro.names who's got same phone number
                valid_carroceiro_1['name'] = ''.join(random.sample(string.ascii_lowercase, 10))
                valid_carroceiro_1['phone'] = str(int(valid_carroceiro_1['phone']) + 100)
                r = requests.put('http://localhost:8000/carroceiro/{0}/'.format(id), json=valid_carroceiro_1, headers={'Authorization': 'Token {0}'.format(token)})
                assert r.status_code == 200

        except ConnectionError:
            assert False, "It couldn't connect to the database, make sure the database exists and authentication is ok"

    def test_invalid_put(self):

        try:
            r = requests.put('http://localhost:8000/carroceiro/9999999999/', json=valid_carroceiro_1, headers={'Authorization': 'Token {0}'.format(token)})
            assert not r.status_code == 200

            # testing a valid id, but wrong json data (null name)
            invalid_carroceiro = valid_carroceiro_1
            invalid_carroceiro['name'] = ''

            r = requests.put('http://localhost:8000/carroceiro/{0}/'.format(ids[0]), json=invalid_carroceiro, headers={'Authorization': 'Token {0}'.format(token)})
            assert not r.status_code == 200

        except ConnectionError:
            assert False, "It couldn't connect to the database, make sure the database exists and authentication is ok"

    def test_delete(self):

        if not ids:
            assert False, "By now ids weren't supposed to be null"

        try:
            # since one carroceiro can have multiple ids..
            for id in ids:
                r = requests.delete('http://localhost:8000/carroceiro/{0}/'.format(id), headers={'Authorization': 'Token {0}'.format(token)})
                assert r.status_code == 204

        except ConnectionError:
            assert False, "It couldn't connect to the database, make sure the database exists and authentication is ok"

    def test_invalid_delete(self):

        try:
            r = requests.delete('http://localhost:8000/carroceiro/888888888888/', headers={'Authorization': 'Token {0}'.format(token)})
            assert not r.status_code == 204

        except ConnectionError:
            assert False, "It couldn't connect to the database, make sure the database exists and authentication is ok"