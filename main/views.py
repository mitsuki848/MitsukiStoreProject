from django.shortcuts import render, redirect, get_object_or_404
from users.models import User
from store_main.models import Product, Sale
from main.forms import AddToCartForm, PurchaseForm
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST
from django.contrib import messages
from django.conf import settings
# https://www.teamxeppet.com/pycharm-module-not-found-error/
import stripe
import json
import requests


# モデル出力確認
def test_index(request):
    # モデルの要素を取得
    users = User.objects.all().values()
    products = Product.objects.all().values()
    sales = Sale.objects.all().values()

    context = {
        'users': users,
        'products': products,
        'sales': sales,
    }
    return render(request, template_name='main/test_index.html',
                  context=context)


# トップページ、商品の一覧表示
def index(request):
    products = Product.objects.all()
    context = {
        'products': products,
    }
    return render(request, template_name='main/index.html', context=context)


# 商品詳細ページ
def product_detail(request, product_id):
    # 　product_idが存在しない場合404
    product = get_object_or_404(Product, pk=product_id)

    # カートに追加
    if request.method == 'POST':
        add_cart_form = AddToCartForm(request.POST)
        # 検証
        if add_cart_form.is_valid():
            # formのnum取り出し
            num = add_cart_form.cleaned_data['num']
            # sessionにcartが含まれているか確認
            if 'cart' in request.session:
                # 既に対象のproduct_idがcartにあれば加算、なければ新しくキーを追加する
                if str(product_id) in request.session['cart']:
                    request.session['cart'][str(product_id)] += num
                else:
                    request.session['cart'][str(product_id)] = num

            # sessionにcartが含まれていない場合
            else:
                # 新しく'cart'というキーをセッションに追加する
                request.session['cart'] = {str(product_id): num}
            # メッセージの出力
            messages.success(request, f'{product.name}を{num}個カートに入れました!')
            return redirect('main:product_detail', product_id=product_id)

    # GET
    add_cart_form = AddToCartForm()
    context = {
        'product': product,
        'add_cart_form': add_cart_form,
    }
    return render(request, template_name='main/product_detail.html',
                  context=context)


# 住所検索の関数
def fetch_address(zip_code):
    """郵便番号検索APIを利用する関数
    引数に指定された郵便番号に対応する住所を返す
    住所取得に失敗した場合じゃ空文字を返す"""

    REQUEST_URL = f'http://zipcloud.ibsnet.co.jp/api/search?zipcode={zip_code}'
    response = requests.get(REQUEST_URL)
    response = json.loads(response.text)
    results, api_status = response['results'], response['status']

    address = ''
    # レスポンスステータスが200　かつ　'results'が存在する場合
    # address変数に取得した住所を代入する
    if api_status == 200 and results is not None:
        result = results[0]
        address = result['address1'] + result['address2'] + result['address3']
    return address


# カートページ
@login_required
def user_cart(request):
    # GET POST 両方の変数＝＝＝＝＝＝＝＝＝＝＝＝

    # session自体が辞書型になっているので.getで'cart'キーでcartの辞書を取得、
    # cartがない場合は空の辞書とする。
    cart = request.session.get('cart', {})

    # 空の辞書とtotal_priceの変数を用意
    cart_products = {}
    total_price = 0

    # 合計金額の計算
    # .items()でkeyとvalueを取り出す
    for product_id, num in cart.items():
        product = Product.objects.filter(id=product_id).first()

        # .first()で削除されている商品の場合はNoneを返す
        if product is None:
            continue

        # cart_productsにproductをkeyとしてnumを追加
        cart_products[product] = num
        total_price += product.price * num

    # ＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝

    if request.method == 'POST':

        # user情報
        user = request.user

        purchase_form = PurchaseForm(request.POST)

        if purchase_form.is_valid():

            # 住所検索ボタンが押下された場合
            if 'search_address' in request.POST:
                zip_code = request.POST['zip_code']
                address = fetch_address(zip_code)

                # 住所が取得できなかった場合はメッセージを出してリダイレクト
                if not address:
                    messages.warning(request, "住所を取得できませんでした")
                    return redirect('main:user_cart')

                # 住所が取得出来たらフォームの値として入力する
                purchase_form = PurchaseForm(
                    initial={'zip_code': zip_code, 'address': address}
                )
                context = {
                    'purchase_form': purchase_form,
                    'cart_products': cart_products,
                    'total_price': total_price,
                }
                return render(request, template_name='main/user_cart.html',
                              context=context)

        # 購入ボタンを押された場合
        if 'buy_product' in request.POST:

            # 住所が入力済みか確認する。未入力の場合はリダイレクトする。
            if not purchase_form.cleaned_data['address']:
                messages.warning(request, "住所の入力は必須です")
                return redirect('main:user_cart')

            # カートが空じゃないか確認する
            if not cart:
                messages.warning(request, "カートは空です")
                return redirect('main:user_cart')

            # 所持ポイントが十分にあるかを確認する。
            if total_price > user.point:
                messages.warning(request, "所持ポイントが足りません")
                return redirect('main:user_cart')

            # 在庫があるか確認する。
            for product, num in cart_products.items():
                if product.amount < num:
                    messages.warning(request, f"{product.name}の在庫が足りません")
                    return redirect('main:user_cart')

            # 各プロダクトのSale情報を保持（売上記録の登録）
            for product, num in cart_products.items():
                sale = Sale(
                    # modelでForeignKeyとしている為、productはProductのインスタンスでなければならない。
                    product=product,
                    user=user,
                    amount=num,
                    price=product.price,
                    zip_code=purchase_form.cleaned_data['zip_code'],
                    address=purchase_form.cleaned_data['address'],
                    # total_priceとしているが、商品ごとの小計
                    total_price=product.price * num,
                )

                # 在庫数変更
                product.amount -= num

                # データベースに保存
                sale.save()
                product.save()

                # 購入した分だけユーザーの保有ポイントを減らす。
                user.point -= total_price
                user.save()

            # セッションから'cart'を削除してカートを空にする
            del request.session['cart']

            messages.success(request, "商品の購入が完了しました！")
            return redirect('main:user_cart')

    # GETの場合
    purchase_form = PurchaseForm()

    context = {
        'purchase_form': purchase_form,
        'cart_products': cart_products,
        'total_price': total_price,
    }
    return render(request, template_name='main/user_cart.html', context=context)


# 数量変更
@login_required
@require_POST
def change_product_amount(request):
    # name="product_id"のフィールドの値を取得（どの商品を増減させるか）
    product_id = request.POST["product_id"]
    # セッションから"cart"情報を取得
    cart_session = request.session['cart']

    # センションの更新
    if product_id in cart_session:
        # １つ減らすボタンが押された時
        if "action_remove" in request.POST:
            cart_session[product_id] -= 1
        # １つ増やすボタンが押された時
        if "action_add" in request.POST:
            cart_session[product_id] += 1
        # 商品個数が0以下になった場合は、カートから対象商品の削除
        if cart_session[product_id] <= 0:
            del cart_session[product_id]
    return redirect('main:user_cart')


# 注文履歴
@login_required
def order_history(request):
    user = request.user
    sales = Sale.objects.filter(user=user).order_by('-created_at')
    context = {'sales': sales}
    return render(request, template_name='main/order_history.html',
                  context=context)


# 決済　支払いフォームを返す処理
def payment(request):
    # StripeのAPIキーを登録する
    stripe.api_key = settings.STRIPE_API_KEY

    # 今回は支払い額を10,000円とする
    amount = 10000

    # PaymentIntentを作成する
    intent = stripe.PaymentIntent.create(
        amount=amount,
        currency='jpy',
        description='テスト支払い',
        payment_method_types=["card"],
    )

    # 作成したPaymentIntentからclient_secretを取得する
    client_secret = intent["client_secret"]

    # テンプレートと渡すデータを指定する
    template_name = "payment.html"
    context = {
        "amount": amount,
        "client_secret": client_secret,
    }

    return render(request, template_name, context)


# 単純に支払い完了ページを表示する処理
def thanks(request):
    template_name = "thanks.html"
    return render(request, template_name)
