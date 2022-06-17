from main import Db

database = Db()
for elem in database.get_all():
    id, username, first_name, last_name = elem
    print(' '.join([str(id).ljust(15), username.ljust(20), first_name.ljust(20), last_name.ljust(20)]))
