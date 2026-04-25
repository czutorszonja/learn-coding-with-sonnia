# Python Lesson 11: Working with APIs — Talking to Other Programs 🌐

**← Back to [Lesson 10: Error Handling](10-error-handling.md)**

---

## What is an API?

**Plain English:** An API (Application Programming Interface) is a way for programs to talk to each other.

**Real-world analogy:** Think of a restaurant:
- You (the customer) = Your Python program
- Waiter = The API
- Kitchen = The server/database

You don't go into the kitchen yourself. You tell the waiter what you want, and they bring it to you!

---

## Why Use APIs?

**Without APIs:**
```python
# You'd need to build EVERYTHING yourself!
# Want weather data? Build your own weather satellites!
# Want maps? Draw them yourself!
```

**With APIs:**
```python
# Use someone else's service!
import requests
response = requests.get("https://api.weather.com/forecast")
weather = response.json()
print(f"It's {weather['temp']}°C outside")
```

---

## The `requests` Library

Python needs a library to make API calls:

```bash
pip install requests
```

Then import it:
```python
import requests
```

---

## Making a GET Request

**GET** means "get data" from the API:

```python
import requests

# Make a GET request
response = requests.get("https://api.example.com/data")

# Check if it worked
print(response.status_code)  # 200 means success!

# Get the data
data = response.json()
print(data)
```

**Key parts:**
- `requests.get()` — makes the request
- `response.status_code` — tells you if it worked (200 = OK, 404 = Not Found, 500 = Server Error)
- `response.json()` — converts the response to Python data

---

## Checking the Response

**Always check if the request worked!**

```python
import requests

response = requests.get("https://api.example.com/data")

if response.status_code == 200:
    data = response.json()
    print("Success!")
    print(data)
else:
    print(f"Error: {response.status_code}")
```

**Common status codes:**
- `200` — OK (success!)
- `201` — Created (something was created)
- `400` — Bad Request (you sent invalid data)
- `401` — Unauthorized (you need to log in)
- `404` — Not Found (the resource doesn't exist)
- `500` — Server Error (their problem, not yours)

---

## Sending Data with POST

**POST** means "send data" to the API:

```python
import requests

# Data to send
new_user = {
    "name": "Szonja",
    "email": "szonja@example.com",
    "age": 30
}

# Send POST request
response = requests.post(
    "https://api.example.com/users",
    json=new_user
)

# Check response
if response.status_code == 201:
    print("User created!")
    print(response.json())
else:
    print(f"Error: {response.status_code}")
```

**Key parts:**
- `requests.post()` — makes a POST request
- `json=new_user` — sends data as JSON
- Response might include the created item with an ID

---

## Working with JSON Data

APIs usually send and receive **JSON** (JavaScript Object Notation):

**JSON looks like Python dictionaries:**
```json
{
    "name": "Szonja",
    "age": 30,
    "city": "London"
}
```

**In Python:**
```python
# Convert JSON response to Python dict
data = response.json()
print(data["name"])  # Output: Szonja
print(data["age"])   # Output: 30
```

---

## Practice Exercise

**Scenario:** You're building a random joke generator that saves favorites to a file!

**Your task:**
1. Import the `requests` library
2. Create a function called `fetch_random_joke` that:
   - Makes a GET request to `https://official-joke-api.appspot.com/random_joke`
   - Checks if the status code is 200
   - Returns the joke as a dictionary (with `setup` and `punchline` keys)
   - Handles errors gracefully (return None if something fails)
3. Create a function called `save_joke_to_file` that takes a joke dictionary and:
   - Opens a file called `jokes.txt` in append mode
   - Writes the setup and punchline in a nice format
   - Adds a newline at the end
4. Create a function called `display_joke` that prints a joke nicely
5. Test by fetching 3 jokes and saving them
6. Read the file and display all saved jokes

**Example output:**
```
Fetching joke 1...
Joke: What do you call a fish with no eyes?
Punchline: Fsh!
Saved to jokes.txt!

=== Your Favorite Jokes ===
Q: What do you call a fish with no eyes?
A: Fsh!
...
```

**Try it yourself first!** Solution below.

---

## Solution

```python
import requests

def fetch_random_joke():
    """Fetch a random joke from the API."""
    url = "https://official-joke-api.appspot.com/random_joke"
    
    try:
        response = requests.get(url, timeout=10)
        
        if response.status_code == 200:
            joke_data = response.json()
            return {
                "setup": joke_data["setup"],
                "punchline": joke_data["punchline"]
            }
        else:
            print(f"Error: Status code {response.status_code}")
            return None
    except Exception as e:
        print(f"Error fetching joke: {e}")
        return None

def save_joke_to_file(joke):
    """Save a joke to jokes.txt."""
    if joke is None:
        return
    
    with open("jokes.txt", "a") as file:
        file.write(f"Q: {joke['setup']}\n")
        file.write(f"A: {joke['punchline']}\n")
        file.write("-" * 40 + "\n")
    print("Saved to jokes.txt!")

def display_joke(joke):
    """Display a joke nicely."""
    if joke:
        print(f"Joke: {joke['setup']}")
        print(f"Punchline: {joke['punchline']}")

# Fetch and save 3 jokes
print("Fetching jokes...\n")
for i in range(3):
    print(f"Fetching joke {i + 1}...")
    joke = fetch_random_joke()
    display_joke(joke)
    save_joke_to_file(joke)
    print()

# Display all saved jokes
print("=== Your Favorite Jokes ===")
try:
    with open("jokes.txt", "r") as file:
        content = file.read()
        print(content)
except FileNotFoundError:
    print("No jokes saved (API may be unavailable)")
```

**Note:** The API returns a different joke each time you run it!

---

## Quick Recap

- **API** — lets programs talk to each other
- **`requests` library** — makes HTTP requests
- **GET** — fetch data from API
- **POST** — send data to API
- **`response.status_code`** — check if request worked (200 = success)
- **`response.json()`** — convert JSON to Python dictionary
- **Always check status codes!** Handle errors gracefully

---

## What's Next?

Ready for more? Continue to **[Lesson 12: Testing Your Code](12-testing-your-code.md)**! 🚀

---

**Your turn:** Try the joke exercise! Then explore other free APIs like:
- `https://dog.ceo/api/breeds/image/random` — Random dog pictures
- `https://api.coindesk.com/v1/bpi/currentprice.json` — Bitcoin prices
- `https://api.chucknorris.io/jokes/random` — Chuck Norris jokes

🌐💛
