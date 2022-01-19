import rules


@rules.predicate
def is_object_owner(user, obj):
    return obj.owner == user


@rules.predicate
def is_object_manager(user, obj):
    return obj.management_team is not None and rules.is_group_member(
        str(obj.management_team)
    )


@rules.predicate
def is_object_maintainer(user, obj):
    return obj.maintenance_team is not None and rules.is_group_member(
        str(obj.maintenance_team)
    )


@rules.predicate
def is_location_owner(user, obj):
    return obj.owner == user


@rules.predicate
def is_location_manager(user, obj):
    return obj.management_team is not None and rules.is_group_member(
        str(obj.management_team)
    )


@rules.predicate
def is_location_maintainer(user, obj):
    return obj.maintenance_team is not None and rules.is_group_member(
        str(obj.maintenance_team)
    )


rules.add_perm(
    "inventory.view_object",
    (is_object_owner | is_object_manager | is_object_maintainer),
)
rules.add_perm("inventory.change_object", is_object_owner | is_object_manager)
rules.add_perm("inventory.delete_object", is_object_owner)
rules.add_perm(
    "inventory.view_location",
    (is_location_owner | is_location_manager | is_location_maintainer),
)
rules.add_perm("inventory.change_location", is_location_owner | is_location_manager)
rules.add_perm("inventory.delete_location", is_location_owner | is_location_manager)
