from app.repositories.role_repository import RoleRepository

role_repo = RoleRepository()


def extract_permissions(id_role):
    role = role_repo.findById(id_role)
    if len(role["permissions"]) == 0:
        return None
    else:
        extracted_permissions = set(
            (permission["resource"], permission["actions"]) for permission in role["permissions"])
        return extracted_permissions
