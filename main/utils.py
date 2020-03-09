

def myprojects(me):
    return ProjectUser.objects.filter(user_id_id=me.id).values_list('project_id')
