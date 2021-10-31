from django.contrib import admin

from . models import author, category, article, comment

class authorModel(admin.ModelAdmin):
    list_display = ["__str__"]
    search_fields = ["__str__","details"]
    class Meta:
        Model = author

admin.site.register(author, authorModel)

class articleModel(admin.ModelAdmin):
    list_display = ["__str__", "created_at"]
    search_fields = ["__str__","details"]
    list_per_page = 10
    list_filter = ["created_at", "category"]
    class Meta:
        Model = article


admin.site.register(article, articleModel)

class categoryModel(admin.ModelAdmin):
    list_display = ["__str__"]
    search_fields = ["__str__"]
    list_per_page = 10
    class Meta:
        Model = category

admin.site.register(category, categoryModel)


class commentModel(admin.ModelAdmin):
    list_display = ["__str__"]
    search_fields = ["__str__"]
    list_per_page = 10
    class Meta:
        Model = comment
        
admin.site.register(comment, commentModel)

