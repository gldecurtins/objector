import rules


@rules.predicate
def is_work_objekt_owner(user, obj):
    return obj.object.owner == user


@rules.predicate
def is_work_objekt_manager(user, obj):
    return obj.object.management_team is not None and rules.is_group_member(
        str(obj.object.management_team)
    )


@rules.predicate
def is_work_objekt_maintainer(user, obj):
    return obj.object.maintenance_team is not None and rules.is_group_member(
        str(obj.object.maintenance_team)
    )


rules.add_perm(
    "journal.add_work",
    (is_work_objekt_owner | is_work_objekt_manager),
)
rules.add_perm(
    "journal.view_work",
    (is_work_objekt_owner | is_work_objekt_manager | is_work_objekt_maintainer),
)
rules.add_perm("journal.change_work", is_work_objekt_owner)
rules.add_perm("journal.delete_work", is_work_objekt_owner)
