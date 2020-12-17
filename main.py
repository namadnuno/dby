from Migrator import Migrator
import yaml

if __name__ == "__main__":
    with open(r'examples/sample.yaml') as file:
        spec = yaml.load(file, Loader=yaml.FullLoader)
        
        Migrator(spec).migrate()