# 03 — Elastic Beanstalk: Deploy Your App Without the Server Headache

**← Back to [Lesson 02: IAM: Who Gets to Do What](02-aws-iam.md)**

You've written an app. Now you want it on the internet. You *could* rent an EC2 server and set up the operating system, install Python, configure nginx, keep it patched... or you could upload your code and let AWS handle all of it.

That's **Elastic Beanstalk**.

---

## 1. What Is Elastic Beanstalk?

Elastic Beanstalk is AWS's **Platform as a Service (PaaS)**. You give it your code — it gives you a running, public website.

- **You provide:** your app's code (a zip file or a Git repo)
- **AWS provides:** servers, load balancer, auto scaling, health monitoring, security groups, even automatic OS patching

Under the hood it's built on **EC2** (which you'll meet properly in Lesson 05) — Beanstalk just does the boring setup for you. If you've used **Heroku**, **Render** or **Railway**, it's the same idea, but inside AWS.

---

## 2. What Beanstalk Sets Up For You

When you create an environment, Beanstalk quietly creates a whole stack:

```
Your code (zip file)
        │
        ▼
Elastic Beanstalk environment
├── EC2 instances        → run your app
├── Load balancer        → spread traffic between instances
├── Auto Scaling group   → add/remove instances as traffic changes
├── Security group       → allows HTTP from anywhere
├── S3 bucket            → stores your uploaded code versions
└── CloudWatch           → health checks + logs
```

All of it is visible in the Beanstalk dashboard — **Health: green** means your app is live and healthy.

---

## 3. Deploying Your First App

### Step 1: Create the application

1. AWS Console → search **Elastic Beanstalk** → **Create Application**
2. Application name: `my-first-app`
3. Platform: **Python** (pick whatever matches your app — Node.js, Java, etc.)

### Step 2: Choose an environment tier

| Tier | What it does | When to use |
|---|---|---|
| **Single instance** | One EC2 instance, no load balancer | Learning, dev, low traffic (fits the free tier) |
| **Load balanced** | Multiple instances + load balancer | Real apps, high traffic, auto scaling |

> **📝 Exam note:** You need to know the difference. Load balanced environments add a **load balancer** in front of your instances and can **auto-scale**; single instance environments can't.

### Step 3: Upload your code

Create a zip containing your app. For a Python (Flask) app, that's two files:

```python
# app.py
from flask import Flask

app = Flask(__name__)

@app.route("/")
def home():
    return "Hello from Elastic Beanstalk! 🌱"

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
```

```text
# requirements.txt
flask
```

Zip them up (`app.zip`), then **Upload your code** → choose the file → **Create environment**.

### Step 4: Wait for green

Beanstalk takes a few minutes to provision everything. Watch the dashboard until **Health turns green** — then open the **environment URL**:

```
http://my-first-app.eu-west-2.elasticbeanstalk.com
```

🎉 Your app is live on the internet.

---

## 4. The Public URL (Exam Note!)

Beanstalk environments are **public by default**:

- Your app gets a public URL: `http://<environment-name>.<region>.elasticbeanstalk.com`
- The security group automatically allows **HTTP (port 80) from anywhere** (`0.0.0.0/0`) so the world can reach it

In **real life** you'd lock this down: restrict access, add HTTPS, put a WAF in front. But for learning (and exams!), the environment being publicly reachable is exactly what makes it work — this is the one place it's OK.

---

## 5. Updating Your App

Code changes are easy:

1. Console → your environment → **Upload and deploy**
2. Pick the new zip → **Deploy**
3. Beanstalk rolls out the update — usually with **zero downtime**

The old versions stay in your S3 bucket, so you can roll back to a previous version any time.

---

## 6. CLI Version (Bonus)

Prefer the terminal? The EB CLI does the same thing:

```bash
eb init            # set up the project (pick region + platform)
eb create          # create the environment
eb deploy          # deploy your code
eb open            # open the environment URL in your browser
```

---

## 7. Real-World: When to Use What

| Need | Use |
|---|---|
| Deploy an app fast, don't want to manage servers | **Elastic Beanstalk** |
| Full control of the server, custom software | **EC2** (Lesson 05) |
| Tiny event-driven functions, pay per request | **Lambda** (Lesson 06) |
| Containerised apps that need to scale | **ECS / Fargate** (Lesson 07) |

---

## 8. Cleaning Up

Beanstalk itself is free — but you pay for the **EC2 instance and load balancer underneath**. Don't leave it running!

1. **Terminate environment** (frees the EC2 + load balancer)
2. **Delete application** (removes the S3 bucket with your code versions)

---

## 🔨 Your Turn

1. Create an app + environment and deploy the Flask app above
2. Open the environment URL — you should see the 🌱 message
3. Change the message, re-zip, **Upload and deploy**, refresh the page
4. Find the auto-created **security group** in EC2 → confirm HTTP is open to `0.0.0.0/0`
5. (Exam prep) Write down the environment URL format and which settings make it public
6. **Important:** Terminate the environment when you're done

**Continue to [Lesson 04: S3: Store Everything in the Cloud](04-aws-s3.md)**
