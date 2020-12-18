from Spec import Spec
from DB import DB
import re

class Migrator():
    """
    This class is responsable for migrating from source to destination
    """

    spec : Spec = None

    def __init__(self, spec):
        source_db = DB(spec['source_url'], spec['source_user'], spec['source_password'], spec['source_db'])
        destination_db = DB(spec['destination_url'], spec['destination_user'], spec['destination_password'], spec['destination_db'])

        self.spec = Spec(source_db, destination_db, spec['migrations'])

    def migrate(self):
        """
        It will receive a spec config, something like 
        """
        for table in self.spec.migrations:
            self.migrateTable(table, self.spec.migrations[table])
    
    def is_from_table(self, m):
        return len(re.findall("s\.([^\.]+)\.([^\.]+)", str(m))) > 0
    
    def get_migration_info(self, m):
        regex = re.findall("s\.([^\.]+)\.([^\.]+)", m)
        return dict({
            'table': regex[0][0],
            'col': regex[0][1]
        })
    
    def has_condition(self, migration):
        return "condition" in migration.keys()
    
    def solve_condition(self, condition, data):
        or_conditions = condition.split(" or ")
        result = False
        for or_condition in or_conditions:
            or_result = True
            and_conditions = or_condition.split(" and ")
            for and_condition in and_conditions:
                m = self.get_migration_info(and_condition)
                col = m['col']
                table = m['table']
                and_condition = and_condition.replace(
                    "s." + table + "." + col, "'" + data[col] + "'")
                or_result = eval(and_condition) and or_result
            result = result or or_result
        
        return result
        

    def migrateTable(self, table, migration):
        source_tables = dict()
        source_tables_list = []
        for m in migration.values():
            if self.is_from_table(m) and isinstance(m, str):
                mdata = self.get_migration_info(m)
                d_table = mdata['table']
                d_col = mdata['col']
                if source_tables.get(d_table) == None:
                    source_tables[d_table] = [d_col]
                    source_tables_list.append(d_table)
                else: 
                    source_tables.get(d_table).append(d_col)

        data = []
        if len(source_tables_list) == 1:
            data = self.spec.source_db.select(source_tables_list[0], source_tables.get(source_tables_list[0]))
        else:
            raise NameError('The migrations can only have one table')
        
        for item in data:
            mapping = dict()
            for col in migration:
                print(type(migration[col]))
                if self.is_from_table(migration[col]) and isinstance(migration[col], str):
                    mdata = self.get_migration_info(migration[col])
                    mapping[col] = item[mdata['col']]
                elif isinstance(migration[col], dict) and self.has_condition(migration[col]):
                    mapping[col] = migration[col][self.solve_condition(
                        migration[col]['condition'], item)]
                else:
                    mapping[col] = migration[col]
            print('Inserting', mapping)
            self.spec.destination_db.insert(table, mapping)
        
        pass
