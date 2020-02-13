import redis
import redisearch
import sys
import string

# REDIS CONSTANTS
redis_host = 'localhost'
redis_port = 6379

def main():
    print("hello!")

    r = redis.Redis(host=redis_host, port=redis_port)
    rs = redisearch.Client('recordIndex', redis_host, redis_port)
    
    # flush to get a fresh db
    # TODO - remove when dockerized
    r.flushall()

    record_collection = [
        {
            'title': 'Brothers and Sisters',
            'artist': 'Allman Brothers',
            'year': 1973,
            'genre': ['rock', 'southern rock', 'blues rock']
        },
        {
            'title': 'Aja',
            'artist': 'Steely Dan',
            'year': 1977,
            'genre': ['rock', 'pop']
        },
        {
            'title': 'Can\'t Buy a Thrill',
            'artist': 'Steely Dan',
            'year': 1972,
            'genre': ['rock', 'pop']
        },
        {
            'title': 'Deguello',
            'artist': 'ZZ Top',
            'year': 1979,
            'genre': ['rock']
        },
        {
            'title': 'American Beauty',
            'artist': 'Grateful Dead',
            'year': 1970,
            'genre': ['rock', 'psychedelic rock']
        },
        {
            'title': 'Second Helping',
            'artist': 'Lynard Skynard',
            'year': 1974,
            'genre': ['rock', 'southern rock']
        },
        {
            'title': 'The Joker',
            'artist': 'Steve Biller Band',
            'year': 1973,
            'genre': ['rock', 'blues rock']
        },
        {
            'title': 'Book of Dreams',
            'artist': 'Steve Biller Band',
            'year': 1977,
            'genre': ['rock']
        },
        {
            'title': 'Rumours',
            'artist': 'Fleetwood Mac',
            'year': 1977,
            'genre': ['rock', 'pop']
        },
        {
            'title': 'Where We All Belong',
            'artist': 'Marshall Tucker Band',
            'year': 1974,
            'genre': ['rock', 'southern rock']
        }
    ]

    try:
        rs.create_index((
            redisearch.TextField('title', sortable=True),   
            redisearch.TextField('artist', sortable=True),
            redisearch.NumericField('year', sortable=True),
            redisearch.TagField('genre', separator=',')
        ))
    except Exception:
            print(f'Error creating index: {sys.exc_info()}')
    print(f'index info: {rs.info()}')

    run = True

    load_data(rs, record_collection)

    while run:
        txt = input("enter a search term: ")
        if (txt == "quit"):
            run = False
            break
        txt_arr = txt.split(' ', 1)
        print(f'searching {txt_arr}')
        if (txt_arr[0] == 'title'):
            res = rs.search(f'@title:{txt_arr[1]}')
            print(res)
        elif (txt_arr[0] == 'artist'):
            res = rs.search(f'@artist:{txt_arr[1]}')
            print(res)
        elif (txt_arr[0] == 'year'):
            full_txt_arr = txt.split(' ')
            former = full_txt_arr[1]
            latter = full_txt_arr[1]
            if (len(full_txt_arr) == 3):
               latter = full_txt_arr[2]
            res = rs.search(f'@year:[{former} {latter}]')
            print(res)
        elif (txt_arr[0] == 'genre'):
            pass
        else:
            print("invalid query")
            



def load_data(rs, collection):
    # add items to the index 
    for record in collection:
        str.lower
        rec_id = 'records:' + (str.lower(record.get('artist')) + ':' + str.lower(record.get('title'))).replace(' ', '')
        # rs.add_document()
        print(f'new record--> {rec_id}')
        rs.add_document(rec_id, title=record.get('title'), artist=record.get('artist'), year=record.get('year'), genre=','.join(record.get('genre')))
    return 0

if __name__ == '__main__':
    main()
