from django.shortcuts import render, redirect
from .models import Category, Income, Expense, user, Transaction, Reminder
from django.contrib.auth.models import User
from django.contrib.auth import login, logout, authenticate
from django.contrib import messages
from datetime import datetime

from django.core.validators import validate_email
from django.core.exceptions import ValidationError
from datetime import date as dt

# Create your views here.
#@login_required
def main(request):
    return render(request,"index.html")
def signup(request):
    if request.method == 'POST':
        uname = request.POST.get('username')
        uphone = request.POST.get('phone')
        email = request.POST.get('email')
        password = request.POST.get('password')
        #validtaion
        try:
            validate_email(email)
        except ValidationError:
            messages.error(request, "Invalid email format. Please enter a correct email.")
            return redirect('signuppage')

        if User.objects.filter(email=email).exists():
            print("Email Already Exist")
            messages.error(request,"Email Already Exist")
        else:
            data = user(name=uname,phone=uphone,email=email,password=password)
            data.save()

            myuser = User.objects.create_user(username=uname,email=email,password=password)
            myuser.save()
            messages.success(request, 'Register Successfully!')

    return render(request,"signup.html")

def login_account(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request,username=username, password=password)

        if user is not None:
            login(request,user)
            messages.success(request,'Login Sucessfully')
            return redirect('homepage')
        else:
            messages.error(request,"Invalid Username or Password")
            return redirect('loginpage')
            
    return render(request,"login.html")


def user_logout(request):
    logout(request)
    messages.success(request,"Logout Successfully")
    return redirect('loginpage')

def home(request):
    if request.user.is_authenticated:
        user = request.user
    else:
        print("Please Sign in")
        
    if request.method == 'POST':
        if 'add_income' in request.POST:
            source = request.POST.get('source')
            amount = request.POST.get('amount')
            date = request.POST.get('date')
            type = "Income"

            
            if source and amount and date:
                 #date vaid..
                selected_date = datetime.strptime(date, "%Y-%m-%d").date()
                if selected_date > dt.today():
                    messages.error(request, "You cannot choose a future date.")
                    return redirect('homepage')
                
                data=Income(user=user,source=source,amount=amount,date=date)
                data.save()
                tran = Transaction(user=user,type=type ,source=source,amount=amount,date=date)
                tran.save()

            return redirect('homepage')

        elif 'add_expense' in request.POST:
            category_id = request.POST.get('category')
            amount = request.POST.get('amount')
            date = request.POST.get('date')
            type = "Expense"

            if category_id and amount and date:
                #vaild ..
                selected_date = datetime.strptime(date, "%Y-%m-%d").date()
                if selected_date > dt.today():
                    messages.error(request, "You cannot choose a future date.")
                    return redirect('homepage')
            
                category = Category.objects.get(id=category_id)
                data=Expense(user=user,category=category,amount=amount,date=date)
                data.save()
                tran = Transaction(user=user,type=type ,category=category,amount=amount,date=date)
                tran.save()
            return redirect('homepage')

        elif 'add_category' in request.POST:
            cname = request.POST.get('category_name')
            if cname:
                if Category.objects.filter(name=cname,user = request.user).exists():
                    messages.error(request,"Category Already Exist")
                    print("Category Already Exist")
                    return redirect("homepage")
                else:
                    data=Category(name=cname,user=user)
                    data.save()

                
            return redirect('homepage')
    #this is for show all category list in home page
    categorydata = Category.objects.filter(user=request.user)
    #this is next code for summary information show

    #calculate total income
    total_income = 0
    income_data=Income.objects.filter(user=request.user)
    for income in income_data:
        total_income = total_income + income.amount

    print(total_income)
    #caluclate total expense
    total_expense = 0
    expense_data = Expense.objects.filter(user=request.user)
    for expense in expense_data:
        total_expense = total_expense + expense.amount

    #calculate current balance
    current_balance = total_income - total_expense
    
    #resent transaction get 

    recent_transactions = Transaction.objects.filter(user=request.user).order_by('-time')[:8]
   
    
    context={
            'categorydata':categorydata,
            'total_income':total_income,
            'total_expense':total_expense,
            'current_balance':current_balance,
            'recent_transcation':recent_transactions,
        }
    
    return render(request,"home.html",context)


def category(request):
    if request.user.is_authenticated:
        username = request.user
        if request.method == "POST":
            n = request.POST.get('category_name')
            u = username
            data = Category(name = n, user = u)
            data.save()
            return redirect('home')
    else:
        print("Please Sign in")


def history(request):
    transactions = None
    if request.method =="POST":
        type = request.POST.get('type')
        
        if type == "all":
            transactions = Transaction.objects.filter(user= request.user)
        elif type== "income":
            transactions = Transaction.objects.filter(user=request.user, type="Income")
        else:
            transactions = Transaction.objects.filter(user=request.user, type="Expense")

    #data sort for pie chart
    Expense_transactions = Expense.objects.filter(user=request.user)
    cats = Category.objects.filter(user=request.user)
    category_labels = []
    category_total = []

    for c in cats:
        print(c)
        c_data = Expense.objects.filter(user=request.user,category = c)
        total=0
        for d in c_data: total =total+ d.amount
        
        category_labels.append(c.name)
        category_total.append(int(abs(total)))

    print(category_total)
    print(category_labels)

    # for bargraph
    current_year = datetime.now().year
    monthly_labels = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", 
                      "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]
    monthly_income = []
    monthly_expense = []
    for month in range(1, 13):
        #monthly income calculate
        income_tra = Income.objects.filter(date__year=current_year ,date__month=month, user = request.user)
        income_total = 0
        for i in income_tra : income_total = income_total + i.amount
        monthly_income.append(float(income_total))
        
        #monthly Expense calculate
        expense_tra = Expense.objects.filter(date__year=current_year ,date__month=month, user=request.user)
        expense_total = 0
        for e in expense_tra: expense_total = expense_total + e.amount
        monthly_expense.append(float(expense_total))

    print(f"Monthly Labels {monthly_labels}")
    print(f"Monthly income {monthly_income}")
    print(f"Monthly Expense {monthly_expense}")

    #calculate total income
    total_income = 0
    income_data=Income.objects.filter(user=request.user)
    for income in income_data:total_income = total_income + income.amount

    #caluclate total expense
    total_expense = 0
    expense_data = Expense.objects.filter(user=request.user)
    for expense in expense_data: total_expense = total_expense + expense.amount

    #calculate current balance
    current_balance = total_income - total_expense
    
  
    
    context={
            'total_income':total_income,
            'total_expense':total_expense,
            'current_balance':current_balance,
            'transcations':transactions,
            #for pie chart
            'category_labels':category_labels,
            'category_total': category_total,
            #for bar chart
            'monthly_labels': monthly_labels,
            'monthly_income': monthly_income,
            'monthly_expense': monthly_expense,

        }
    
    return render(request,"history.html",context)


def about(request):
    return render(request,"about.html")

def reminder(request):
    if request.method == "POST":
        message = request.POST.get('message')
        date = request.POST.get('date')
        time = request.POST.get('time')

        data = Reminder(user= request.user,message = message, date = date, time = time)
        data.save()

    reminders = Reminder.objects.filter(user=request.user)


    context ={
        'reminders':reminders,
    }
    return render(request,"reminder.html",context)

def delete_reminder(request, reminder_id):
    reminder = Reminder.objects.get(id=reminder_id, user=request.user)
    reminder.delete()
    return redirect("reminderpage")