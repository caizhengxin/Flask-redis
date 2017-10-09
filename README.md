# Flask-redis


Example:

    from flask_redis import Redis
    from flask import Flask
    
    import time
    
    app = Flask(__name__)

    app.config['REDIS_URL'] = 'redis://localhost:6379/0'
    
    # redis = Redis(app)
    redis = Redis()
    redis.init_app(app)
    
    # Redis 原始命令都有，eg:
    
    # Set
    redis.set('test', 'test')
    
    # Get
    redis.get('test')
    
    # 新增命令(内置序列化、反序列化)
    
    # set_cache, 
    redis.set_cache('setcache', {"test": "python"}, 200)
    
    # get_cache
    redis.get_cache('setcache')
    
    # mset_cache, 设置许多缓存key/value
    redis.mset_cache({'c': 1, 'd': 2})
    
    # mget_cache, 获取多个缓存value
    redis.mget_cache('c', 'd')
    
    # 缓存装饰器
    @app.route('/')
    @redis.cached(timeout=5)
    def test_view():
        print(time.time())
        