#!bin/python
import imp
from migrate.versioning import api
from app import app, db
db_repo = app.config['SQLALCHEMY_MIGRATE_REPO']
db_uri = app.config['SQLALCHEMY_DATABASE_URI']
migration = db_repo + '/versions/%03d_migration.py' % (api.db_version(db_uri, db_repo) + 1)
tmp_module = imp.new_module('old_model')
old_model = api.create_model(db_uri, db_repo)
exec old_model in tmp_module.__dict__
script = api.make_update_script_for_model(db_uri, db_repo, tmp_module.meta, db.metadata)
open(migration, "wt").write(script)
api.upgrade(db_uri, db_repo)
print 'New migration saved as ' + migration
print 'Current database version: ' + str(api.db_version(db_uri, db_repo))

