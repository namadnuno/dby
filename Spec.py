class Spec(object):
    source_db = None
    destination_db = None
    migrations = []

    def __init__(self, source_db, destination_db, migrations): 
        self.source_db = source_db
        self.destination_db = destination_db
        self.migrations = migrations
    