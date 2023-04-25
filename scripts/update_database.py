from issues.models import Issue

priority_map = {
    'HIGH': 3,
    'MED': 2,
    'LOW': 1,
}

for obj in Issue.objects.all():
    print(f"current object priority: {obj.priority}")
    obj.priority = priority_map[obj.priority]
    obj.save()
    print(f"new object priority: {obj.priority}")
