from django.contrib import admin
from .models import Topic, Course, Student, Order, Review

def add_50_to_hours(self, request, queryset):
    for hour in queryset.all():
        queryset.update(hours=(int(hour.hours) + 10))

    add_50_to_hours.short_description = 'Add 10 Hours'

def upper_case_name(obj):
    return ("%s %s" % (obj.first_name, obj.last_name)).upper()

upper_case_name.short_description = 'Student\'s Full Name'

class CourseAdmin(admin.ModelAdmin):
    fields = [('title', 'topic'), ('price', 'num_reviews', 'hours', 'for_everyone')]
    list_display = ('title', 'topic', 'price', 'hours', 'for_everyone')
    list_filter = ('for_everyone', 'topic', 'price')
    search_fields = ('name__startswith',)
    actions = ['add_50_to_hours']

class OrderAdmin(admin.ModelAdmin):
    fields = ['courses', ('Student', 'order_status', 'order_date')]
    list_display = ('id', 'Student', 'order_status', 'order_date', 'total_items')

class StudentAdmin(admin.ModelAdmin):
    list_display = (upper_case_name, 'city')
    list_filter = ('city',)
    search_fields = ('name__startswith',)

# Register your models here.
admin.site.register(Topic)
admin.site.register(Course, CourseAdmin)
admin.site.register(Student, StudentAdmin)
admin.site.register(Order, OrderAdmin)
admin.site.register(Review)

