import sys
sys.path.append('/usr/lib/python3/dist-packages')
import odoo
odoo.tools.config.parse_config(['-c', '/etc/odoo/odoo.conf'])
db = odoo.sql_db.db_connect('vidya')
registry = odoo.registry(db.dbname)
with registry.cursor() as cr:
    env = odoo.api.Environment(cr, odoo.SUPERUSER_ID, {})
    fields = env['res.groups']._fields.keys()
    print('Fields:')
    for f in sorted(list(fields)):
        if 'cat' in f or 'module' in f:
            print('-', f)
