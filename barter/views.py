from django.shortcuts import render, redirect, get_object_or_404
from .models import Ad, Category, ExchangeProposal
from .forms import AdForm, ExchangeProposal
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import login as auth_login

def home(request):
    q = request.GET.get('q')
    category = request.GET.get('category')
    condition = request.GET.get('condition')

    ads = Ad.objects.all()
    if q:
        ads = ads.filter(title__icontains=q)
    if category:
        ads = ads.filter(category_id=category)
    if condition:
        ads = ads.filter(condition=condition)

    categories = Category.objects.all()
    return render(request, 'barter/home.html', {
        'ads': ads,
        'categories': categories
    })

@login_required
def my_ads(request):
    myads = Ad.objects.filter(user=request.user)
    return render(request, 'barter/my_ads.html', {'ads': myads})

@login_required
def ad_create(request):
    if request.method == 'POST':
        form = AdForm(request.POST, request.FILES)
        if form.is_valid():
            ad = form.save(commit=False)
            ad.user = request.user
            ad.save()
            return redirect('my_ads')
    else:
        form = AdForm()
    return render(request, 'barter/ad_create.html', {'form': form})
    
def ad_detail(request, pk):
    ad = get_object_or_404(Ad, pk=pk)
    images = ad.images.all()
    context = {'ad': ad, 'images': images}
    # Добавляем свои объявления для возможности обмена, если пользователь залогинен и просматривает не своё объявление
    if request.user.is_authenticated and request.user != ad.user:
        context['my_ads'] = Ad.objects.filter(user=request.user)
    else:
        context['my_ads'] = ""
        print('addetail called', pk, context)
    return render(request, 'barter/ad_detail.html', context)

@login_required
def ad_edit(request, pk):
    ad = get_object_or_404(Ad, pk=pk)
    if ad.user != request.user:
        messages.error(request, "Вы не можете редактировать это объявление, так как не являетесь его автором.")
        return redirect('my_ads')

    if request.method == 'POST':
        form = AdForm(request.POST, request.FILES, instance=ad)
        if form.is_valid():
            form.save()
            messages.success(request, "Объявление успешно обновлено!")
            return redirect('my_ads')
    else:
        form = AdForm(instance=ad)

    return render(request, 'barter/ad_edit.html', {'form': form, 'ad': ad})

@login_required
def ad_delete(request, pk):
    ad = get_object_or_404(Ad, pk=pk, user=request.user)
    if request.method == 'POST':
        ad.delete()
        return redirect('my_ads')
    return render(request, 'barter/ad_confirm_delete.html', {'ad': ad})

@login_required
def my_exchange_proposals(request):
    tab = request.GET.get('tab', 'incoming')
    if tab == 'incoming':
        proposals = ExchangeProposal.objects.filter(ad_receiver__user=request.user)
    elif tab == 'outgoing':
        proposals = ExchangeProposal.objects.filter(ad_sender__user=request.user)
    else:
        proposals = []
    return render(request, 'barter/my_exchange_proposals.html', {
        'proposals': proposals,
        'tab': tab
    })

@login_required
def accept_exchange_proposal(request, proposal_id):
    proposal = get_object_or_404(ExchangeProposal, id=proposal_id, ad_receiver__user=request.user)
    proposal.status = 'accepted'
    proposal.save()
    # Здесь по желанию можно добавить дополнительные действия (например, больше не разрешать обмениваться этим объявлением)
    return redirect('my_exchange_proposals')

@login_required
def decline_exchange_proposal(request, proposal_id):
    proposal = get_object_or_404(ExchangeProposal, id=proposal_id, ad_receiver__user=request.user)
    proposal.status = 'declined'
    proposal.save()
    return redirect('my_exchange_proposals')

@login_required
def propose_exchange(request, ad_receiver_id):
    ad_receiver = get_object_or_404(Ad, pk=ad_receiver_id)
    if ad_receiver.user == request.user:
        messages.error(request, "Вы не можете предложить обмен на своё объявление.")
        return redirect('ad_detail', pk=ad_receiver_id)
    
    myads = Ad.objects.filter(user=request.user)
    if request.method == "POST":
        myadid = request.POST.get('ad_sender')
        comment = request.POST.get('comment') 
        myad = get_object_or_404(Ad, pk=myadid, user=request.user)
        
        alreadyproposed = ExchangeProposal.objects.filter(
            ad_sender=myad, ad_receiver=ad_receiver, status='pending'
        ).exists()
        if alreadyproposed:
            messages.warning(request, "Вы уже отправили заявку на обмен этим объявлением.")
            return redirect('ad_detail', pk=ad_receiver_id)
        
        # Сохраняем предложение обмена с комментариями
        ExchangeProposal.objects.create(
            ad_sender=myad,
            ad_receiver=ad_receiver,
            status='pending',
            comment=comment  # Сохраняем комментарий
        )
        messages.success(request, "Заявка на обмен успешно отправлена!")
        return redirect('ad_detail', pk=ad_receiver_id)
    
    return render(request, "barter/propose_exchange.html", {
        'ad_receiver': ad_receiver,
        'my_ads': myads
    })

def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Вы успешно зарегистрировались! Теперь вы можете войти.")
            return redirect('login')
    else:
        form = UserCreationForm()
    return render(request, 'registration/register.html', {'form': form})

def login_view(request):
    if request.method == "POST":
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            auth_login(request, user)
            return redirect('home')
        else:
            messages.error(request, "Такой пользователь не зарегистрирован или неверный пароль.")
    else:
        form = AuthenticationForm()
    return render(request, 'registration/login.html', {'form': form})

@login_required
def my_sent_proposals(request):
    proposals = ExchangeProposal.objects.filter(ad_sender__user=request.user)

    # Получаем параметры фильтрации из GET-запроса
    status = request.GET.get('status')
    sender = request.GET.get('sender')
    receiver = request.GET.get('receiver')

    # Фильтрация по статусу
    if status:
        proposals = proposals.filter(status=status)
    # Фильтрация по отправителю (по имени пользователя)
    if sender:
        proposals = proposals.filter(ad_sender__user__username__icontains=sender)
    # Фильтрация по получателю (по имени пользователя)
    if receiver:
        proposals = proposals.filter(ad_receiver__user__username__icontains=receiver)

    print("== МОИ ЗАЯВКИ ==", proposals.count())
    for p in proposals:
        print(
            'sender:', p.ad_sender.user,
            '| receiver:', p.ad_receiver.user,
            '| status:', p.status
        )

    return render(
        request,
        'barter/my_sent_proposals.html',
        {
            'proposals': proposals,
            'selected_status': status or '',
            'selected_sender': sender or '',
            'selected_receiver': receiver or ''
        }
    )