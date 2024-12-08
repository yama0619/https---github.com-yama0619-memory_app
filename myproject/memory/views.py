from django.shortcuts import render, redirect
from .models import Memory
from django.http import HttpResponse
from datetime import datetime,timedelta,date
from django.utils import timezone
from calendar import monthrange
from django import forms
from django.contrib import messages



#メインページ(カレンダー画面)の描画
def memory_list(request):
    current_date = datetime.now()
    
    year = int(request.GET.get('year', current_date.year))
    month = int(request.GET.get('month', current_date.month))
    
    # ナビゲーション用の先月と来月を計算
    prev_month = month - 1 if month > 1 else 12
    prev_year = year if month > 1 else year - 1
    next_month = month + 1 if month < 12 else 1
    next_year = year if month < 12 else year + 1
    
    # 月初と月末を計算
    first_day_of_month = datetime(year, month, 1)
    last_day_of_month = datetime(year, month, monthrange(year, month)[1])
    
    # カレンダーに表示する日付を準備
    days_in_month = []
    first_day_weekday = first_day_of_month.weekday()  # 月初の曜日 (0:月曜, 6:日曜)

    #1か月分を取得
    memories = Memory.objects.filter(created_at__year=year, created_at__month=month).values_list('created_at__day', flat=True)
    for day in days_in_month:
        if isinstance(day, dict) and day['day']:
            day['has_memory'] = day['day'] in memories
    
    # 前月の空白
    for _ in range(first_day_weekday + 1):
        days_in_month.append({'day': '', 'is_today': False,'is_future': False ,'has_memory': False})

    # 現在の月の日付
    for day in range(1, last_day_of_month.day + 1):
        is_today = (year == current_date.year and month == current_date.month and day == current_date.day)
        is_future = datetime(year, month, day).date() > timezone.now().date()
        has_memory = day in memories
        days_in_month.append({'day': day, 'is_today': is_today,'is_future':is_future, 'has_memory': has_memory})
    
    # 翌月の空白（最後の週を埋める）
    while len(days_in_month) % 7 != 0:
        days_in_month.append({'day': '', 'is_today': False,'is_future': False,'has_memory': False})

    
    # 週ごとに分割
    weeks = [days_in_month[i:i + 7] for i in range(0, len(days_in_month), 7)]

    # 曜日
    weekdays = ["日","月", "火", "水", "木", "金", "土" ]

    context = {
        'current_date': current_date,
        'weeks': weeks,
        'year': year,
        'month': month,
        'prev_year': prev_year,
        'prev_month': prev_month,
        'next_year': next_year,
        'next_month': next_month,
        'weekdays': weekdays,
    }

    return render(request, 'memory/memory_list.html', context)


from .forms import MemoryForm
#追加ページ(入力画面)の描画
def memory_add(request):
    if request.method == 'POST':
        form = MemoryForm(request.POST, request.FILES)  # ファイルを含むフォームデータ
        if form.is_valid():  #有効なら
            form.save()  #DBに保存
            return redirect('memory_list')  #思い出一覧へ
    else:
        form = MemoryForm()  # GETリクエストなら空のフォームを表示

    return render(request, 'memory/memory_add.html', {'form': form})


def memory_check(request, year, month, day):
    if not day:
        return HttpResponse("Invalid date", status=400)
    
    # URLから取得した日付を確認
    print(f"Clicked date: {year}-{month}-{day}")

    # 指定された日付に関連する思い出を取得
    memories = Memory.objects.filter(created_at__year=year, created_at__month=month, created_at__day=day)
    
    
    # コンテキストを作成
    context = {
        'memories': memories,
        'year': year,
        'month': month,
        'day': day,
    }
    
    return render(request, 'memory/memory_check.html', context)