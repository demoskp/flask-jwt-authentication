from flask import request
from flask_query_builder.querying import QueryBuilder, AllowedFilter, AllowedSort
from flask_restful import Resource

from api.schemas.user import UserSchema
from extensions import db
from models import User


class UserList(Resource):
    def get(self):
        users = (
            QueryBuilder(User)
            .allowed_filters([
                "age",
                "email",
                AllowedFilter.partial("name"),
            ])
            .allowed_sorts([
                "name",
                "email",
                "age"
            ])
            .query
            .all()
        )

        schema = UserSchema(many=True)
        return {"results": schema.dump(users)}

    def post(self):
        schema = UserSchema()
        validated_data = schema.load(request.json)

        user = User(**validated_data)
        db.session.add(user)
        db.session.commit()

        return {"msg": "User created", "user": schema.dump(user)}


class UserResource(Resource):
    def get(self, user_id):
        user = User.query.get_or_404(user_id)
        schema = UserSchema()

        return {"user": schema.dump(user)}

    def put(self, user_id):
        schema = UserSchema(partial=True)
        user = User.query.get_or_404(user_id)
        user = schema.load(request.json, instance=user)

        db.session.add(user)
        db.session.commit()

        return {"msg": "User updated", "user": schema.dump(user)}

    def delete(self, user_id):
        user = User.query.get_or_404(user_id)

        db.session.delete(user)
        db.session.commit()

        return {"msg": "User deleted"}
