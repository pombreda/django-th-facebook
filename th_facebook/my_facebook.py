# -*- coding: utf-8 -*-

# Facebook API
import facebook

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
        'app_id': '1234456576',
        'app_secret': 'abcdefghjkilmonpqert',
        'permissions': {'email','publish_actions','read_stream'}
    }

    TH_SERVICES = (
        ...
        'th_facebook.my_facebook.ServiceFacebook',
        ...
    )

"""

logger = getLogger('django_th.trigger_happy')


class ServiceFacebook(ServicesMgr):

    def __init__(self):
        """
            initial value
        """
        self.AUTH_URL = 'https://www.facebook.com/dialog/oauth'
        self.ACC_TOKEN = 'https://graph.facebook.com/oauth/access_token'
        self.app_id = settings.TH_FACEBOOK['app_id']
        self.consumer_secret = settings.TH_FACEBOOK['app_secret']
        self.permissions = settings.TH_FACEBOOK['permissions']


    def process_data(self, token, trigger_id, date_triggered):
        """
            get the data from the service
        """
        # TODO : get recent activity since "date_triggered"
        # https://developers.facebook.com/docs/graph-api/reference/v2.0/user/feed
        # + 
        # https://developers.facebook.com/docs/graph-api/reference/v2.0/post
        facebook_instance = facebook.GraphAPI(token)
        feed = facebook_instance.get_connections("me", "feed")
        return feed

    def save_data(self, token, trigger_id, **data):
        """
            let's save the data
        """

        if token and 'link' in data and data['link'] is not None and len(data['link']) > 0:
            # get the data of this trigger
            # right now ; just create a message on the current wall's user
            from th_facebook.models import Facebook
            trigger = Facebook.objects.get(trigger_id=trigger_id)
            sentance = ''

            message = trigger.title + ' '
            message = (data['title'] if 'title' in data else '')
            message += (data['link'] if 'link' in data else '')
            message += (data['content'] if 'content' in data else '')

            facebook_instance = facebook.GraphAPI(token)
            try:
                item_id = facebook_instance.put_wall_post(message=message)
                if item_id:
                    sentance = str('facebook {} created').format(data['link'])
            except:
                sentance = str('facebook {} creation failed').format(data['link'])

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

        # URL to redirect user to, to authorize your app
        auth_url = facebook.auth_url(app_id=self.app_id,
                                     canvas_url=callbackUrl,
                                     perms=self.permissions)

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

            access_token = facebook.get_app_access_token(
                app_secret=self.consumer_secret,
                app_id=self.app_id)

            us.token = access_token

            # 3) and save everything
            us.save()
        except KeyError:
            return '/'

        return 'facebook/callback.html'
