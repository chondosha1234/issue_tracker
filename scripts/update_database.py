from issues.models import Issue

priority_map = {
    'HIGH': 3,
    'MED': 2,
    'LOW': 1,
}

for obj in Issue.objects.all():
    obj.priority = priority_map[obj.priority]
    obj.save()
