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


class EntityRelationModelView(ModelView):
    datamodel = SQLAInterface(EntityRelation)
    list_columns = ["source_entity", "relation", "target_entity", "mutual"]
    show_columns = ["source_entity", "relation", "target_entity", "mutual"]
    add_columns = ["source_entity", "relation", "target_entity", "mutual"]
    edit_columns = ["source_entity", "relation", "target_entity", "mutual"]


@appbuilder.app.errorhandler(404)
def page_not_found(e):
    return (
        render_template(
            "404.html", base_template=appbuilder.base_template, appbuilder=appbuilder
        ),
        404,
    )


db.create_all()


views = {
    "Datacenters": ("fa-database", [
        (EntityModelView,  "List Datacenters"),
        (EntityRelationModelView, "List Datacenter Relations"),
    ]),

}

for category, views in views.items():
    icon = views[0]
    for view in views[1]:
        appbuilder.add_view(view[0], view[1], category_icon=icon, category=category)
