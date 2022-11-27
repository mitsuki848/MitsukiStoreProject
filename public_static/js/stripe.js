// JavaScriptを使用して、client secretを取得する
const client_secret = document.getElementById('client_secret').value;

// JavaScriptを使用して、Stripeのインスタンスを作成する
const stripe = Stripe('pk_test_51M38WdDL7zxXIthJIyjKM3qLiCZerTGOM57VxWGiYuXaQZuigFA02wR8IhZwGxI5xMbH6xl3G2nooYapxRWpjGEz00Z5HeJHGQ');

// 支払いフォームで使用するElementsを設定し、上で取得したclient secretを渡す
const elements = stripe.elements({
    clientSecret:client_secret,
    appearance:{
        theme: 'stripe',
    },
});

// Payment Elementを作成し、既存のDOM要素から生成したDOM要素に置き換える
const paymentElement = elements.create('payment');
paymentElement.mount('#payment-element');

// id=payment-formの要素を取得する
const form = document.getElementById('payment-form');

// クレジットカード情報が送信された時の処理を記述する
form.addEventListener('submit', async (event) => {
  event.preventDefault();

  // confirmPaymentを呼び出して支払い処理を完了させる
  await stripe.confirmPayment({
    //`Elements` instance that was used to create the Payment Element
    elements,
    confirmParams: {
      return_url: '/thanks',
    },
  });
});
