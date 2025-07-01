def admin_nama(request):
    return {
        'admin_nama': request.session.get('admin_nama')
    }