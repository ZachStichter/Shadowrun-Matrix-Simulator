def load_dotenv():
    from dotenv import load_dotenv as load
    from os.path import join, dirname, isfile
    secret_location = join(dirname(__file__),'.env.secret')
    env_location = join(dirname(__file__),'.env.public')
    config_location = join(dirname(__file__),'.env.config')
    values = locals().copy()
    for _ in values:
        if _.endswith('_location') and isfile(values[_]):
            load(values[_])

if __name__ == '__main__':
    load_dotenv()