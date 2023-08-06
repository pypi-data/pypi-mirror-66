
from django.db import models
from django.conf import settings
from django.utils.translation import ugettext_lazy as _


class Feedback(models.Model):

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        verbose_name=_('User'),
        blank=True,
        null=True,
        on_delete=models.SET_NULL)

    subject = models.CharField(_("Subject"), max_length=255)

    name = models.CharField(_("Name"), max_length=255, blank=True)

    mobile = models.CharField(_("Mobile"), max_length=255, blank=True)

    email = models.EmailField(_("Email"), max_length=255, blank=True)

    date_created = models.DateTimeField(
        _('Date created'), auto_now_add=True, editable=False)

    text = models.TextField(_('Message text'), max_length=4096)

    def __str__(self):
        return self.subject

    class Meta:
        verbose_name = _('Feedback message')
        verbose_name_plural = _('Feedback messages')
