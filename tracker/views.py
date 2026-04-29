from django.shortcuts import render, redirect, get_object_or_404
from django.db.models import Sum
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, logout
from django.contrib.auth.forms import AuthenticationForm

from .forms import ExpenseForm, CustomUserForm
from .models import Expense


# ✅ HOME (Add + List + Chart)
@login_required
def add_expense(request):
    if request.method == "POST":
        form = ExpenseForm(request.POST)
        if form.is_valid():
            expense = form.save(commit=False)
            expense.user = request.user   # 🔥 link expense to user
            expense.save()
            return redirect('/')
    else:
        form = ExpenseForm()

    # ✅ Show only logged-in user's data
    expenses = Expense.objects.filter(user=request.user)

    # ✅ Chart Data
    data = expenses.values('category').annotate(total=Sum('amount'))
    categories = [item['category'] for item in data]
    totals = [item['total'] for item in data]

    return render(request, 'add_expense.html', {
        'form': form,
        'expenses': expenses,
        'categories': categories,
        'totals': totals
    })


# ✅ DELETE (only own data)
@login_required
def delete_expense(request, id):
    expense = get_object_or_404(Expense, id=id, user=request.user)
    expense.delete()
    return redirect('/')


# ✅ EDIT (only own data)
@login_required
def edit_expense(request, id):
    expense = get_object_or_404(Expense, id=id, user=request.user)

    if request.method == "POST":
        form = ExpenseForm(request.POST, instance=expense)
        if form.is_valid():
            form.save()
            return redirect('/')
    else:
        form = ExpenseForm(instance=expense)

    return render(request, 'add_expense.html', {'form': form})


# ✅ SIGNUP
def signup(request):
    if request.method == "POST":
        form = CustomUserForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('/')
    else:
        form = CustomUserForm()

    return render(request, 'signup.html', {'form': form})


# ✅ LOGIN
def user_login(request):
    if request.method == "POST":
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('/')
    else:
        form = AuthenticationForm()

    return render(request, 'login.html', {'form': form})


# ✅ LOGOUT (NEW)
@login_required
def user_logout(request):
    logout(request)
    return redirect('/login/')