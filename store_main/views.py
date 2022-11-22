from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.conf import settings

from store_main.models import Product, ImageZip
from main.views import index
from store_main.forms import ProductForm, CsvUploadForm, ImageZipForm

import csv
import io
import os
import glob
import shutil


def store_index(request):
    # スーパーユーザーでない場合。
    if not request.user.is_superuser:
        return redirect('main:index')

    context = {}
    return render(request, template_name="store_main/store_index.html",
                  context=context)


def product_new(request):
    # スーパーユーザーでない場合
    if not request.user.is_superuser:
        return redirect('main:index')

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
    # スーパーユーザーでない場合
    if not request.user.is_superuser:
        return redirect('main:index')

    products = Product.objects.all()
    context = {
        'products': products,
    }
    return render(request, template_name="store_main/product_list.html",
                  context=context)


# ストア側の商品編集ページ
def product_edit(request, product_id):
    # スーパーユーザーでない場合
    if not request.user.is_superuser:
        return redirect('main:index')

    product = get_object_or_404(Product, pk=product_id)
    # formを入力済みの状態で表示
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
        if "product_edit" in request.POST:
            # 商品編集ボタンが押された場合
            form = ProductForm(request.POST, instance=product, )
            # 検証
            if form.is_valid():
                form.save()
                messages.add_message(request, messages.SUCCESS,
                                     "編集を完了しました。")
                return redirect('store_main:product_edit',
                                product_id=product_id)
            else:
                messages.add_message(request, messages.ERROR,
                                     "編集に失敗しました。")

        if "product_delete" in request.POST:
            print('delete')
            # 商品削除ボタンが押された場合
            product_delete(request, product_id)
            # ???product_listにリダイレクトされない？

    # GET の場合
    context = {
        'product': product,
        'form': form,
    }
    return render(request, template_name="store_main/product_edit.html",
                  context=context)


# 商品削除
def product_delete(request, product_id):
    # スーパーユーザーでない場合
    if not request.user.is_superuser:
        return redirect('main:index')

    # 該当商品読み込み
    product = get_object_or_404(Product, pk=product_id)
    # 商品削除
    product.delete()

    return redirect('store_main:product_list')


# ストア側のcsv商品登録・編集機能
# https://blog.narito.ninja/detail/60/
def product_csv(request):
    # スーパーユーザーでない場合
    if not request.user.is_superuser:
        return redirect('main:index')

    # POSTの場合
    if request.method == 'POST':
        # product_csvが含まれている場合
        if 'product_csv' in request.POST:

            # フォームのhtmlとファイルを受け取る
            csv_form = CsvUploadForm(request.POST, request.FILES)

            if csv_form.is_valid():
                """ 商品csvアップ機能 """
                # csv.readerに渡すため、TextIOWrapperでテキストモードなファイルに変換
                csvfile = io.TextIOWrapper(csv_form.cleaned_data['file'],
                                           encoding='utf-8')
                reader = csv.reader(csvfile)
                # 1行ずつ取り出し、作成していく
                for i, row in enumerate(reader):
                    if i == 0:
                        continue
                    product, created = Product.objects.update_or_create(
                        code=row[0])
                    product.name = row[1]
                    product.description = row[2]
                    product.price = row[3]
                    product.amount = row[4]
                    product.image = f'product/{row[5]}'
                    product.save()
                messages.add_message(request, messages.SUCCESS,
                                     "追加・編集を完了しました。")
                return redirect('store_main:product_csv')
            else:
                messages.add_message(request, messages.ERROR,
                                     "追加・編集が失敗しました。")
                return redirect('store_main:product_csv')

        if 'product_img_zip' in request.POST:
            """ 画像zipアップ機能 """
            # フォームのhtmlとファイルを受け取る
            image_zip_form = ImageZipForm(request.POST, request.FILES)
            if image_zip_form.is_valid():
                image_zip = image_zip_form.save(commit=False)
                # zipを保存
                image_zip.save()
                # zipを展開
                shutil.unpack_archive(
                    glob.glob(os.path.join(settings.MEDIA_ROOT, 'image_zip',
                                           '*.zip'))[-1],
                    os.path.join(settings.MEDIA_ROOT, 'product'),
                )
                # ImageZipのレコードを全て削除
                ImageZip.objects.all().delete()
                # ディレクトリごとzipファイルを削除
                shutil.rmtree(os.path.join(settings.MEDIA_ROOT, 'image_zip'))

                messages.add_message(request, messages.SUCCESS,
                                     "画像アップロードを完了しました。")
                return redirect('store_main:product_csv')
            else:
                messages.add_message(request, messages.ERROR,
                                     "画像アップロードが失敗しました。")
                return redirect('store_main:product_csv')

    # GETの場合
    csv_upload_form = CsvUploadForm()
    image_zip_form = ImageZipForm()

    context = {
        'csv_upload_form': csv_upload_form,
        'image_zip_form': image_zip_form,
    }
    return render(request, template_name='store_main/product_csv.html',
                  context=context)
