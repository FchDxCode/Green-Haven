from django.contrib import admin
from .models import Kuliner, ImageKuliner
from unfold.admin import ModelAdmin
from analytics.models import CustomEvent
from django.utils import timezone
import uuid

class KulinerEventTracker:
    @staticmethod
    def track_event(event_name, user, kuliner, action=None, metadata=None):
        CustomEvent.objects.create(
            event_name=event_name,
            event_category='kuliner',
            user_id=user.id if user else None,
            user_type='staff' if user and user.is_staff else 'user',
            session_id=str(uuid.uuid4()),
            event_value={
                'kuliner_id': kuliner.id if kuliner else None,
                'kuliner_title': kuliner.title if kuliner else None,
                'action': action,
                'timestamp': timezone.now().isoformat()
            },
            source='admin',
            metadata=metadata or {}
        )

class ImageKulinerInline(admin.TabularInline):
    model = ImageKuliner
    extra = 1

@admin.register(Kuliner)
class KulinerAdmin(ModelAdmin):
    list_display = ('title', 'slug', 'created_at', 'updated_at')
    search_fields = ('title', 'slug')
    prepopulated_fields = {'slug': ('title',)}
    inlines = [ImageKulinerInline]

    def save_model(self, request, obj, form, change):
        super().save_model(request, obj, form, change)
        # Track kuliner creation/update
        event_name = 'kuliner_updated' if change else 'kuliner_created'
        metadata = {
            'changed_fields': form.changed_data if change else None,
            'admin_user': request.user.username,
        }
        
        KulinerEventTracker.track_event(
            event_name=event_name,
            user=request.user,
            kuliner=obj,
            action='update' if change else 'create',
            metadata=metadata
        )

    def delete_model(self, request, obj):
        # Track single kuliner deletion
        KulinerEventTracker.track_event(
            event_name='kuliner_deleted',
            user=request.user,
            kuliner=obj,
            action='delete',
            metadata={'admin_user': request.user.username}
        )
        super().delete_model(request, obj)

    def delete_queryset(self, request, queryset):
        # Track bulk deletion
        for obj in queryset:
            KulinerEventTracker.track_event(
                event_name='kuliner_deleted',
                user=request.user,
                kuliner=obj,
                action='bulk_delete',
                metadata={'admin_user': request.user.username}
            )
        super().delete_queryset(request, queryset)

    def save_formset(self, request, form, formset, change):
        # Track inline changes (images)
        instances = formset.save(commit=False)
        
        # Track added/updated images
        for obj in instances:
            if isinstance(obj, ImageKuliner):
                event_name = 'kuliner_image_updated' if obj.pk else 'kuliner_image_added'
                KulinerEventTracker.track_event(
                    event_name=event_name,
                    user=request.user,
                    kuliner=obj.kuliner,
                    action='update_image' if obj.pk else 'add_image',
                    metadata={
                        'admin_user': request.user.username,
                        'image_id': obj.pk
                    }
                )
        
        # Track deleted images
        for obj in formset.deleted_objects:
            if isinstance(obj, ImageKuliner):
                KulinerEventTracker.track_event(
                    event_name='kuliner_image_deleted',
                    user=request.user,
                    kuliner=obj.kuliner,
                    action='delete_image',
                    metadata={
                        'admin_user': request.user.username,
                        'image_id': obj.pk
                    }
                )
        
        super().save_formset(request, form, formset, change)

@admin.register(ImageKuliner)
class ImageKulinerAdmin(ModelAdmin):
    list_display = ('kuliner', 'image', 'created_at', 'updated_at')
    list_filter = ('kuliner',)

    def save_model(self, request, obj, form, change):
        super().save_model(request, obj, form, change)
        # Track image addition/update
        event_name = 'kuliner_image_updated' if change else 'kuliner_image_added'
        
        KulinerEventTracker.track_event(
            event_name=event_name,
            user=request.user,
            kuliner=obj.kuliner,
            action='update_image' if change else 'add_image',
            metadata={
                'admin_user': request.user.username,
                'image_id': obj.id
            }
        )

    def delete_model(self, request, obj):
        # Track image deletion
        KulinerEventTracker.track_event(
            event_name='kuliner_image_deleted',
            user=request.user,
            kuliner=obj.kuliner,
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
            KulinerEventTracker.track_event(
                event_name='kuliner_image_deleted',
                user=request.user,
                kuliner=obj.kuliner,
                action='bulk_delete_image',
                metadata={
                    'admin_user': request.user.username,
                    'image_id': obj.id
                }
            )
        super().delete_queryset(request, queryset)