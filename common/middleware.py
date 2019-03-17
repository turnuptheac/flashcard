"""
Custom middleware
"""


class WebfactionFixes(object):
    """
    On WebFaction each host has its own Apache instance, with WebFaction's main
    Nginx instance forwarding request. So when a Django application's Apache
    instance proxies requests to Django, the `REMOTE_ADDR` header is not set
    with  the client's IP address. Instead, the IP address is available as the
    first IP address in the comma separated list in the `HTTP_X_FORWARDED_FOR`
    header.

    This middleware fixes this by automatically setting `REMOTE_ADDR` to the
    value of `HTTP_X_FORWARDED_FOR`

    Note:
        This middleware should be installed at the top of your list to restore
        the lost info.

    Ref:
        https://docs.webfaction.com/software/django/troubleshooting.html#accessing-remote-addr
    """
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # Code to be executed for each request before the view
        # (and later middleware) are called
        self.process_request(request)

        response = self.get_response(request)

        # Code to be executed for each request/response after the view is called
        # N/A

        return response

    def process_request(self, request):
        """
        Set's `REMOTE_ADDR` based on `HTTP_X_FORWARDED_FOR`, if the latter is
        set.

        Args:
            request: HttpRequest object

        Returns:
            None, which allows Django to continue processing this request and
            execute other process_request() middleware.
        """
        if 'HTTP_X_FORWARDED_FOR' in request.META:
            ip = request.META['HTTP_X_FORWARDED_FOR'].split(',')[0].strip()
            request.META['REMOTE_ADDR'] = ip
