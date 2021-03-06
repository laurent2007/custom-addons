from argparse import ArgumentParser
from library_api import LibraryAPI


parser = ArgumentParser()
parser.add_argument(
        'command',
        choices=['list','add','set-title','del'])
parser.add_argument('params',nargs='*') # ke xuan can shu
args = parser.parse_args()

srv,port,db = '192.168.116.129',8069,'dev12'
user,pwd= 'admin','admin'
api = LibraryAPI(srv,port,db,user,pwd)

if args.command=='list':
    text = args.params[0] if args.params else None
    books = api.search_read(text)
    for book in books:
        print('%(id)d %(name)s' % book)

if args.command=='add':
    for title in args.params:
        new_id = api.create(title)
        print('Book added with ID %d.' % new_id)

if args.command =='set-title':
    if len(args.params) != 2:
        print("Set command requires a title and ID")

    else:
        book_id,title = int(args.params[0]),args.params[1]
        ari.write(title,book_id)
        print('Title set for book ID %d'% book_id)

if args.command =='del':
    for param in args.params:
        api.unlink(int(param))
        print('Book with ID %s deleted.' % param)
