from django.http import HttpRequest, HttpResponse, JsonResponse
from django.shortcuts import render

from administrator.decorators import admin_rights_required
from administrator.forms import UserRegistrationRequestsDecisionForm
from administrator.logic import _get_message_for_role_application


@admin_rights_required
def admin_page(request: HttpRequest):
    return render(
        request,
        'administrator.html',
        {
            'pending_registration_requests_form': UserRegistrationRequestsDecisionForm()
        }
    )


class RegistrationRequestReview(View):
    http_method_names = ['post']

    def post(self, request: HttpRequest):  # noqa
        pass
        # f = request.POST
        # try:
        #     registration_request = UserRegistrationRequest.objects.get(
        #         id=f['user_registration_request']
        #     )
        #     if decision.lower() == 'схвалити':
        #         UserRole(
        #             position=f['position'],
        #             access_level_id=f['access_level'],
        #             institution=registration_request.institution,
        #             user=registration_request.user
        #         ).save()
        #     elif decision.lower() == 'відмовити':
        #         registration_request.user.delete()
        #     else:
        #         return HttpResponse(status=400)
        #     registration_request.delete()
        #     return redirect('admin_page')
        # except KeyError:
        #     return HttpResponse(status=400)


@admin_rights_required
def get_message_for_registration_request(request: HttpRequest):
    if request_id := request.POST.get('request_id'):  # noqa
        return JsonResponse(
            {'message': _get_message_for_role_application(request_id)},
        )
    return HttpResponse(status=405)
