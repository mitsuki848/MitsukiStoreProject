from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages

from store_main.models import Product
from main.views import index
from store_main.forms import ProductForm, CsvUploadForm

import csv
import io


def store_index(request):
    context = {}
    return render(request, template_name="store_main/store_index.html",
                  context=context)


@login_required
def product_new(request):
    if request.method == 'POST':
        # フォームのhtmlとファイルを受け取る
        form = ProductForm(request.POST, request.FILES)
        if form.is_valid():
            product = form.save(commit=False)
            product.save()
            messages.add_message(request, messages.SUCCESS,
                                 "商品を登録しました。")
            redirect('store_main:product_list')
        else:
            messages.add_message(request, messages.ERROR,
                                 "商品登録に失敗しました。")
    # GETの場合
    form = ProductForm()

    context = {
        'form': form,
    }
    print(ProductForm())
    return render(request, template_name="store_main/product_new.html",
                  context=context)


# ストア側の商品一覧ページ
def product_list(request):
    products = Product.objects.all()
    context = {
        'products': products,
    }
    return render(request, template_name="store_main/product_list.html",
                  context=context)


# ストア側の商品編集ページ
def product_edit(request, product_id):
    # formを入力済みの状態で表示
    product = get_object_or_404(Product, pk=product_id)

    form = ProductForm(
        initial={
            'name': product.name,
            'description': product.description,
            'price': product.price,
            'amount': product.amount,
            'image': product.image,
            'code': product.code,
        }
    )
    if request.method == 'POST':
        # 商品編集ボタンが押された場合
        form = ProductForm(request.POST, instance=product,)
        # 検証
        if form.is_valid():
            form.save()
            messages.add_message(request, messages.SUCCESS,
                                 "編集を完了しました。")
            return redirect('store_main:product_edit', product_id=product_id)
        else:
            messages.add_message(request, messages.ERROR,
                                 "編集に失敗しました。")

    # GET の場合
    context = {
        'product': product,
        'form': form,
    }
    return render(request, template_name="store_main/product_edit.html",
                  context=context)


# ストア側のcsv商品登録・編集機能
# https://blog.narito.ninja/detail/60/
def product_csv(request):
    # POSTの場合
    if request.method == 'POST':
        # フォームのhtmlとファイルを受け取る
        csv_form = CsvUploadForm(request.POST, request.FILES)

        if csv_form.is_valid():
            # csv.readerに渡すため、TextIOWrapperでテキストモードなファイルに変換
            csvfile = io.TextIOWrapper(csv_form.cleaned_data['file'],
                                       encoding='utf-8')
            reader = csv.reader(csvfile)
            # 1行ずつ取り出し、作成していく
            for i, row in enumerate(reader):
                if i == 0:
                    continue
                product, created = Product.objects.update_or_create(code=row[0])
                product.name = row[1]
                product.description = row[2]
                product.price = row[3]
                product.amount = row[4]
                product.image = row[5]
                product.save()
            messages.add_message(request, messages.SUCCESS,
                                 "追加・編集を完了しました。")
            return redirect('store_main:product_csv')
        else:
            messages.add_message(request, messages.ERROR,
                                 "追加・編集が失敗しました。")
            return redirect('store_main:product_csv')
        # 途中

    # GETの場合
    csv_form = CsvUploadForm()
    context = {
        'CsvUploadForm': CsvUploadForm
    }
    return render(request, template_name='store_main/product_csv.html',
                  context=context)
