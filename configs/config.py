import confuse

config = confuse.Configuration('Digital-Survey', __name__)
config.set_file('config.yml', base_for_paths=True)

databasename = config['database'].get()