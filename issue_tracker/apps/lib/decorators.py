# from apps.users.models import User
from apps.issues.models import Issue
from django.core.exceptions import ObjectDoesNotExist
from django.http import HttpResponseBadRequest


def get_issue_from_issueno(func):
    '''
    Decorator to get the issue from issueno argument. Checks the database for
    the issue and then passed in the resolved ORM object for the issue
    directly.

    Requires "issueno" as a keyword argument.

    -> function with the same functionality with the query for the issue already resolved.
      ex:
        def handle_route(request, issue, ...)

    Note: Proper decorator order should feature this and other DB calls last.
    '''
    def decorated(*args, **kwargs):
        try:
            kwargs['issue'] = Issue.objects.get(id=kwargs['issueno'])
            del kwargs['issueno']
        except ObjectDoesNotExist:
            return HttpResponseBadRequest("Invalid issue ID.")

        return func(*args, **kwargs)

    return decorated