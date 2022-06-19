class EmployeePermissionMixin:
    def check_permissions(self, request):
        super().check_permissions(request)
        if self.request.user.type != 'BANK_EMPLOYEE':
            raise self.permission_denied(request, message='You do not have permission to access this panel')


class TraderPermissionMixin:
    def check_permissions(self, request):
        super().check_permissions(request)
        if self.request.user.type != 'TRADER':
            raise self.permission_denied(request, message='You do not have permission to access this panel')


class CardholderPermissionMixin:
    def check_permissions(self, request):
        super().check_permissions(request)
        if self.request.user.type != 'CLIENT':
            raise self.permission_denied(request, message='You do not have permission to access this panel')
