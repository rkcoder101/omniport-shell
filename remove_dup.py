from django.db.models import Count
from session_auth.models import SessionMap  # Replace 'your_app' with the actual app name

duplicates = (
    SessionMap.objects.values('session_key')
    .annotate(key_count=Count('id'))
    .filter(key_count__gt=1)
)
print(str(len(duplicates)) + " Duplicate Records Found")
for dup in duplicates:
    try:
        all_objs = SessionMap.objects.filter(session_key=dup['session_key']).order_by('id')
        all_objs.exclude(id=all_objs.first().id).delete()
    except Exception as e:
        print(e)
