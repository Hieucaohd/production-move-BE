from flask_apispec import FlaskApiSpec


def register_view(docs: FlaskApiSpec, blueprint, views):
    bp_name = blueprint.name
    for view in views:
        docs.register(view, endpoint=f"{bp_name}.{view.__name__}")