# -*- coding: utf-8 -*-
from datetime import datetime
from persistent.dict import PersistentDict
from plone import api
from plone.z3cform.layout import wrap_form
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile
from rer.newsletter import _
from rer.newsletter import logger
from rer.newsletter.content.channel import Channel
from rer.newsletter.utility.channel import IChannelUtility
from rer.newsletter.utility.channel import OK
from rer.newsletter.utils import addToHistory
from rer.newsletter.utils import get_site_title
from six.moves.urllib.parse import urlencode
from z3c.form import button
from z3c.form import form
from zope.annotation.interfaces import IAnnotations
from zope.component import getUtility
from zope.component import queryUtility


try:
    from collective.taskqueue.interfaces import ITaskQueue
    from rer.newsletter.queue.handler import QUEUE_NAME
    from rer.newsletter.queue.interfaces import IMessageQueue

    HAS_TASKQUEUE = True
except ImportError:
    HAS_TASKQUEUE = False


KEY = 'rer.newsletter.message.details'


class SendMessageView(form.Form):

    ignoreContext = True

    def _getNewsletter(self):
        channel = None
        for obj in self.context.aq_chain:
            if isinstance(obj, Channel):
                channel = obj
                break
        else:
            if not channel:
                return
        return channel

    def getUserNumber(self):
        channel = self._getNewsletter()

        api_channel = getUtility(IChannelUtility)
        active_users, status = api_channel.getNumActiveSubscribers(
            channel.id_channel
        )
        if status == OK:
            return active_users
        else:
            return 0

    @button.buttonAndHandler(_('send_sendingview', default='Send'))
    def handleSave(self, action):
        channel = self._getNewsletter()
        api_channel = getUtility(IChannelUtility)
        active_users, status = api_channel.getNumActiveSubscribers(
            channel.id_channel
        )
        if HAS_TASKQUEUE:
            messageQueue = queryUtility(IMessageQueue)
            isQueuePresent = queryUtility(ITaskQueue, name=QUEUE_NAME)
            if isQueuePresent is not None and messageQueue is not None:
                # se non riesce a connettersi con redis allora si spacca
                messageQueue.start(self.context)
            else:
                # invio sincrono del messaggio
                self.send_syncronous(
                    api_channel=api_channel,
                    status=status,
                    active_users=active_users,
                )
        else:
            # invio sincrono del messaggio
            self.send_syncronous(
                api_channel=api_channel,
                status=status,
                active_users=active_users,
            )

        # cambio di stato dopo l'invio
        # api.content.transition(obj=self.context, transition='send')

        # self.request.response.redirect('view')
        self.request.response.redirect(
            '@@send_success_view?' + urlencode({'active_users': active_users})
        )
        api.portal.show_message(
            message=_(
                u'message_send',
                default=u'Il messaggio è stato '
                'inviato a {0} iscritti al canale'.format(active_users),
            ),
            request=self.request,
            type=u'info',
        )

    def send_syncronous(self, api_channel, status, active_users):
        channel = self._getNewsletter()
        # preparo il messaggio
        unsubscribe_footer_template = self.context.restrictedTraverse(
            '@@unsubscribe_channel_template'
        )
        parameters = {
            'portal_name': get_site_title(),
            'channel_name': channel.title,
            'unsubscribe_link': channel.absolute_url() + '/@@unsubscribe',
        }
        unsubscribe_footer_text = unsubscribe_footer_template(**parameters)
        api_channel.sendMessage(
            channel.id_channel, self.context, unsubscribe_footer_text
        )

        # i dettagli sull'invio del messaggio per lo storico
        annotations = IAnnotations(self.context)
        if KEY not in list(annotations.keys()):
            annotations[KEY] = PersistentDict({})

        annotations = annotations[KEY]
        now = datetime.today().strftime('%d/%m/%Y %H:%M:%S')

        if status != OK:
            logger.warning('Problems...{0}'.format(status))
            api.portal.show_message(
                message=u'Problemi con l\'invio del messaggio. '
                'Contattare l\'assistenza.',
                request=self.request,
                type=u'error',
            )
            return

        annotations[
            self.context.title + str(len(list(annotations.keys())))
        ] = {'num_active_subscribers': active_users, 'send_date': now}
        addToHistory(self.context, active_users)


message_sending_view = wrap_form(
    SendMessageView, index=ViewPageTemplateFile('templates/sendmessageview.pt')
)
