import redis

redis_instances = redis.StrictRedis(host='localhost', port=6379, db=1)
# for key in r.scan_iter():
#     print(key)


# class RedisServices:

#     def set_token(self, key, value):
#         # this method is used to add the data to redis
#         r.set(key, value)
#         print('token set')

#     def get_token(self, key):
#         # this method is used to get the data out of redis
#         token = r.get(key)
#         return token

#     def flush(self):
#         # this method is used to delete data from redis
#         r.flushall()