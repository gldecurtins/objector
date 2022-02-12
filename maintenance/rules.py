import rules


@rules.predicate
def is_object_owner(user, obj):
    return obj.object.owner == user


@rules.predicate
def is_object_manager(user, obj):
    return obj.object.management_team is not None and rules.is_group_member(
        str(obj.object.management_team)
    )


@rules.predicate
def is_object_maintainer(user, obj):
    return obj.object.maintenance_team is not None and rules.is_group_member(
        str(obj.object.maintenance_team)
    )


rules.add_perm(
    "maintenance.add_task",
    (is_object_owner | is_object_manager),
)
rules.add_perm(
    "maintenance.view_task",
    (is_object_owner | is_object_manager | is_object_maintainer),
)
rules.add_perm("maintenance.change_task", is_object_owner)
rules.add_perm("maintenance.delete_task", is_object_owner)

rules.add_perm(
    "maintenance.add_journal",
    (is_object_owner | is_object_manager | is_object_maintainer),
)
rules.add_perm(
    "maintenance.view_journal",
    (is_object_owner | is_object_manager | is_object_maintainer),
)
rules.add_perm("maintenance.change_journal", is_object_owner)
rules.add_perm("maintenance.delete_journal", is_object_owner)

rules.add_perm(
    "maintenance.add_trigger",
    (is_object_owner | is_object_manager | is_object_maintainer),
)
rules.add_perm(
    "maintenance.view_trigger",
    (is_object_owner | is_object_manager | is_object_maintainer),
)
rules.add_perm("maintenance.change_trigger", is_object_owner)
rules.add_perm("maintenance.delete_trigger", is_object_owner)
