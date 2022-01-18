import rules


@rules.predicate
def is_team_owner(user, obj):
    return obj.owner == user


@rules.predicate
def is_team_member(user, obj):
    return obj.group is not None and rules.is_group_member(str(obj.group))


rules.add_perm("teamapp.view_team", (is_team_owner | is_team_member))
rules.add_perm("teamapp.change_team", is_team_owner)
rules.add_perm("teamapp.delete_team", is_team_owner)
