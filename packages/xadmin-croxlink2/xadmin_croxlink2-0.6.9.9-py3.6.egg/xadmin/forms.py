from django import forms

from django.contrib.auth import authenticate
from django.contrib.auth.forms import AuthenticationForm

from django.utils.translation import ugettext_lazy, ugettext as _

from django.contrib.auth import get_user_model

ERROR_MESSAGE = ugettext_lazy("Please enter the correct username and password "
                              "for a staff account. Note that both fields are case-sensitive.")


class AdminAuthenticationForm(AuthenticationForm):
    """
    A custom authentication form used in the admin app.

    """
    this_is_the_login_form = forms.BooleanField(
        widget=forms.HiddenInput, initial=1,
        error_messages={'required': ugettext_lazy("Please log in again, because your session has expired.")})

    def clean(self):
        username = self.cleaned_data.get('username')
        password = self.cleaned_data.get('password')
        message = ERROR_MESSAGE

        if username and password:
            self.user_cache = authenticate(
                username=username, password=password)
            if self.user_cache is None:
                User = get_user_model()
                # check if not staff or not active
                try:
                    user = User.objects.get(username=username)

                except (User.DoesNotExist, User.MultipleObjectsReturned):
                    # Nothing to do here, moving along.
                    pass

                else:
                    if user.check_password(password):
                        message = _("This account '%s' is not authorized to login!") % user.username
                        raise forms.ValidationError(message)

                if u'@' in username:
                    # Mistakenly entered e-mail address instead of username? Look it up.
                    try:
                        user = User.objects.get(email=username,
                                                is_staff=True,
                                                is_active=True)

                    except (User.DoesNotExist, User.MultipleObjectsReturned):
                        # Nothing to do here, moving along.
                        pass

                    else:
                        if user.check_password(password):
                            message = _("Your e-mail address is not your username."
                                        " Try '%s' instead.") % user.username
                            raise forms.ValidationError(message)

                raise forms.ValidationError(message)

        return self.cleaned_data
