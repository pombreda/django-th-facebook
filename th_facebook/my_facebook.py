# -*- coding: utf-8 -*-
# add here the call of any native lib of python like datetime etc.
#
# add the python API here if needed
from external_api import CallOfApi

# django classes
from django.conf import settings
from django.core.urlresolvers import reverse
from django.utils.log import getLogger

# django_th classes
from django_th.services.services import ServicesMgr
from django_th.models import UserService, ServicesActivated

"""
    handle process with facebook
    put the following in settings.py

    TH_FACEBOOK = {
        'consumer_key': 'abcdefghijklmnopqrstuvwxyz',
    }

    TH_SERVICES = (
        ...
        'th_facebook.my_facebook.ServiceFacebook',
        ...
    )

"""

logger = getLogger('django_th.trigger_happy')


class ServiceFacebook(ServicesMgr):

    def process_data(self, token, trigger_id, date_triggered):
        """
            get the data from the service
        """
        datas = list()
        return datas

    def save_data(self, token, trigger_id, **data):
        """
            let's save the data
        """
        from th_facebook.models import Facebook

        if token and 'link' in data and data['link'] is not None and len(data['link']) > 0:
            # get the data of this trigger
            trigger = Facebook.objects.get(trigger_id=trigger_id)
            # if the external service need we provide
            # our stored token and token secret then I do
            # token_key, token_secret = token.split('#TH#')

                # get the token of the external service for example
            facebook_instance = external_api.CallOfApi(
                settings.TH_FACEBOOK['consumer_key'], token)

            title = ''
            title = (data['title'] if 'title' in data else '')
                # add data to the external service
            item_id = facebook_instance .add(
                url=data['link'], title=title, tags=(trigger.tag.lower()))

            sentance = str('facebook {} created').format(data['link'])
            logger.debug(sentance)
        else:
            logger.critical(
                "no token or link provided for trigger ID {} ".format(trigger_id))

    def auth(self, request):
        """
            let's auth the user to the Service
        """
        callbackUrl = 'http://%s%s' % (
            request.get_host(), reverse('facebook_callback'))

        request_token = CallOfApi.get_request_token(
            consumer_key=settings.TH_FACEBOOK['consumer_key'],
            redirect_uri=callbackUrl)

        # Save the request token information for later
        request.session['request_token'] = request_token

        # URL to redirect user to, to authorize your app
        auth_url = CallOfApi.get_auth_url(
            code=request_token, redirect_uri=callbackUrl)

        return auth_url

    def callback(self, request):
        """
            Called from the Service when the user accept to activate it
        """

        try:
            # finally we save the user auth token
            # As we already stored the object ServicesActivated
            # from the UserServiceCreateView now we update the same
            # object to the database so :
            # 1) we get the previous objet
            us = UserService.objects.get(
                user=request.user,
                name=ServicesActivated.objects.get(name='ServiceFacebook'))
            # 2) then get the token
            access_token = CallOfApi.get_access_token(
                consumer_key=settings.TH_FACEBOOK['consumer_key'],
                code=request.session['request_token'])

            us.token = access_token

            # if the service require us to provide
            # the access token +  access token secret then
            # here is the way I do
            # access_token = self.get_access_token(
            #    request.session['oauth_token'],
            #    request.session['oauth_token_secret'],
            #    request.GET.get('oauth_verifier', '')
            #)
            # us.token = access_token['oauth_token'] + \
            # '#TH#' + access_token['oauth_token_secret']
            # then in process_data I split on #TH# to get each one

            # 3) and save everything
            us.save()
        except KeyError:
            return '/'

        return 'facebook/callback.html'

"""
    if the external API does not provide the Oauth workflow
    here his the one to use it
    just move the next 4 line to the top of the script,
    then move the __init__ function under the Class definition
    that's it
"""
"""

    # oauth and url stuff
    import oauth2 as oauth
    import urlparse
    import urllib

    def __init__(self):
        # change those by the real URL used by the service you need
        # to read
        self.AUTH_URL = 'https://www.domain.com/api/oauth/authorize/'
        self.REQ_TOKEN = 'https://www.domain.com/api/oauth/request_token/'
        self.ACC_TOKEN = 'https://www.domain.com/api/oauth/access_token/'
        self.consumer_key = settings.TH_DUMMY['consumer_key']
        self.consumer_secret = settings.TH_DUMMY['consumer_secret']

    # Oauth Stuff
    def get_auth_url(self, request, request_token):
        return '%s?oauth_token=%s' % (
            self.AUTH_URL,
            urllib.quote(request_token['oauth_token']))

    def get_request_token(self, request, callback_url):
        client = self._get_oauth_client()
        request_url = '%s?oauth_callback=%s' % (
            self.REQ_TOKEN, urllib.quote(callback_url))

        resp, content = client.request(request_url, 'GET')
        request_token = dict(urlparse.parse_qsl(content))
        return request_token

    def get_access_token(
        self, oauth_token, oauth_token_secret, oauth_verifier
    ):
        token = oauth.Token(oauth_token, oauth_token_secret)
        token.set_verifier(oauth_verifier)
        client = self._get_oauth_client(token)

        resp, content = client.request(self.ACC_TOKEN, 'POST')
        access_token = dict(urlparse.parse_qsl(content))
        return access_token

    def _get_oauth_client(self, token=None):
        consumer = oauth.Consumer(self.consumer_key, self.consumer_secret)
        if token:
            client = oauth.Client(consumer, token)
        else:
            client = oauth.Client(consumer)
        return client

"""
