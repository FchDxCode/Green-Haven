from django.shortcuts import render
from django.contrib.admin.views.decorators import staff_member_required
from django.db.models import Count, Avg, F, ExpressionWrapper, FloatField, Q
from django.db.models.functions import TruncDay
from django.utils import timezone
from datetime import timedelta
from .models import RequestLog
import json
import logging

# Konfigurasi logger
logger = logging.getLogger(__name__)

@staff_member_required
def analytics_dashboard_view(request):
    """View untuk menampilkan dashboard analytics"""
    try:
        # Set rentang waktu (7 hari terakhir)
        end_date = timezone.now()
        start_date = end_date - timedelta(days=7)
        
        logger.debug(f"Generating analytics for period: {start_date} to {end_date}")

        # Statistik harian
        daily_stats = (
            RequestLog.objects.filter(timestamp__gte=start_date)
            .annotate(day=TruncDay('timestamp'))
            .values('day')
            .annotate(
                total_requests=Count('id'),
                avg_response_time=Avg('response_time'),
                error_count=Count('id', filter=Q(is_error=True))
            )
            .order_by('day')
        )

        daily_stats_list = list(daily_stats)
        logger.info(f"Retrieved daily stats for {len(daily_stats_list)} days")

        # Prepare data untuk charts
        days = [stat['day'].strftime('%Y-%m-%d') for stat in daily_stats_list]
        total_requests_series = [int(stat['total_requests']) for stat in daily_stats_list]
        avg_response_times = [
            round(float(stat['avg_response_time']), 2) if stat['avg_response_time'] else 0 
            for stat in daily_stats_list
        ]

        # Convert ke JSON
        try:
            days_json = json.dumps(days)
            requests_json = json.dumps(total_requests_series)
            response_times_json = json.dumps(avg_response_times)
        except Exception as e:
            logger.error(f"JSON conversion error: {str(e)}", exc_info=True)
            days_json = json.dumps([])
            requests_json = json.dumps([])
            response_times_json = json.dumps([])

        # Calculate metrics
        total_requests_today = RequestLog.objects.filter(
            timestamp__gte=timezone.now().replace(
                hour=0, minute=0, second=0, microsecond=0
            )
        ).count()

        recent_logs = RequestLog.objects.filter(timestamp__gte=start_date)
        total_recent = recent_logs.count()
        
        context = {
            'days_json': days_json,
            'requests_json': requests_json,
            'response_times_json': response_times_json,
            'popular_endpoints': daily_stats_list,
            'total_requests_today': total_requests_today,
            'avg_response_time': recent_logs.aggregate(avg=Avg('response_time'))['avg'] or 0,
            'error_rate': (
                recent_logs.filter(is_error=True).count() / max(total_recent, 1) * 100
            ),
            'unique_users': recent_logs.values('user_id').distinct().count(),
        }

        logger.info(
            "Analytics dashboard generated successfully",
            extra={
                'total_requests': total_requests_today,
                'error_rate': context['error_rate'],
                'unique_users': context['unique_users']
            }
        )

        return render(request, 'admin/analytics/dashboard.html', context)

    except Exception as e:
        logger.error("Error generating analytics dashboard", exc_info=True)
        return render(request, 'admin/analytics/dashboard.html', {
            'error': 'Error generating analytics dashboard'
        })

