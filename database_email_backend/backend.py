# -*- coding: utf-8 -*-
from email.MIMEBase import MIMEBase

from django.core.mail.backends.base import BaseEmailBackend
from django.utils.encoding import smart_unicode

from database_email_backend.models import Email, Attachment


class DatabaseEmailBackend(BaseEmailBackend):
    def send_messages(self, email_messages):
        for message in email_messages:
            email = Email.objects.create(
                from_email=u'%s' % message.from_email,
                to_emails=u', '.join(message.to),
                cc_emails=u', '.join(message.cc),
                bcc_emails=u', '.join(message.bcc),
                all_recipients=u', '.join(message.recipients()),
                subject=u'%s' % message.subject,
                body=u'%s' % message.body,
                raw=u'%s' % smart_unicode(message.message().as_string()),
                reply_to=u', '.join(message.reply_to)
            )
            for attachment in message.attachments:
                if isinstance(attachment, tuple):
                    filename, content, mimetype = attachment
                elif isinstance(attachment, MIMEBase):
                    filename = attachment.get_filename()
                    content = attachment.get_payload(decode=True)
                    mimetype = None
                else:
                    continue
                Attachment.objects.create(
                    email=email,
                    filename=filename,
                    content=content,
                    mimetype=mimetype
                )
        return len(email_messages)
