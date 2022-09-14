from tests import test_credentials

test_user = test_credentials.Test_User()
test_task = test_credentials.Test_Task()

def login(client, username, password):
    """Login function that returns the response"""
    return client.post('/login', data=dict(
        email=username,
        password=password
    ), follow_redirects=True)

def add_task(client, title, descr, stat):

    """Function that adds task and returns the response"""

    return client.post('/', data=dict(
        title=title,
        descr=descr,
        stat = stat,
    ), follow_redirects=True)

def move_task(client, taskId, newstat):

    """Function that moves a task and return the response"""
     
    client.post('/move-task', data='{ "taskId": "%i", "newStatus": "%s" }' % (taskId, newstat),
    follow_redirects=True)
    return client.get('/kanban')

def delete_task(client, taskId):

    """Function that deletes a task and return the response"""

    client.post('/delete-task', data='{ "taskId": "%i" }' % (taskId),
    follow_redirects=True)
    return client.get('/kanban')

def add_task_test(client):

    "Testing that a task is added"

    login(client, test_user.username, test_user.password)
    
    rv = add_task(client, "another"+test_task.title, test_task.descr, test_task.stat)
    assert b'Task added!' in rv.data


def move_task_test(client):

    "Testing that a task is moved" 
    
    login(client, test_user.username, test_user.password)
    add_task(client, "another"+test_task.title, test_task.descr, test_task.stat)

    c_user = move_task(client, 1, "doing")
    assert b"moveTask(1, \'todo\')" in c_user.data 
    assert b"moveTask(1, \'done\')" in c_user.data

def delete_task_test(client):

    "Testing that a task is deleted"

    login(client, test_user.username, test_user.password)
    add_task(client, "another"+test_task.title, test_task.descr, test_task.stat)
    
    c_user = delete_task(client, 1)
    assert b"deleteTask(1)" not in c_user.data 

    

    