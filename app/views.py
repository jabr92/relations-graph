from flask import render_template
from flask_appbuilder import ModelView
from flask_appbuilder.models.sqla.interface import SQLAInterface

from . import appbuilder, db
from .models import *


class EntityModelView(ModelView):
    datamodel = SQLAInterface(Entity)
    list_columns = ["title", "first_name", "last_name", "status", "entity_type"]
    show_columns = ["title", "first_name", "last_name", "status", "entity_type"]
    add_columns = ["title", "first_name", "last_name", "status", "entity_type"]
    edit_columns = ["title", "first_name", "last_name", "status", "entity_type"]


@appbuilder.app.errorhandler(404)
def page_not_found(e):
    return (
        render_template(
            "404.html", base_template=appbuilder.base_template, appbuilder=appbuilder
        ),
        404,
    )


db.create_all()

appbuilder.add_view(
    EntityModelView,
    "List Datacenters",
    icon="fa-folder-open-o",
    category="Datacenters",
    category_icon="fa-envelope",
)
