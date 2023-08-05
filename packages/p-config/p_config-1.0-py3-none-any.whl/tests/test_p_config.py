import os

from p_config import Config

base_dir = os.path.dirname(os.path.abspath(__file__))


def test_default():
    config = Config(os.path.join(base_dir, 'default.yml'))
    assert config['server.port'] == 80
    assert config['server.hostname'] == 'localhost'
    assert config['dbs.mysql.hostname'] == 'localhost'
    assert config['dbs.mysql.port'] == 3306
    assert config['dbs.mysql.options.charset'] == 'utf8mb4'
    assert config['hostnames'] == ['demo.com']
    assert config['nodes'] == ['127.0.0.2', '127.0.0.3']
    # test upper case
    assert config['DBS.MYSQL.OPTIONS.CHARSET'] == 'utf8mb4'
    # test title case
    assert config['Dbs.Mysql.Options.Charset'] == 'utf8mb4'

    try:
        config['server.unknow']
        raise Exception('expect KeyError')
    except KeyError:
        pass


def test_override_yaml():
    config = Config(os.path.join(base_dir, 'default.yml'))
    config.load(os.path.join(base_dir, 'override.yml'))

    assert config['server.port'] == 8080
    assert config['server.hostname'] == 'localhost'
    assert config['dbs.mysql.hostname'] == 'online.com'
    assert config['dbs.mysql.port'] == 3308
    assert config['dbs.mysql.options.charset'] == 'utf8'
    assert config['dbs.mysql.options.timeout'] == 1000
    assert config['dbs.postgresql.hostname'] == 'online.com'
    assert config['dbs.postgresql.username'] == 'root'
    assert config['nodes.node1'] == '127.0.0.1'
    assert config['nodes'] == {'NODE1': '127.0.0.1'}


def test_environ():
    config = Config()
    config.set_cast_func('server.port', int)

    os.environ['server.port'] = '22'
    os.environ['SERVER.hostname'] = 'demo.com'

    config.load_env()
    assert config['server.port'] == 22
    assert config['server.hostname'] == 'demo.com'

    os.environ['SERVER.PORT'] = '33'
    config.load_env()
    assert config['server.port'] == 33
