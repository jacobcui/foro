from django.contrib.auth.models import User


if __name__ == '__main__':
    user = User.objects.create_user('jacob', 'jacob.tsui@loankit.com.au', 'qweasdzxc')

    user.last_name = 'CUI'
    user.first_name = 'Jacob'

    user.save()
