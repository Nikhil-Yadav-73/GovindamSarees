import razorpay
client = razorpay.Client(auth=("YOUR_ID", "YOUR_SECRET"))

client.order.create({
  "amount": 50000,
  "currency": "INR",
  "receipt": "receipt#1",
  "partial_payment": false,
  "notes": {
    "key1": "value3",
    "key2": "value2"
  }
})