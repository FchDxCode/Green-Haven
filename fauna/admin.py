from django.contrib import admin
from .models import Fauna, ImageFauna
from unfold.admin import ModelAdmin
from analytics.models import CustomEvent
from django.utils import timezone
import uuid

class FaunaEventTracker:
    @staticmethod
    def track_event(event_name, user, fauna, action=None, metadata=None):
        CustomEvent.objects.create(
            event_name=event_name,
            event_category='fauna',
            user_id=user.id if user else None,
            user_type='staff' if user and user.is_staff else 'user',
            session_id=str(uuid.uuid4()),
            event_value={
                'fauna_id': fauna.id if fauna else None,
                'fauna_title': fauna.title if fauna else None,
                'action': action,
                'timestamp': timezone.now().isoformat()
            },
            source='admin',
            metadata=metadata or {}
        )

class ImageFaunaInline(admin.TabularInline):
    model = ImageFauna
    extra = 1

@admin.register(Fauna)
class FaunaAdmin(ModelAdmin):
    list_display = ('title', 'slug', 'created_at', 'updated_at')
    search_fields = ('title', 'slug')
    prepopulated_fields = {'slug': ('title',)}
    inlines = [ImageFaunaInline]

    def save_model(self, request, obj, form, change):
        super().save_model(request, obj, form, change)
        # Track fauna creation/update
        event_name = 'fauna_updated' if change else 'fauna_created'
        metadata = {
            'changed_fields': form.changed_data if change else None,
            'admin_user': request.user.username,
        }
        
        FaunaEventTracker.track_event(
            event_name=event_name,
            user=request.user,
            fauna=obj,
            action='update' if change else 'create',
            metadata=metadata
        )

    def delete_model(self, request, obj):
        # Track single fauna deletion
        FaunaEventTracker.track_event(
            event_name='fauna_deleted',
            user=request.user,
            fauna=obj,
            action='delete',
            metadata={'admin_user': request.user.username}
        )
        super().delete_model(request, obj)

    def delete_queryset(self, request, queryset):
        # Track bulk deletion
        for obj in queryset:
            FaunaEventTracker.track_event(
                event_name='fauna_deleted',
                user=request.user,
                fauna=obj,
                action='bulk_delete',
                metadata={'admin_user': request.user.username}
            )
        super().delete_queryset(request, queryset)

    def save_formset(self, request, form, formset, change):
        # Track inline changes (images)
        instances = formset.save(commit=False)
        
        # Track added/updated images
        for obj in instances:
            if isinstance(obj, ImageFauna):
                event_name = 'fauna_image_updated' if obj.pk else 'fauna_image_added'
                FaunaEventTracker.track_event(
                    event_name=event_name,
                    user=request.user,
                    fauna=obj.fauna,
                    action='update_image' if obj.pk else 'add_image',
                    metadata={
                        'admin_user': request.user.username,
                        'image_id': obj.pk
                    }
                )
        
        # Track deleted images
        for obj in formset.deleted_objects:
            if isinstance(obj, ImageFauna):
                FaunaEventTracker.track_event(
                    event_name='fauna_image_deleted',
                    user=request.user,
                    fauna=obj.fauna,
                    action='delete_image',
                    metadata={
                        'admin_user': request.user.username,
                        'image_id': obj.pk
                    }
                )
        
        super().save_formset(request, form, formset, change)

@admin.register(ImageFauna)
class ImageFaunaAdmin(ModelAdmin):
    list_display = ('fauna', 'image', 'created_at', 'updated_at')
    list_filter = ('fauna',)

    def save_model(self, request, obj, form, change):
        super().save_model(request, obj, form, change)
        # Track image addition/update
        event_name = 'fauna_image_updated' if change else 'fauna_image_added'
        
        FaunaEventTracker.track_event(
            event_name=event_name,
            user=request.user,
            fauna=obj.fauna,
            action='update_image' if change else 'add_image',
            metadata={
                'admin_user': request.user.username,
                'image_id': obj.id
            }
        )

    def delete_model(self, request, obj):
        # Track image deletion
        FaunaEventTracker.track_event(
            event_name='fauna_image_deleted',
            user=request.user,
            fauna=obj.fauna,
            action='delete_image',
            metadata={
                'admin_user': request.user.username,
                'image_id': obj.id
            }
        )
        super().delete_model(request, obj)

    def delete_queryset(self, request, queryset):
        # Track bulk image deletion
        for obj in queryset:
            FaunaEventTracker.track_event(
                event_name='fauna_image_deleted',
                user=request.user,
                fauna=obj.fauna,
                action='bulk_delete_image',
                metadata={
                    'admin_user': request.user.username,
                    'image_id': obj.id
                }
            )
        super().delete_queryset(request, queryset)