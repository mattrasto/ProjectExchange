from django.contrib import admin

from ExchangeSite.models.websitemodels import NewsStories



class NewsAdmin(admin.ModelAdmin):
    list_display = ('story_id', 'title', 'author', 'date_entered')
    list_filter = ('date_entered',)
    date_hierarchy = 'date_entered'
    search_fields = ('title',)
    ordering = ('-story_id',)
    fields = ('type', 'title', 'content', 'author', 'date_entered')



admin.site.register(NewsStories, NewsAdmin)




