from celery import shared_task
from notes.models import Note
from notes.serializers import NoteCreationSerializer

@shared_task
def create_note_task(note_data):
    serializer = NoteCreationSerializer(data=note_data)
    if serializer.is_valid():
        note_instance = serializer.save()
        return {'status': 'SUCCESS', 'note_id': note_instance.id}
    else:
        raise ValueError("Invalid data")