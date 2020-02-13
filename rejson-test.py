import redis
import rejson 
import json

# REDIS CONSTANTS
redis_host = 'localhost'
redis_port = 6379

def main():
    rj = rejson.Client(host=redis_host, port=redis_port, decode_responses=True)    
    rj.flushall()
    json_data = []
    load_data(json_data, rj)

def load_data(data, rj):
    print("loading data!")
    with open("record-collection.json") as json_file:
        data = json.load(json_file)
    for r in data:
        rec_id = 'records:' + str.lower(r.get('title')).replace(' ', '').replace('\'', '')
        rj.jsonset(rec_id, rejson.Path.rootPath(), r)

if __name__ == '__main__':
    main()