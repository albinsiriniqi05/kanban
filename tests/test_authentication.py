from werkzeug.security import generate_password_hash
from tests import test_credentials

test_user = test_credentials.Test_User()


def test_first_entrance(client):
    """What the user should see when they first enter the app, without being logged in"""

    rv = client.get('/login')
    
    assert b'Login' in rv.data


def signup(client, email, firstname, lastname, password1, password2):
    """Sign-up function that returns the data"""
    return client.post('/sign-up', data={
            'email': email,
            'firstName': firstname,
            'lastName': lastname,
            'password1': password1,
            'password2': password2,
        }, follow_redirects=True)


def login(client, username, password):
    """Login function that returns the response"""
    return client.post('/login', data=dict(
        email=username,
        password=password
    ), follow_redirects=True)


def logout(client):
    """Logout function that returns the response"""
    return client.get('/logout', follow_redirects=True)


def signup_test(client):
    "Testing signup with a new user "
    rv = signup(client, 'test_user2@test.com', "Tester", 'password123', 'password123' )
    assert b'Account created!' in rv.data 


def login_test(client):
    """Testing if log in works, with the appropriate credentials."""
    

    c_user = login(client, test_user.username, test_user.password)

    assert b'Welcome' in c_user.data 

    assert b'My Tasks' in c_user.data 

    assert b'Login' not in c_user.data 

    assert b'Logout' in c_user.data 

    logout(client)

def incorrect_login_test(client):
    """Assert that the login flashes correct error messages for wrong email or password"""

    c_user = login(client, f"{test_user.username}x", test_user.password)
    assert b'This email does not exist.' in c_user.data

    c_user = login(client, test_user.username, f'{test_user.password}x')
    assert b'Incorrect password, please try again.' in c_user.data


def logout_test(client):
    """Assert logout works correctly and that the user sees the right menu items"""


    login(client, test_user.username, test_user.password)

    c_user = logout(client)
    assert b'Logged out successfully!' in c_user.data

    assert b'Logout' not in c_user.data 

    assert b'Login' in c_user.data 

    assert b'My Tasks' not in c_user.data 
    
