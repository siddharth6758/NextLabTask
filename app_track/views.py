from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from app_track.forms import AppsForm, AppsInstallForm
from app_track.models import Apps, UserAppInstall, SubCategory
from django.contrib import messages

@login_required
@csrf_exempt
def get_subcategories(request):
    category_id = request.POST.get('category_id')
    subcategories = SubCategory.objects.filter(category__id=category_id).values('id', 'sub_category')
    return JsonResponse(list(subcategories), safe=False)

@login_required
def add_app_view(request):
    if request.method == 'POST':
        try:
            app_form = AppsForm(request.POST, request.FILES)
            if app_form.is_valid():
                app_form.save()
            messages.success(request,'New App added!')
            return redirect('dashboard-user')
        except Exception as e:
            messages.error(request,f'Error while adding app! - {str(e)}')
            return redirect('dashboard-user')
    app_form = AppsForm()
    return render(request,'app_add.html',{
        'app_form':app_form
    })

@login_required
def edit_app_view(request, id):
    app_instance = get_object_or_404(Apps, id=id)
    app_form = AppsForm(request.POST, request.FILES, instance=app_instance)
    if request.method == 'POST':
        try:
            if app_form.is_valid():
                app_form.save()
            messages.success(request,'App Updated!')
            return redirect('dashboard-user')
        except Exception as e:
            messages.error(request,f'Error while updating app! - {str(e)}')
            return redirect('dashboard-user')
    else:
        app_form = AppsForm(instance=app_instance)
    return render(request,'app_edit.html',{
        'app_form':app_form
    })

@login_required
def details_app_view(request, id):
    app = get_object_or_404(Apps, id=id)
    return render(request,'app_detail.html',{
        'app':app
    })

@login_required
@csrf_exempt
def delete_app_view(request):
    try:
        id = request.POST.get('id',None)
        if id:
            app = Apps.objects.get(id=id)
            app.delete()
            messages.success(request,'App deleted successfully!')
            return JsonResponse({
                'message':'App deleted successfully!',
                'status':200
            })
    except Exception as e:
        messages.error(request, f'Error occured while deleting App: {str(e)}')
        return JsonResponse({
            'message':f'Error occured while deleting App: {str(e)}',
            'status':500
        })

@login_required
def install_app_view(request, id):
    app = Apps.objects.get(id=id)
    if request.method == 'POST':
        user = request.user
        screenshot = request.FILES.get('screenshot')
        UserAppInstall.objects.create(
            user=user,
            app=app,
            screenshot=screenshot
        )
        messages.success(request,'App Installed!')
        return redirect('dashboard-user')
    install_form = AppsInstallForm()
    return render(request,'app_install.html',{
        'install_form': install_form,
        'app': app
    })

@login_required
@csrf_exempt
def uninstall_app_view(request):
    if request.method == 'POST':
        id = request.POST.get('id',None)
        app = Apps.objects.get(id=id)
        user = request.user
        installed_app = UserAppInstall.objects.filter(user=user,app=app)
        if installed_app.exists():
            installed_app.first().delete()
            messages.success(request,'App Uninstalled!')
            return JsonResponse({
                'message':'App uninstalled successfully!',
                'status':200
            })
        else:
            messages.error(request,'App is not installed by user!')
            return JsonResponse({
                'message':'App is not installed by user!',
                'status':500
            })