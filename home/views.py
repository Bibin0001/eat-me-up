from django.shortcuts import render, redirect

from accounts.views import check_if_user_has_completed_the_profile


# Create your views here.
def index(request):
    user = request.user
    if user.is_authenticated:
        account = check_if_user_has_completed_the_profile(user)

        if not account:
            return redirect('account creation page')

        return render(request, 'home/index.html', context={"user": request.user, 'account': account})
    return render(request, 'home/index.html', context={"user": request.user})
