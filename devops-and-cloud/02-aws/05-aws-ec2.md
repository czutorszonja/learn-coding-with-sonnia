# 05 — EC2: Your First Cloud Server

**← Back to [Lesson 04: S3: Store Everything in the Cloud](04-aws-s3.md)**


EC2 (Elastic Compute Cloud) is AWS's virtual server service. You choose the specs, launch it, SSH in, and treat it like a computer in the cloud.

---

## 1. What Is an EC2 Instance?

An **instance** is a virtual machine running on AWS hardware.

```
Your Laptop                         EC2 Instance
┌──────────────────┐                ┌──────────────────┐
│ Your terminal    │────SSH────▶    │ Linux / Windows  │
│                  │                │ Your app code    │
│                  │                │ CPU: 2 cores     │
│                  │                │ RAM: 8 GB        │
│                  │                │ Disk: 100 GB SSD │
└──────────────────┘                │ IP: 54.123.45.67 │
                                    └──────────────────┘
                                    Running 24/7 in AWS
```

---

## 2. Instance Types

AWS names instances like this: `t2.micro`, `t3.medium`, `c5.large`

```
[Family] [Generation] . [Size]
    t          2         .  micro
    │          │              │
    │          │              └── Size (micro = smallest)
    │          └── Generation (2 = second version)
    └── Family (t = general purpose)
```

| Family | Use case | Example |
|---|---|---|
| **t** (general) | Web servers, small apps — burstable | t3.micro |
| **c** (compute) | Data processing, video encoding | c5.large |
| **r** (memory) | Databases, caching, in-memory ops | r5.large |
| **m** (balanced) | General mid-range workloads | m5.large |

The **free tier** gives you 750 hours/month of a `t2.micro` or `t3.micro` — enough for one server running 24/7.

---

## 3. Launching Your First EC2 Instance

### Via Console

1. Go to **EC2** → **Instances** → **Launch Instance**
2. Name: `my-first-server`
3. AMI (Amazon Machine Image): **Amazon Linux 2023** (free tier eligible)
4. Instance type: **t2.micro** or **t3.micro** (free tier)
5. Key pair: **Create new key pair**
   - Name: `my-keys`
   - Type: **RSA**
   - Format: **.pem** (for Mac/Linux) or **.ppk** (for PuTTY on Windows)
   - **Download the .pem file and save it somewhere safe.** You can't download it again.
6. Network settings: Check **Allow SSH traffic from** → **Anywhere** (for learning) or **My IP** (safer)
7. **Launch instance**

Wait ~30 seconds. You'll see it go from `pending` → `running`.

### Connect via SSH

**Choose your OS. You only run ONE of these blocks:**

**💻 macOS / Linux:**

```bash
# Make sure your key file isn't publicly visible (only needed on Mac/Linux)
chmod 400 ~/Downloads/my-keys.pem

# Connect
ssh -i ~/Downloads/my-keys.pem ec2-user@<public-ip-address>
```

**🪟 Windows (PowerShell or CMD):**

> **There is no `chmod` on Windows — skip it entirely.** If you typed `chmod` and got "not recognized as a command", that's expected here. Windows 10/11 come with a built-in OpenSSH client, so you can SSH directly:

```powershell
ssh -i C:\Users\Szonja\Downloads\my-first-server-key-pair.pem ec2-user@<public-ip-address>
```

> Replace `Szonja` with your actual Windows username, and make sure the path points to where your browser **actually saved** the `.pem` key (usually `Downloads`).
>
> **If SSH complains about key permissions** ("UNPROTECTED PRIVATE KEY FILE"), fix it:
> 1. Right-click your `.pem` file → **Properties** → **Security** → **Advanced**
> 2. **Disable inheritance** → **Remove** all inherited permissions
> 3. **Add** yourself (your Windows account) with **Full Control**
> 4. Apply and retry SSH
>
> Or simply move the `.pem` into `C:\Users\YourName\.ssh\` and skip the permissions dance entirely.

*(Find the public IP in the EC2 console — under your instance's details.)*

You're now inside a real Linux server in AWS! Try:

```bash
whoami          # → ec2-user
cat /etc/os-release  # → Amazon Linux info
df -h           # disk space
free -h         # memory
uptime          # how long it's been running
```

---

## 4. Security Groups — Your Firewall

A **Security Group** is a virtual firewall attached to your EC2 instance. It controls what traffic can reach it.

When you launched the instance, a default security group was created.

```
Inbound Rules (what's allowed in):
┌─────────────────────────────────────────┐
│ SSH      │ TCP :22  │ My IP     │ Allow │
├─────────┼─────────┼─────────┼──────┤
│ HTTP     │ TCP :80  │ Anywhere │ Allow │
├─────────┼─────────┼─────────┼──────┤
│ HTTPS    │ TCP :443 │ Anywhere │ Allow │
├─────────┼─────────┼─────────┼──────┤
│ Custom   │ TCP :8080│ My IP    │ Allow │ (for a custom port app)
└─────────────────────────────────────────┘

Outbound Rules (all traffic allowed out — usually fine)
```

> **🔑 Match the port to the rules!** The app in Section 5 runs on **port 80** (`app.run(host='0.0.0.0', port=80)`). For anyone to reach it over the internet, the security group must **allow inbound TCP on port 80 from Anywhere** — that's the **HTTP** rule shown above. The `Custom :5000` row in older versions of this table was a leftover; our app uses port 80, so HTTP :80 is the one that matters.

> If you change the app to a different port (say **8080**, like in "Your Turn" step 5), you MUST also add a matching **Custom TCP** rule for that port, or the traffic gets blocked at the firewall and your page won't load. A classic gotcha: the app runs fine on the server (you see the logs), but the browser times out — that's almost always the security group.

**Rules of thumb:**
- Allow only what you need (don't open port 22 to everyone)
- Use "My IP" for SSH, not "Anywhere"
- Open app ports (80/443) to "Anywhere" only if it's a public website
- **Edit a rule:** select your instance → **Security** tab → your security group → **Inbound rules** → **Edit inbound rules**

---

## 5. Running a Simple App on EC2

Let's deploy a real web app on your EC2 instance. We'll create a simple Flask API **directly on the server** — no extra tools needed.

> **👉 Where do I type this?** Make sure you're **inside the SSH session** you opened in Section 3 — the one where your terminal prompt shows `[ec2-user@ip-…]`. If your prompt still looks like your laptop (e.g. `szonja@MacBook` or `C:\Users\…`), you're **not** on the server yet. Every line below runs **on the EC2 server**, not on your laptop and not in the AWS console. Paste the whole block into your SSH terminal.

```bash
# Update packages and install Python
sudo yum update -y
sudo yum install python3 python3-pip -y

# Install Flask
pip3 install flask

# Create a simple app
cat > /home/ec2-user/app.py << 'EOF'
from flask import Flask, jsonify

app = Flask(__name__)

@app.route('/')
def home():
    return "Hello from EC2! 🌐"

@app.route('/about')
def about():
    return jsonify({"name": "My EC2 App", "platform": "AWS"})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=80)
EOF

# Run it (in the background)
sudo python3 /home/ec2-user/app.py &
```

Now open your browser and go to `http://<your-ec2-public-ip>`. You should see "Hello from EC2!"

**Your app is live on the internet.** 🌐

> **Note:** We're running the dev server here. For production, you'd use Gunicorn or uWSGI behind nginx. But for learning, this works fine.

---

## 6. Elastic IP — Don't Lose Your Address

If you stop and start your EC2 instance, it gets a **new IP address**. That's annoying.

An **Elastic IP** is a static, fixed IP you can attach to your instance.

1. Go to **EC2** → **Elastic IPs**
2. **Allocate Elastic IP address**
3. Select it → **Actions** → **Associate Elastic IP address**
4. Pick your instance

Now your IP won't change. Note: Elastic IPs cost ~$0.005/hour if they're **not attached** to a running instance. Attached to a running instance, they're free.

---

## 7. User Data — Automate Setup at Launch

You can provide a script that runs automatically when the instance starts:

```bash
#!/bin/bash
yum update -y
yum install python3 python3-pip -y
pip3 install flask

# Create and run a simple web app
cat > /home/ec2-user/app.py << 'APPEOF'
from flask import Flask
app = Flask(__name__)
@app.route('/')
def hello():
    return "Hello from EC2! 🌐"
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=80)
APPEOF

# Start the app
cd /home/ec2-user && python3 app.py &
```

Paste this into the **User data** section when launching an instance. The first time it boots, it sets up Python and starts your web app automatically. No manual SSH needed.

---

## 8. Cleaning Up (IMPORTANT)

EC2 costs money even when idle. When you're done:

```bash
# Stop (not terminate) — keeps the instance, you can start later
aws ec2 stop-instances --instance-ids i-1234567890

# Terminate — deletes the instance permanently
aws ec2 terminate-instances --instance-ids i-1234567890
```

**Always terminate when you're done learning.** Or at least stop it. A running t2.micro costs ~$8.50/month. A stopped one costs $0.

---

## 🔨 Your Turn

1. Launch a t2.micro EC2 instance with Amazon Linux
2. SSH into it and run `uname -a` — what kernel version is it running?
3. Install Python and Flask, then run the sample app from section 5
4. Visit your instance's public IP in a browser — can you see your app?
5. Modify the security group to allow port 8080. Create a second app listening on port 8080 and visit `<ip>:8080`.
6. **Important:** Terminate the instance when you're done.

**Continue to [Lesson 06: Lambda: Code Without Servers](06-aws-lambda.md)**
