# OOP Lesson 2: Same Interface, Different Behaviour 🎭

**← Back to [Lesson 1: Inheritance](01-inheritance.md)**

---

## The Magic You Already Saw

Remember the animal shelter? You wrote this:

```python
for animal in shelter.animals:
    print(animal.make_sound())
```

And Python just... knew what to do. Dogs barked. Cats meowed. You didn't write `if dog: bark elif cat: meow`. You just called `make_sound()` and trusted each animal to handle itself.

That's **polymorphism**. The word is intimidating. The idea isn't.

**Polymorphism = "many shapes."** Different objects respond to the same method name in their own way.

---

## A Real Example, Step By Step

Let's say you're building a payment system. You support credit cards and PayPal. They work completely differently — but from your app's perspective, they should look the same.

Without polymorphism, you'd write this mess every time:

```python
def process_payment(payment_type, amount, details):
    if payment_type == "credit_card":
        # Validate card, charge it, log it...
        pass
    elif payment_type == "paypal":
        # Verify account, send money, log it...
        pass
    elif payment_type == "bank_transfer":
        # Another 20 lines...
        pass
    # Every new payment type = another elif = more mess
```

With polymorphism:

```python
class CreditCardPayment:
    def __init__(self, card_number):
        self.card_number = card_number

    def pay(self, amount):
        last_four = self.card_number[-4:]
        return f"Charged £{amount} to card ending {last_four} 💳"


class PayPalPayment:
    def __init__(self, email):
        self.email = email

    def pay(self, amount):
        return f"Sent £{amount} via PayPal to {self.email} 📧"


# The function that uses them doesn't care HOW they work:
def checkout(payment_method, amount):
    return payment_method.pay(amount)


# Use any payment type — checkout doesn't change:
card = CreditCardPayment("4111111111111111")
paypal = PayPalPayment("szonja@example.com")

print(checkout(card, 25.00))
# Charged £25.00 to card ending 1111 💳

print(checkout(paypal, 50.00))
# Sent £50.00 via PayPal to szonja@example.com 📧
```

The `checkout` function doesn't know or care what kind of payment it's processing. It just calls `.pay()` and trusts the object to handle itself.

---

## Python Doesn't Check Types (and That's the Point)

In some languages, you have to declare "this function accepts a PaymentMethod type." Python doesn't care. If an object has a `.pay()` method, you can pass it to `checkout`. No type declarations needed.

This is called **duck typing**: "If it walks like a duck and quacks like a duck, it's a duck."

```python
class CryptoPayment:  # Brand new — no shared parent class!
    def __init__(self, wallet_address):
        self.wallet = wallet_address

    def pay(self, amount):
        return f"Sent {amount} BTC to {self.wallet[:8]}... 🪙"

# Works immediately with checkout — no changes needed
crypto = CryptoPayment("1A1zP1eP5QGefi2DMPTfTL5SLmv7DivfNa")
print(checkout(crypto, 0.01))
# Sent 0.01 BTC to 1A1zP1eP... 🪙
```

No inheritance from `PaymentMethod`. No interface declaration. Just a `.pay()` method. That's all Python needs.

---

## When to Use a Shared Parent Class

Duck typing is great for flexibility. But sometimes you WANT a shared parent class — to guarantee certain methods exist:

```python
class PaymentMethod:  # Parent — defines the contract
    def pay(self, amount):
        raise NotImplementedError(
            "Every payment method MUST implement pay()"
        )


class CreditCardPayment(PaymentMethod):
    def __init__(self, card_number):
        self.card_number = card_number

    def pay(self, amount):
        last_four = self.card_number[-4:]
        return f"Charged £{amount} to card ending {last_four} 💳"


class BrokenPayment(PaymentMethod):
    # Forgot to write pay()!
    pass


# card = CreditCardPayment("4111111111111111")
# print(card.pay(10))  # ✅ Works

# broken = BrokenPayment()
# broken.pay(10)  # ❌ NotImplementedError — caught the mistake!
```

The parent class acts as documentation: "Here's what every payment method MUST do." If someone forgets, they get a clear error instead of a mysterious crash later.

---

## Practice: A Simple Notification System

**Your task:** Build a notification dispatcher that can send messages through different channels.

1. Create a `Notifier` parent class with:
   - A `send(message, recipient)` method that raises `NotImplementedError`

2. Create child classes:
   - `EmailNotifier` — `send()` returns `"📧 Emailed '{message}' to {recipient}"`
   - `SMSNotifier` — `send()` returns `"📱 Texted '{message}' to {recipient}"`
   - `SlackNotifier` — `send()` returns `"💬 Posted '{message}' to #{recipient}"`

3. Create an `AlertSystem` class that:
   - Takes a list of notifiers
   - `broadcast(message, recipient)` — sends the message through ALL notifiers and returns the results

**Test it:**

```python
alert = AlertSystem([
    EmailNotifier(),
    SMSNotifier(),
    SlackNotifier(),
])

results = alert.broadcast("Server is down!", "admin")
for result in results:
    print(result)

# 📧 Emailed 'Server is down!' to admin
# 📱 Texted 'Server is down!' to admin
# 💬 Posted 'Server is down!' to #admin
```

Create `notifications.py` and try it!

---

## Solution

```python
class Notifier:
    def send(self, message, recipient):
        raise NotImplementedError(
            "Subclasses must implement send()"
        )


class EmailNotifier(Notifier):
    def send(self, message, recipient):
        return f"📧 Emailed '{message}' to {recipient}"


class SMSNotifier(Notifier):
    def send(self, message, recipient):
        return f"📱 Texted '{message}' to {recipient}"


class SlackNotifier(Notifier):
    def send(self, message, recipient):
        return f"💬 Posted '{message}' to #{recipient}"


class AlertSystem:
    def __init__(self, notifiers):
        self.notifiers = notifiers

    def broadcast(self, message, recipient):
        results = []
        for notifier in self.notifiers:
            results.append(notifier.send(message, recipient))
        return results


# Test
alert = AlertSystem([
    EmailNotifier(),
    SMSNotifier(),
    SlackNotifier(),
])

results = alert.broadcast("Server is down!", "admin")
for result in results:
    print(result)
```

---

## What You Just Learned

- **Polymorphism = same method name, different behaviour** — no if/elif chains needed
- **Duck typing** — Python doesn't care about types, only about methods
- **Parent classes as contracts** — they document what methods must exist
- **Adding new types is easy** — write the class, give it the right methods, and it just works with existing code

---

## What's Next?

You've built classes that behave differently. Now let's make them feel like real Python objects — supporting `+`, `print()`, `len()`, and all the built-in operations you know and love.

Continue to **[OOP Lesson 3: Making Your Objects Pythonic](../oop/03-magic-methods.md)** ✨

---

**Your turn:** Build the notification system! Then add a `PushNotification` class and add it to the alert system — notice you didn't have to change ANY existing code. 🎭💛
