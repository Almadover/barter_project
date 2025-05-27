from django.contrib import admin
from .models import Category, Ad, ExchangeProposal

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('id', 'name')
    search_fields = ('name',)

@admin.register(Ad)
class AdAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'user', 'category', 'condition', 'created_at')
    search_fields = ('title', 'description')
    list_filter = ('category', 'condition', 'created_at')
    raw_id_fields = ('user',)

@admin.register(ExchangeProposal)
class ExchangeProposalAdmin(admin.ModelAdmin):
    list_display = ('id', 'ad_sender', 'ad_receiver', 'status', 'created_at')
    list_filter = ('status', 'created_at')
    search_fields = ('comment',)
