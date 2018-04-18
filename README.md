# PyDonalds

An attempt to reverse engineer the McDonalds private API, as used by the McDonalds mobile app.

# Usage

```python
>>> spoofer = Spoofer(api_key, market_id="UK")
>>> spoofer.sign_in(email, username)
>>> order = spoofer.new_order(restaurant_id)
>>> item = ItemFactory.large_coke()
>>> order.add_item(item)
>>> spoofer.get_total(order)
1.53
>>> spoofer.payment(order)
>>> spoofer.payment(order, customer_payment_method_id)
>>> spoofer.pickup(order, customer_pament_method_id)  # Returns order number
53
```

Available order items are listed in `/docs/meals/overview.txt`.

