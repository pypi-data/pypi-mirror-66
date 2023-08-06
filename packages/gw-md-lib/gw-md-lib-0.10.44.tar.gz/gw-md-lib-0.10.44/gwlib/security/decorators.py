import sys
import traceback
from functools import wraps

from sqlalchemy.orm.exc import NoResultFound

from gwlib.base.errors import PolicyRoleInvalid, TypeUserNotDefined
from gwlib.models import GolfCourse
from gwlib.models import User
from gwlib.services.base_policy_service import BasePolicyService
from gwlib.services.base_user_service import BaseUserService

try:
    from flask import _app_ctx_stack as ctx_stack, request, current_app, jsonify, g
except ImportError:  # pragma: no cover
    from flask import _request_ctx_stack as ctx_stack
from flask_jwt_extended import verify_jwt_in_request, get_jwt_identity


def resource_by_role(resource_name=None):
    from gwlib.security import method_to_permission

    def resource_by_role_decorator(fn):
        @wraps(fn)
        def resource_by_role_innner(*args, **kwargs):
            base_policy_service = BasePolicyService()
            base_user_service = BaseUserService()
            verify_jwt_in_request()
            current_user = get_jwt_identity()
            type_id = current_user.get("type_id")
            user_id = current_user.get("user_id")
            user = base_user_service.get_by_user_id(user_id=user_id)
            print("user", user)
            try:
                resource_permission = base_policy_service.get_resource_permissions(type_id, resource_name)
                print("resource", resource_permission)
                permission = method_to_permission.get(request.method)
            except PolicyRoleInvalid as e:
                print("Error: PolicyRoleInvalid")
                return jsonify(error=True, msg=str(e)), 403
            except TypeUserNotDefined as e:
                print("Error: TypeUserNotDefined")
                return jsonify(error=True, msg=str(e)), 403
            except NoResultFound:
                print("Error: NoResultFound")
                return jsonify(error=True, msg="Invalid User"), 403
            except Exception as e:
                traceback.print_exc(file=sys.stdout)
                print("ERROR >>>>>>>", e)
                return jsonify(error=True, msg='User not Allowed'), 403

            if not resource_permission.get(permission):
                print("PERMISION")
                return jsonify(error=True, msg='User not Allowed'), 403

            g.user = user
            print("aqui")
            # login_user(user)

            return fn(*args, **kwargs)

        return resource_by_role_innner

    return resource_by_role_decorator


def has_access_to_course(fn):
    @wraps(fn)
    def has_access_to_course_inner(*args, **kwargs):
        from gwlib.security import method_to_permission
        user = g.user  # type: User
        golf_courses = user.golf_courses  # type: [GolfCourse]
        path = request.path
        path_splited = path.split('/')
        microservice = path_splited[1]
        resource = path_splited[2]
        obj_id = path_splited[3] if len(path_splited) > 3 and path_splited[3].isnumeric() else None
        per_obj = path_splited[3] if len(path_splited) > 3 and not obj_id else None
        per_obj_id = path_splited[4] if len(path_splited) > 4 and path_splited[4].isnumeric() else None
        users = []
        holes = []
        golf_ids = []
        have_access = False
        for golf_course in golf_courses:
            golf_ids.append(golf_course.course_id)
            holes.append(golf_course.holes)
            users.extend(golf_course.users)

        permission = method_to_permission.get(request.method)
        json = request.json

        if resource == "user":
            # can access to course
            if request.method != "POST":
                if per_obj == "per_course":
                    if int(per_obj_id) in golf_ids:
                        have_access = True
                else:
                    # users can access
                    for user in users:
                        if user.user_id == int(obj_id):
                            have_access = True
            else:
                course_id = json.get("course_id")
                if course_id in golf_ids:
                    have_access = True

        elif resource == "hole":
            # can access to course
            if per_obj == "per_course":
                if int(per_obj_id) in golf_ids:
                    have_access = True
            # holes can access
            for hole in holes:
                if hole.hole_id == int(obj_id):
                    have_access = True

        elif resource == "golf_course":
            if int(obj_id) in golf_ids:
                have_access = True

        if not have_access:
            return jsonify(error=True, msg='User not Allowed'), 403

        return fn(*args, **kwargs)

    return has_access_to_course_inner
