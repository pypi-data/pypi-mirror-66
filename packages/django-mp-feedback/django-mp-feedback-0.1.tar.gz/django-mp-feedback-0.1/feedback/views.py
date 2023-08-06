
from django.conf import settings
from django.apps import apps
from django.shortcuts import render
from django.http.response import HttpResponse
from django.views.generic import FormView
from django.core.mail import send_mail
from django.template.loader import render_to_string

from feedback.forms import FeedbackForm


class CreateFeedbackView(FormView):

    form_class = FeedbackForm

    def dispatch(self, request, *args, **kwargs):
        self.is_modal = request.GET.get('modal', False)
        return super().dispatch(request, *args, **kwargs)

    def get_initial(self):

        user = self.request.user

        if user.is_authenticated:
            return {
                'name': user.get_full_name(),
                'email': user.email
            }

        return self.initial

    @property
    def template_name(self):
        return 'feedback/modal.html' if self.is_modal else 'feedback/view.html'

    def form_valid(self, form):

        obj = form.save(commit=False)

        if self.request.user.is_authenticated:
            obj.user = self.request.user

        obj.save()

        self.send_email_notification(obj)
        self.send_sms_notification(obj)

        message = render_to_string(
            'feedback/success-message.html', {'object': obj})

        return HttpResponse(message)

    def form_invalid(self, form):
        return render(
            self.request,
            'feedback/form.html' if self.is_modal else 'feedback/view.html',
            {'form': form},
            status=403)

    def send_email_notification(self, obj):

        context = self.get_notifications_context(obj)

        subject = render_to_string('feedback/email/subject.txt', context)

        html = render_to_string('feedback/email/message.html', context)

        send_mail(
            subject=subject.strip(),
            message='',
            from_email=settings.DEFAULT_FROM_EMAIL,
            html_message=html,
            recipient_list=self.get_email_recipients())

    def get_email_recipients(self):
        return [a[1] for a in settings.MANAGERS]

    def send_sms_notification(self, obj):

        if not apps.is_installed('turbosms'):
            return

        from turbosms.lib import send_sms_from_template

        context = self.get_notifications_context(obj)

        send_sms_from_template('feedback/sms.txt', context)

    def get_notifications_context(self, obj):
        return {
            'object': obj,
            'site': apps.get_model('sites', 'Site').objects.get_current()
        }
