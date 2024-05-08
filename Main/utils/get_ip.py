def get_client_ip(request):
    if xff := request.META.get('HTTP_X_FORWARDED_FOR'):
        return xff.splite(',')[0]
    return request.META.get('REMOTE_ADDR')