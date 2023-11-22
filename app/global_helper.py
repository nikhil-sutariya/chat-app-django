from django.http import Http404

def get_or_raise(model, obj_id, error_message):
    if obj_id:
        try:
            return model.objects.get(id=obj_id)
        except:
            raise Http404(error_message)
    return model.objects.all()