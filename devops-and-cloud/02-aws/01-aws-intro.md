# 01 — Welcome to the Cloud: AWS Basics

Docker taught us how to package apps consistently. Now we need somewhere to **run them** that's not our laptop.

That's the cloud — someone else's computers that you can use over the internet. AWS is the biggest one.

---

## 1. What Is Cloud Computing?

Before the cloud, if you wanted to run a website, you bought a physical server:

- Ordered a machine from Dell ($5,000+)
- Waited 2 weeks for delivery
- Plugged it in at your office or a data centre
- If it broke, you fixed it yourself
- If you needed more capacity, you bought another one (2 more weeks)

**The cloud changed everything.** Now you click a button and get a server instantly. Pay by the hour (or second). When you're done, delete it. No hardware, no waiting, no breaking.

AWS is the biggest provider, but the concepts are the same everywhere (Google Cloud, Azure, DigitalOcean).

---

## 2. AWS Global Infrastructure

AWS has **data centres** all over the world, organised into **Regions** and **Availability Zones**.

```
Region (e.g. eu-west-2 London)
├── Availability Zone A (a physical data centre)
├── Availability Zone B (a separate building, miles away)
└── Availability Zone C (another separate building)

Region (e.g. us-east-1 Virginia)
├── Availability Zone A
├── Availability Zone B
└── Availability Zone C
```

- **Region** = a geographic area (London, Frankfurt, Sydney, etc.)
- **Availability Zone (AZ)** = one or more data centres in that region
- **Edge Location** = a smaller cache point for fast content delivery (CloudFront)

**Which region to pick?**
- Closest to your users (lower latency)
- Check what services are available in that region (not everything is everywhere)
- London (`eu-west-2`) is great for UK users
- The `us-east-1` (N. Virginia) region usually gets new services first

---

## 3. The Most Important AWS Services

There are **200+** AWS services. You'll probably use 10 regularly. Here are the ones that matter most:

| Service | What it does | Lesson |
|---|---|---|
| **IAM** | Users, permissions, security | 10 |
| **S3** | Store files (images, backups, static websites) | 11 |
| **EC2** | Virtual servers (run any software) | 12 |
| **Lambda** | Serverless functions (code that runs on-demand) | 13 |
| **ECS / Fargate** | Run Docker containers on AWS | 14 |
| **RDS** | Managed databases (PostgreSQL, MySQL, etc.) | 14 |
| **CloudFront** | Content delivery network (fast worldwide) | 11 |
| **Route 53** | DNS (domain names) | — |
| **VPC** | Virtual network (security, isolation) | 14 |

---

## 4. The Free Tier

AWS is famously "pay as you go" — but it's also infamous for surprise bills. The **Free Tier** is your safety net for learning:

### Always Free
- **IAM** — always free
- **Lambda** — 1 million requests/month free
- **S3** — 5 GB storage free
- **CloudFront** — 1 TB transfer free

### 12 Months Free (from sign-up)
- **EC2** — 750 hours/month of a t2.micro instance (a small virtual server)
- **RDS** — 750 hours/month of a db.t2.micro database
- **S3** — 20,000 GET requests

### ⚠️ Cost Warning
AWS will happily let you provision expensive resources and send you a bill. **Set up billing alerts first** (we'll do this in the IAM lesson). Never leave unused resources running.

---

## 5. Real-World Scenario

**Why AWS over just Docker on your laptop?**

You've built the URL shortener from lesson 08. It works great locally. But:

- **Your laptop goes to sleep** → the app goes offline
- **Your friend wants to use it** → they need to be on your WiFi
- **It gets popular** → your laptop can't handle 10,000 requests/second
- **The database gets corrupted** → you didn't set up backups

AWS solves all of these. You deploy your Docker containers to EC2 or ECS, put a load balancer in front, use RDS for the database with automated backups, and CloudFront for fast global access.

The app doesn't change — you just run it on better hardware that you rent by the hour.

---

## 6. Setting Up Your AWS Account

1. Go to [aws.amazon.com](https://aws.amazon.com/)
2. Click **Create an AWS Account**
3. Enter email and password
4. Choose **Personal** account type
5. Enter billing info (you need a card — but everything in these tutorials stays in the free tier)
6. Verify your phone number
7. Choose the **Free** support plan

**Once signed in:**
- Go to **Billing Dashboard** → **Billing Preferences**
- Enable **Receive Free Tier Usage Alerts**
- Create a **budget** for $5/month (just in case)

Then go to **IAM** (Identity and Access Management) — we'll set up proper access in lesson 10.

> ⚠️ **Keep your root account safe.** The email you signed up with is the "root user" — it has full access to everything. Enable Multi-Factor Authentication (MFA) on it immediately. Then create IAM users for everyday work.

---

## 🔨 Your Turn

Before moving on:

1. Create your AWS account (if you haven't already)
2. Set up a billing alert for $5/month in the Billing Dashboard
3. Enable MFA on your root account
4. Open the AWS Management Console and find the region selector (top-right) — switch to **London (eu-west-2)**
5. Search for "S3" in the services search bar — we'll use it next

**Continue to [Lesson 02: IAM: Who Gets to Do What](02-aws-iam.md)**
