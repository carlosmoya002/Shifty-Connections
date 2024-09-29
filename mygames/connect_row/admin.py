from django.contrib import admin
from .models import Vocabulary, Connection, Game

@admin.register(Vocabulary)
class VocabularyAdmin(admin.ModelAdmin):
    list_display = ('word',)

@admin.register(Connection)
class ConnectionsAdmin(admin.ModelAdmin):
    list_display = ('description', 'word1', 'word2', 'word3', 'word4', 'difficulty')

admin.site.register(Game)

# @admin.register(Game)
# class GamesAdmin(admin.ModelAdmin):
#     list_display = ('id', 'connection1', 'connection2', 'connection3', 'connection4', 'difficulty', 'created_at')
