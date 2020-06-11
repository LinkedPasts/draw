from main.models import ProjectUser

def myprojects(me):
    return ProjectUser.objects.filter(user_id=me.id).values_list('project_id')
