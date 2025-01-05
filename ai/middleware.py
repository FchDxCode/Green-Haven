import time
import json
from .models import AIAnalytics, AIFeedbackAnalytics
import uuid

class AIAnalyticsMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if not request.path.startswith('/api/chatbot/'):
            return self.get_response(request)

        start_time = time.time()
        
        request_data = {}
        session_id = None
        
        if request.method == 'POST':
            try:
                body = request.body
                if body:
                    request._body = body
                    request_data = json.loads(body.decode('utf-8'))
                    session_id = request_data.get('session_id')
            except (json.JSONDecodeError, UnicodeDecodeError):
                pass

        if not session_id:
            session_id = f"anon_{str(uuid.uuid4())[:8]}"
        
        response = self.get_response(request)
        
        response_time = time.time() - start_time

        try:
            endpoint = request.path.split('/')[-2] if request.path.endswith('/') else request.path.split('/')[-1]

            try:
                response_data = json.loads(response.content.decode('utf-8'))
                error_message = str(response_data.get('error')) if response.status_code >= 400 else None
            except (json.JSONDecodeError, AttributeError):
                error_message = None
                
            safe_request_data = {
                'endpoint': endpoint,
                'method': request.method,
                'path': request.path,
            }
            if request_data:
                if 'message' in request_data:
                    safe_request_data['message'] = request_data['message']

            AIAnalytics.objects.create(
                session_id=session_id, 
                endpoint=endpoint,
                response_time=response_time,
                success=200 <= response.status_code < 300,
                error_message=error_message,
                ip_address=request.META.get('REMOTE_ADDR'),
                user_agent=request.META.get('HTTP_USER_AGENT'),
                request_data=safe_request_data
            )
        except Exception as e:
            print(f"Error in AIAnalyticsMiddleware: {str(e)}")

        return response 

class AIFeedbackAnalyticsMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if not request.path.startswith('/api/chatbot/feedback/'):
            return self.get_response(request)

        start_time = time.time()
        
        request_data = {}
        session_id = None
        
        if request.method == 'POST':
            try:
                body = request.body
                if body:
                    request._body = body
                    request_data = json.loads(body.decode('utf-8'))
                    session_id = request_data.get('session_id')
            except (json.JSONDecodeError, UnicodeDecodeError):
                pass

        if not session_id:
            session_id = f"anon_{str(uuid.uuid4())[:8]}"
        
        response = self.get_response(request)
        
        response_time = time.time() - start_time

        try:
            AIFeedbackAnalytics.objects.create(
                session_id=session_id,
                rating=request_data.get('rating'),
                has_comment=bool(request_data.get('comment')),
                response_time=response_time,
                ip_address=request.META.get('REMOTE_ADDR'),
                user_agent=request.META.get('HTTP_USER_AGENT')
            )
        except Exception as e:
            print(f"Error in AIFeedbackAnalyticsMiddleware: {str(e)}")

        return response 