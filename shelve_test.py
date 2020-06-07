import shelve

d = shelve.open('base')

# d['users'] = [{'id': 0, 'username': 'user1', 'password': 'pass1'}, {'id': 1, 'username': 'user2', 'password': 'pass2'},
#               {'id': 2, 'username': 'user3', 'password': 'pass3'}]

#print(d['users'])

s = {'id': 0, 'username': 'user1', 'password': 'pass1'}
if 'user1' in s.values():
    print(s)

def if_exist(username):

    for i in d['users']:
        if username in i.values():
            return i
    return False