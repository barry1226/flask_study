import math
import redis
import threading
from flask import Flask, request, render_template, jsonify

app = Flask(__name__)
app.debug = True

class CachePi:
    def __init__(self, client):
        self.client = client

    def set_pi(self, n, pi):
        self.client.hset('pis', str(n), str(pi))
    
    def get_pi(self, n):
        result = self.client.hget('pis', str(n))
        if result:
            return float(result)
        return None
    
    def set_fib(self, n, fib):
        self.client.hset('fibs', str(n), str(fib))

    def get_fib(self, n):
        result = self.client.hget('fibs', str(n))
        if result:
            return int(result)
        return None

client = redis.StrictRedis()
cache = CachePi(client)

@app.route('/pi')
def pi():
    n = int(request.args.get('n', '100'))
    if cache.get_pi(n):
        print('get pi from cache')
        return jsonify({'cached': True, 'result': cache.get_pi(n)})
    print('start to calculate pi')
    temp = 0.0
    for i in range(1, n):
        temp += 1 / (i * i)
    p = str(math.sqrt(temp * 6))
    cache.set_pi(n, p)
    return jsonify({'cached': False, 'result': p})

@app.route('/fib')
def fib():
    n = int(request.args.get('n', '10'))
    result, cached = calc_fib(n)
    return jsonify({'cached': cached, 'result': result})

def calc_fib(n):
    if n == 0:
        return 0, True
    if n == 1:
        return 1, True
    result = cache.get_fib(n)
    if result:
        return result, True
    result = calc_fib(n-1)[0] + calc_fib(n-2)[0]
    cache.set_fib(n, result)
    return result, False


if __name__ == '__main__':
    app.run('127.0.0.1', 5000)