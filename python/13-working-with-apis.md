# Python Lesson 13: Working with APIs 🌐

**← Back to [Lesson 12: Error Handling and Debugging](12-error-handling.md)**

---

## What is an API?

**Plain English:** An API (Application Programming Interface) is a way for programs to talk to each other.

**Real-world analogy:** Think of a restaurant:
- **You (client)** = Your Python program
- **Waiter (API)** = Takes your request to the kitchen
- **Kitchen (server)** = Prepares your food (data)
- **Food (response)** = Data sent back to you

You don't need to know how the kitchen works — you just order from the menu!

---

## Why Use APIs?

APIs let you:
- Get real-time data (weather, stocks, news)
- Send data (post to social media, send emails)
- Use services (payment processing, maps, translation)

**Examples:**
- Weather app fetching forecast data
- Twitter bot posting tweets
- Payment system processing transactions

---

## HTTP Methods

| Method | Purpose | Example |
|--------|---------|---------|
| `GET` | Retrieve data | Get list of users |
| `POST` | Create new data | Create a new user |
| `PUT` | Update existing data | Update user info |
| `DELETE` | Remove data | Delete a user |

---

## Installing the `requests` Library

```bash
pip install requests
```

**Check installation:**
```python
import requests
print(requests.__version__)
```

---

## Making Your First API Call

### GET Request

```python
import requests

# Make a GET request
response = requests.get("https://api.example.com/users")

# Check if successful
print(response.status_code)  # 200 means success!

# Get the data
data = response.json()
print(data)
```

---

## Understanding Responses

```python
import requests

response = requests.get("https://api.github.com/users/github")

# Status code
print(f"Status: {response.status_code}")  # 200

# Response headers
print(f"Content-Type: {response.headers['Content-Type']}")

# Response data
data = response.json()
print(f"User: {data['login']}")
print(f"Followers: {data['followers']}")
```

### Common Status Codes

| Code | Meaning | What it means |
|------|---------|---------------|
| 200 | OK | Success! |
| 201 | Created | Resource created successfully |
| 400 | Bad Request | Your request was invalid |
| 401 | Unauthorized | You need to log in |
| 403 | Forbidden | You don't have permission |
| 404 | Not Found | Resource doesn't exist |
| 500 | Server Error | Problem on their end |

---

## Working with JSON Data

APIs usually return data in JSON format:

```python
import requests

response = requests.get("https://api.example.com/users/1")
user = response.json()

# Access data like a dictionary
print(f"Name: {user['name']}")
print(f"Email: {user['email']}")
print(f"ID: {user['id']}")

# Loop through data
for key, value in user.items():
    print(f"{key}: {value}")
```

---

## Sending Data with POST

```python
import requests

# Data to send
new_user = {
    "name": "Alice Smith",
    "email": "alice@example.com",
    "age": 30
}

# Make POST request
response = requests.post(
    "https://api.example.com/users",
    json=new_user
)

# Check result
print(f"Status: {response.status_code}")
print(f"Response: {response.json()}")
```

---

## API Authentication

Many APIs require an API key:

```python
import requests

# API key (NEVER share this!)
api_key = "your_api_key_here"

# Include in request
headers = {
    "Authorization": f"Bearer {api_key}"
}

response = requests.get(
    "https://api.example.com/protected-data",
    headers=headers
)

print(response.json())
```

**Security tip:** Store API keys in environment variables, not in your code!

---

## Handling API Errors

```python
import requests

try:
    response = requests.get("https://api.example.com/data")
    
    # Check if request was successful
    response.raise_for_status()  # Raises exception for 4xx/5xx errors
    
    data = response.json()
    print(data)
    
except requests.exceptions.HTTPError as e:
    print(f"HTTP error occurred: {e}")
except requests.exceptions.ConnectionError:
    print("Could not connect to the server!")
except requests.exceptions.Timeout:
    print("Request timed out!")
except requests.exceptions.RequestException as e:
    print(f"An error occurred: {e}")
```

---

## Adding Timeouts

Always set a timeout to prevent hanging:

```python
import requests

try:
    response = requests.get(
        "https://api.example.com/data",
        timeout=5  # 5 seconds
    )
    print(response.json())
except requests.exceptions.Timeout:
    print("Request took too long!")
```

---

## Real-World Examples

### Example 1: Get Weather Data

```python
import requests

def get_weather(city):
    api_key = "your_openweathermap_api_key"
    url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}"
    
    response = requests.get(url)
    
    if response.status_code == 200:
        data = response.json()
        temp = data['main']['temp'] - 273.15  # Convert from Kelvin
        print(f"Temperature in {city}: {temp:.1f}°C")
    else:
        print(f"Error: {response.status_code}")

# Usage
get_weather("London")
```

---

### Example 2: Fetch Random User Data

```python
import requests

def get_random_user():
    url = "https://randomuser.me/api/"
    response = requests.get(url)
    
    if response.status_code == 200:
        data = response.json()
        user = data['results'][0]
        
        print(f"Name: {user['name']['first']} {user['name']['last']}")
        print(f"Email: {user['email']}")
        print(f"City: {user['location']['city']}")
    else:
        print("Failed to fetch user")

# Usage
get_random_user()
```

---

### Example 3: Search GitHub Repositories

```python
import requests

def search_github_repos(query):
    url = "https://api.github.com/search/repositories"
    params = {"q": query, "sort": "stars", "order": "desc"}
    
    response = requests.get(url, params=params)
    
    if response.status_code == 200:
        data = response.json()
        repos = data['items'][:5]  # Top 5 results
        
        for repo in repos:
            print(f"⭐ {repo['name']} by {repo['owner']['login']}")
            print(f"   Stars: {repo['stargazers_count']}")
            print(f"   URL: {repo['html_url']}")
            print()
    else:
        print(f"Error: {response.status_code}")

# Usage
search_github_repos("python machine learning")
```

---

## Practice Exercises

### Exercise 1: Fetch and Display Data

**Scenario:** You want to fetch data from a public API!

**Your task:**
1. Import the `requests` library
2. Make a GET request to `https://jsonplaceholder.typicode.com/posts/1`
3. Print the status code
4. Print the title of the post
5. Print the body of the post

**Try it yourself first!** Scroll down when ready.

---

### Exercise 2: Get Multiple Items

**Scenario:** You need to fetch a list of items!

**Your task:**
1. Make a GET request to `https://jsonplaceholder.typicode.com/users`
2. Loop through the users
3. Print each user's name and email
4. Count and print the total number of users

**Try it yourself first!** Scroll down when ready.

---

### Exercise 3: Create a New Resource

**Scenario:** You need to add a new post to a blog!

**Your task:**
1. Create a dictionary with `title`, `body`, and `userId`
2. Make a POST request to `https://jsonplaceholder.typicode.com/posts`
3. Print the status code
4. Print the created post (including the new ID)

**Try it yourself first!** Scroll down when ready.

---

### Exercise 4: Handle API Errors

**Scenario:** You're fetching data that might not exist!

**Your task:**
1. Try to fetch a post with ID 9999 from `https://jsonplaceholder.typicode.com/posts/9999`
2. Check the status code
3. If status is 404, print "Post not found!"
4. If status is 200, print the post title
5. Handle any other errors gracefully

**Try it yourself first!** Scroll down when ready.

---

## Solutions

### Solution 1: Fetch and Display Data

```python
import requests

# Make GET request
response = requests.get("https://jsonplaceholder.typicode.com/posts/1")

# Print status code
print(f"Status: {response.status_code}")

# Parse JSON
post = response.json()

# Print title and body
print(f"Title: {post['title']}")
print(f"Body: {post['body']}")
```

**Output:**
```
Status: 200
Title: sunt aut facere repellat provident occaecati excepturi optio reprehenderit
Body: quia et suscipit...
```

---

### Solution 2: Get Multiple Items

```python
import requests

# Fetch users
response = requests.get("https://jsonplaceholder.typicode.com/users")
users = response.json()

# Print each user
for user in users:
    print(f"{user['name']} - {user['email']}")

# Print total count
print(f"\nTotal users: {len(users)}")
```

**Output:**
```
Leanne Graham - Sincere@april.biz
Ervin Howell - Shanna@melissa.tv
...
Total users: 10
```

---

### Solution 3: Create a New Resource

```python
import requests

# Data to send
new_post = {
    "title": "My First Post",
    "body": "This is the content of my post.",
    "userId": 1
}

# Make POST request
response = requests.post(
    "https://jsonplaceholder.typicode.com/posts",
    json=new_post
)

# Print result
print(f"Status: {response.status_code}")
print(f"Created post: {response.json()}")
```

**Output:**
```
Status: 201
Created post: {'title': 'My First Post', 'body': 'This is the content of my post.', 'userId': 1, 'id': 101}
```

---

### Solution 4: Handle API Errors

```python
import requests

try:
    response = requests.get("https://jsonplaceholder.typicode.com/posts/9999")
    
    if response.status_code == 404:
        print("Post not found!")
    elif response.status_code == 200:
        post = response.json()
        print(f"Title: {post['title']}")
    else:
        print(f"Unexpected status: {response.status_code}")
        
except requests.exceptions.RequestException as e:
    print(f"Error: {e}")
```

**Output:**
```
Post not found!
```

---

## Quick Recap

- **API** = Way for programs to communicate
- **`requests` library** = Make HTTP requests
- **`GET`** = Retrieve data
- **`POST`** = Create new data
- **`.json()`** = Parse JSON response
- **Status codes** = 200 (OK), 404 (Not Found), 500 (Server Error)
- **Authentication** = API keys in headers
- **Error handling** = Use `try/except` with `raise_for_status()`
- **Timeouts** = Prevent hanging requests

---

## What's Next?

Ready for more? Continue to **[Lesson 14: Testing Your Code](14-testing.md)** — learn to write tests and ensure your code works correctly! ✅

---

**Your turn:** Try the exercises above! APIs are everywhere in modern development. Ask if you get stuck! 💛🌞
