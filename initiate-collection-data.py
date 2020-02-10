import redis
import redisearch
import sys

# REDIS CONSTANTS
redis_host = 'localhost'
redis_port = 6379

def main():
    print("hello!")

    rs = redisearch.Client('recordIndex', redis_host, redis_port)

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
            'title': 'Degüello',
            'artist': 'ZZ Top',
            'year': 1979,
            'genre': ['rock']
        },
        {
            'title': 'American Beauty',
            'artist': 'Grateful Dead',
            'year': 1970,
            'genre': ['rock', 'psychedelic rock']
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

    test = True

    while test:
        txt = input("test me and enter something here: ")
        if (txt == "quit"):
            test = False


if __name__ == '__main__':
    main()
