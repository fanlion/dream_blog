from django.shortcuts import render, redirect
from .forms import RegisterForm


# 功能暂时取消，开发待定(URL已注销)
def register(request):
    """
    注册视图
    :param request: 
    :return: 
    """
    # 如果是POST请求
    if request.method == 'POST':
        form = RegisterForm(request.POST)

        # 如果数据通过验证
        if form.is_valid():
            form.save()

            # 注册成功去主页
            return redirect('/')
    else:
        form = RegisterForm()
    return render(request, 'users/register.html', context={'form': form})
