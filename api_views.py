from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
import json
from .models import SmartBin
from .utils import notify_bin_full

@csrf_exempt
@require_http_methods(["POST"])
def bin_status_update(request):
    """API endpoint for IoT devices to update bin status"""
    try:
        data = json.loads(request.body)
        bin_id = data.get('bin_id')
        fill_percentage = data.get('fill_percentage')
        
        if not bin_id or fill_percentage is None:
            return JsonResponse({'error': 'Missing required fields'}, status=400)
        
        try:
            bin = SmartBin.objects.get(bin_id=bin_id)
            bin.update_status(fill_percentage)
            
            # Send notification if bin is 75% or more full
            if fill_percentage >= 75:
                notify_bin_full(bin)
            
            return JsonResponse({
                'success': True,
                'bin_id': bin_id,
                'status': bin.status,
                'fill_percentage': fill_percentage
            })
        except SmartBin.DoesNotExist:
            return JsonResponse({'error': 'Bin not found'}, status=404)
    
    except json.JSONDecodeError:
        return JsonResponse({'error': 'Invalid JSON'}, status=400)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)

@require_http_methods(["GET"])
def bin_status_detail(request, bin_id):
    """Get current status of a bin"""
    try:
        bin = SmartBin.objects.get(bin_id=bin_id)
        return JsonResponse({
            'bin_id': bin.bin_id,
            'status': bin.status,
            'fill_percentage': bin.fill_percentage,
            'location': bin.location,
            'last_collection': bin.last_collection_date.isoformat() if bin.last_collection_date else None,
            'next_collection': bin.next_collection_date.isoformat() if bin.next_collection_date else None,
        })
    except SmartBin.DoesNotExist:
        return JsonResponse({'error': 'Bin not found'}, status=404)
