import rules


@rules.predicate
def is_object_owner(user, obj):
    return rules.is_authenticated(user) and obj.object.owner == user


@rules.predicate
def is_object_manager(user, obj):
    return (
        rules.is_authenticated(user)
        and obj.object.management_group is not None
        and rules.is_group_member(str(obj.object.management_group))
    )


@rules.predicate
def is_object_maintainer(user, obj):
    return (
        rules.is_authenticated(user)
        and obj.object.maintenance_group is not None
        and rules.is_group_member(str(obj.object.maintenance_group))
    )


@rules.predicate
def is_sensor_object_owner(user, obj):
    return rules.is_authenticated(user) and obj.sensor.object.owner == user


@rules.predicate
def is_sensor_object_manager(user, obj):
    return (
        rules.is_authenticated(user)
        and obj.sensor.object.management_group is not None
        and rules.is_group_member(str(obj.sensor.object.management_group))
    )


@rules.predicate
def is_sensor_object_maintainer(user, obj):
    return (
        rules.is_authenticated(user)
        and obj.sensor.object.maintenance_group is not None
        and rules.is_group_member(str(obj.sensor.object.maintenance_group))
    )


rules.add_perm(
    "maintenance.add_task",
    rules.is_authenticated,
)
rules.add_perm(
    "maintenance.view_task",
    (is_object_owner | is_object_manager | is_object_maintainer),
)
rules.add_perm("maintenance.change_task", is_object_owner)
rules.add_perm("maintenance.delete_task", is_object_owner)

rules.add_perm(
    "maintenance.add_journal",
    rules.is_authenticated,
)
rules.add_perm(
    "maintenance.view_journal",
    (is_object_owner | is_object_manager | is_object_maintainer),
)
rules.add_perm("maintenance.change_journal", is_object_owner)
rules.add_perm("maintenance.delete_journal", is_object_owner)

rules.add_perm(
    "maintenance.add_trigger",
    (is_sensor_object_owner | is_sensor_object_manager | is_sensor_object_maintainer),
)
rules.add_perm(
    "maintenance.view_trigger",
    (is_sensor_object_owner | is_sensor_object_manager | is_sensor_object_maintainer),
)
rules.add_perm("maintenance.change_trigger", is_sensor_object_owner)
rules.add_perm("maintenance.delete_trigger", is_sensor_object_owner)
