from django.contrib import admin
from .models import Visitor

# class CustomVisitorAdmin(UserAdmin):
#     model = Visitor
#     list_display = ('')
#     list_filter = ('')
#     search_fields = ('')

# admin.site.register(Visitor, VisitorAdmin)
admin.site.register(Visitor)