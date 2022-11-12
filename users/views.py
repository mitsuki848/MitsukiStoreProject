from django.shortcuts import render, redirect
from users.forms import CustomUserCreationForm
from django.contrib.auth import authenticate, login


def signup(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        # 検証
        if form.is_valid():
            # モデルに保存
            form.save()
            input_email = form.cleaned_data['email']
            input_password = form.cleaned_data['password1']
            # ユーザー認証：emailとpasswordでユーザーを特定しnew_userに代入
            new_user = authenticate(
                email=input_email,
                password=input_password,
            )
            if new_user is not None:
                # new_userでログイン
                login(request, new_user)
                # urlpatternsにあるindexのviewを呼び出す
                return redirect('main:index')

        context = {'form': form}
        return render(request, template_name='users/signup.html',
                      context=context)

    form = CustomUserCreationForm()
    context = {'form': form}
    return render(request, template_name='users/signup.html', context=context)
