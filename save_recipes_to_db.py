import couchdb
import os, sys
import json
import click

def load_settings():
    if 'COUCHDB_URL' not in os.environ:
        COUCHDB_URL = 'http://localhost:5984'
    else:
        COUCHDB_URL = os.environ['COUCHDB_URL']
    return COUCHDB_URL

COUCHDB_URL = load_settings()


def load_recipe(file_name):
    if not os.path.exists(file_name):
        raise OSError("Recipe not found at file location {}".format(file_name))
    with open(file_name, 'r') as f:
        d = json.load(f)

    return d


def save_recipe_to_db(db, recipe):
    db[recipe['_id']] = recipe

@click.command()
@click.option('--recipe_upload', help="Path to the recipe json file you'd like to upload")
@click.option('--recipe_delete', help="Name of recipe to delete")
def main(recipe_upload, recipe_delete):
    server = couchdb.Server(COUCHDB_URL)
    db = server['recipes']
    if recipe_delete:
        print("Deleting {} from {} database.".format(recipe_delete, COUCHDB_URL))
        if type(recipe_delete) != dict:
            recipe_delete = db[recipe_delete]
        db.delete(recipe_delete)
    if recipe_upload:
        print("Saving {} to {} database.".format(recipe_upload, COUCHDB_URL))
        recipe = load_recipe(recipe_upload)
        save_recipe_to_db(db, recipe)

if __name__ == "__main__":
    main()

