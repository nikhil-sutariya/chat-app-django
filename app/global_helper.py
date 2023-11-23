from django.http import Http404
from datetime import datetime

def date_formatting(self):
    # sample date format - October 19, 2023
    if 'T' in self:
        return datetime.strptime(self.split('T')[0], '%Y-%m-%d').strftime('%B %e, %Y')

def get_or_raise(model, obj_id, error_message):
    if obj_id:
        try:
            return model.objects.get(id=obj_id)
        except:
            raise Http404(error_message)
    return model.objects.all()