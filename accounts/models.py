from django.db import models
from django.contrib.auth.models import User
import settings

class Profile(models.Model):
    user = models.OneToOneField(User)

    PROVIDER_CHOICES = (
        (u'vtext.net', u'Verizon'),
    )
    location = models.CharField(max_length=100)

    # Contact information
    use_email_mit = models.BooleanField(default=True)
    use_email_alt = models.BooleanField(default=False)
    email_alt = models.EmailField(
        blank = True,
    )

    use_cell = models.BooleanField(default=False)
    cell_number = models.CharField(
        max_length = 15,
        blank = True,
    )
    cell_number.helptext = "Format: 123456789"
    cell_provider = models.CharField(
        max_length = 50,
        blank = True,
        choices = PROVIDER_CHOICES
    )

    def send(self, email):
        if self.use_email_mit:
            email.to.append(self.user.email)
        if self.use_email_alt:
            email.to.append(self.email_alt)
        if self.use_cell:
            email.to.append("%s@%s" % (self.cell_number, self.cell_provider))
        email.body = """
%s,
    %s
    
--
The MOX Team. (http://mox.mit.edu/)
""" % (self.name, email.body)
        email.send()

    @property
    def name(self):
        return self.user.get_full_name()

    def __unicode__(self):
        return self.name

