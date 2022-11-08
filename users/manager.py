from django.contrib.auth.base_user import BaseUserManager

class CustomUserManager(BaseUserManager):

    def create_user(self, first_name, last_name, email, password=None):
        if email:
            email = self.normalize_email(email)
        else:
            raise ValueError('Email must be set.')
        user = self.model(
            email=email,
             first_name=first_name,
             last_name=last_name)

        user.set_password(password)
        # user.is_active = True
        user.save()
        return user

    
    def create_superuser(self, first_name, last_name, email, password=None):
        user=self.create_user(first_name, last_name, email, password=None)
        user.is_staff=True
        user.is_superuser=True
        user.save()
        return user