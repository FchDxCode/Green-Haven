from django.contrib import admin
from .models import Guides, ImageGuides
from unfold.admin import ModelAdmin
from analytics.models import CustomEvent
from django.utils import timezone
import uuid

class GuideEventTracker:
    @staticmethod
    def track_event(event_name, user, guide, action=None, metadata=None):
        CustomEvent.objects.create(
            event_name=event_name,
            event_category='guide',
            user_id=user.id if user else None,
            user_type='staff' if user and user.is_staff else 'user',
            session_id=str(uuid.uuid4()),
            event_value={
                'guide_id': guide.id if guide else None,
                'guide_title': guide.title if guide else None,
                'action': action,
                'timestamp': timezone.now().isoformat()
            },
            source='admin',
            metadata=metadata or {}
        )

class ImageGuidesInline(admin.TabularInline):
    model = ImageGuides
    extra = 1

@admin.register(Guides)
class GuidesAdmin(ModelAdmin):
    list_display = ('title', 'slug', 'created_at', 'updated_at')
    search_fields = ('title', 'slug')
    prepopulated_fields = {'slug': ('title',)}
    inlines = [ImageGuidesInline]

    def save_model(self, request, obj, form, change):
        super().save_model(request, obj, form, change)
        # Track guide creation/update
        event_name = 'guide_updated' if change else 'guide_created'
        metadata = {
            'changed_fields': form.changed_data if change else None,
            'admin_user': request.user.username,
        }
        
        GuideEventTracker.track_event(
            event_name=event_name,
            user=request.user,
            guide=obj,
            action='update' if change else 'create',
            metadata=metadata
        )

    def delete_model(self, request, obj):
        # Track single guide deletion
        GuideEventTracker.track_event(
            event_name='guide_deleted',
            user=request.user,
            guide=obj,
            action='delete',
            metadata={'admin_user': request.user.username}
        )
        super().delete_model(request, obj)

    def delete_queryset(self, request, queryset):
        # Track bulk deletion
        for obj in queryset:
            GuideEventTracker.track_event(
                event_name='guide_deleted',
                user=request.user,
                guide=obj,
                action='bulk_delete',
                metadata={'admin_user': request.user.username}
            )
        super().delete_queryset(request, queryset)

    def save_formset(self, request, form, formset, change):
        # Track inline changes (images)
        instances = formset.save(commit=False)
        
        # Track added/updated images
        for obj in instances:
            if isinstance(obj, ImageGuides):
                event_name = 'guide_image_updated' if obj.pk else 'guide_image_added'
                GuideEventTracker.track_event(
                    event_name=event_name,
                    user=request.user,
                    guide=obj.guides,
                    action='update_image' if obj.pk else 'add_image',
                    metadata={
                        'admin_user': request.user.username,
                        'image_id': obj.pk
                    }
                )
        
        # Track deleted images
        for obj in formset.deleted_objects:
            if isinstance(obj, ImageGuides):
                GuideEventTracker.track_event(
                    event_name='guide_image_deleted',
                    user=request.user,
                    guide=obj.guides,
                    action='delete_image',
                    metadata={
                        'admin_user': request.user.username,
                        'image_id': obj.pk
                    }
                )
        
        super().save_formset(request, form, formset, change)

@admin.register(ImageGuides)
class ImageGuidesAdmin(ModelAdmin):
    list_display = ('guides', 'image', 'created_at', 'updated_at')
    list_filter = ('guides',)

    def save_model(self, request, obj, form, change):
        super().save_model(request, obj, form, change)
        # Track image addition/update
        event_name = 'guide_image_updated' if change else 'guide_image_added'
        
        GuideEventTracker.track_event(
            event_name=event_name,
            user=request.user,
            guide=obj.guides,
            action='update_image' if change else 'add_image',
            metadata={
                'admin_user': request.user.username,
                'image_id': obj.id
            }
        )

    def delete_model(self, request, obj):
        # Track image deletion
        GuideEventTracker.track_event(
            event_name='guide_image_deleted',
            user=request.user,
            guide=obj.guides,
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
            GuideEventTracker.track_event(
                event_name='guide_image_deleted',
                user=request.user,
                guide=obj.guides,
                action='bulk_delete_image',
                metadata={
                    'admin_user': request.user.username,
                    'image_id': obj.id
                }
            )
        super().delete_queryset(request, queryset)