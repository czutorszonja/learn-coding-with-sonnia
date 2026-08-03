# 04 — S3: Store Everything in the Cloud

**← Back to [Lesson 03: Elastic Beanstalk: Deploy Your App Without the Server Headache](03-aws-elastic-beanstalk.md)**


S3 is **the** AWS service. It's simple, cheap, and you'll use it in almost every project.

**What it is:** A place to store files — images, videos, backups, HTML, logs, anything. Files are called **objects**, stored in **buckets**.

---

## 1. The Mental Model

Think of S3 as a **giant, internet-accessible filing cabinet**.

```
S3 Bucket ("my-app-bucket")
├── images/
│   ├── logo.png
│   └── banner.jpg
├── backups/
│   └── db-2026-07-21.sql
└── index.html
```

- **Bucket** = a folder at the top level (globally unique name)
- **Object** = a file (any type) + metadata
- **Key** = the full path to an object (`images/logo.png`)
- **URL** = every object gets a URL like `https://my-app-bucket.s3.eu-west-2.amazonaws.com/images/logo.png`

---

## 2. Your First Bucket

### Via the Console

1. Go to **S3** in the AWS Console
2. Click **Create bucket**
3. Bucket name: `my-first-bucket-szonja` (must be **globally unique**)
4. Region: **eu-west-2** (London)
5. Leave the defaults (block public access — safe)
6. Click **Create**

### Via the AWS CLI

Install the CLI first:

```bash
brew install awscli           # Mac
# or
curl "https://awscli.amazonaws.com/awscli-exe-linux-x86_64.zip" -o "awscliv2.zip"
```

Configure it:

```bash
aws configure
# Enter your Access Key ID and Secret Access Key
# Default region: eu-west-2
# Output format: json
```

Then:

```bash
# Create a bucket
aws s3 mb s3://my-first-bucket-szonja --region eu-west-2

# List buckets
aws s3 ls

# Upload a file
echo "Hello, S3!" > hello.txt
aws s3 cp hello.txt s3://my-first-bucket-szonja/

# Download it
aws s3 cp s3://my-first-bucket-szonja/hello.txt ./downloaded.txt

# List contents
aws s3 ls s3://my-first-bucket-szonja/
```

---

## 3. S3 Storage Classes

Not all data is created equal. S3 has different storage tiers:

| Class | Use case | Cost | Retrieval |
|---|---|---|---|
| **S3 Standard** | Frequently accessed data | Higher | Instant |
| **S3 Intelligent-Tiering** | Unknown access patterns | Auto-optimised | Instant |
| **S3 Standard-IA** | Infrequent access (monthly) | Lower | Instant |
| **S3 One Zone-IA** | Non-critical, infrequent | Even lower | Instant |
| **S3 Glacier** | Archives (retrieved rarely) | Very low | Minutes to hours |
| **S3 Glacier Deep Archive** | Long-term backups | Cheapest | Up to 12 hours |

**Real-world tiering strategy:**
- **Standard:** Profile pictures, current data
- **Standard-IA:** Last month's logs
- **Glacier:** Audit records from 3 years ago
- **Deep Archive:** Legal document retention

---

## 4. Hosting a Static Website on S3

This is one of S3's best features. You can host a static site (HTML + CSS + JS) for pennies.

> ⚠️ **Two different places — don't confuse them.**
>
> Almost every task in this section can be done **either** in the **web console** (pointing and clicking in your browser) **or** the **command line** (typing `aws ...` commands). They do the same thing; you only need **one** path per task. The lesson shows you both, but you never mix them mid-task:
>
> - **Web console** = the AWS website you log into. Click around, use tabs and edit boxes.
> - **Command line (CLI)** = a terminal where you type commands. There are two places you can run them:
>   1. **AWS Cloud Shell** — a terminal built into the console. Look for the `>_` icon near the top-right of the AWS page, next to the region selector. Click it and a terminal opens *inside* your browser, already logged into AWS. No install needed. **This is the easiest place to type `aws ...` commands.**
>   2. **Your local terminal** — Terminal (Mac) / Command Prompt (Windows). Only use this if you've **installed the AWS CLI** (`aws --version` should print a version, not an error) **and** run `aws configure` once with your Access Key / Secret Key.
>
> If you're just getting it live as quickly as possible, **use the console** for the whole task — no CLI needed. The CLI steps are there for when you want to do it faster or script it.

### The goal

You want `index.html` (plus any `style.css`, `script.js`) sitting in a bucket, publicly readable, served as a website.

```
Bucket: my-static-site-szonja
├── index.html
├── style.css
└── script.js
```

### Steps, both paths

**1. Create the bucket** (name it the same as your domain, or anything unique)

- **Console:** S3 → **Create bucket** → name → leave defaults → Create.
- **CLI:** `aws s3 mb s3://my-static-site-szonja --region eu-west-2`

**2. Upload your HTML files** ← this is where they go

- **Console:** Open your bucket → **Objects** tab (this is the "files" view) → **Upload** button (top right) → drag your files in (or **Add files**) → **Upload** at the bottom.
- Make sure your files sit at the **root** of the bucket — the Objects tab shows `index.html`, `style.css`, `script.js` directly, **not** inside a subfolder. The site URL looks for `index.html` at the root.
- **CLI:** `aws s3 cp index.html s3://my-static-site-szonja/` (repeat for each file, or `aws s3 cp . s3://my-static-site-szonja/ --recursive` to grab everything in the current folder)

**3. Turn on static website hosting** (tells AWS "serve `index.html` as the homepage")

- **Console:** Bucket → **Properties** tab → scroll to **Static website hosting** → **Edit** → select **Enable** → set **Index document** to `index.html` → Save. Note the **Bucket website endpoint** URL that appears (that's your live site address).
- **CLI:** `aws s3 website s3://my-static-site-szonja/ --index-document index.html`

**4. Make the files publicly readable** (the crucial `index.html` would otherwise 403 in the browser)

- **Console:** Bucket → **Permissions** tab → scroll to **Bucket policy** → **Edit** → paste the JSON below → replace `my-static-site-szonja` with **your** bucket name → Save. (If you get a "block public access" error, finish step 5 first, then come back.)
- **CLI:** See the policy JSON below. In Cloud Shell or your local terminal, save it to a file then apply it with `aws s3api put-bucket-policy`.

**5. Turn **off** "Block public access" for the bucket** (a newer safety default that blocks the public policy above)

- **Console:** Bucket → **Permissions** tab → top section **Block public access (bucket settings)** → **Edit** → **uncheck** all four boxes → Save.
- **CLI:** `aws s3api put-public-access-block --bucket my-static-site-szonja --public-access-block-configuration BlockPublicAcls=false,IgnorePublicAcls=false,BlockPublicPolicy=false,RestrictPublicBuckets=false`
- ⚠️ Only do this on a bucket you *intend* to be public. For anything private, leave it on.

### The bucket policy JSON

This is the JSON you paste in the console (step 4) **or** save to a file for the CLI:

```json
{
  "Version": "2012-10-17",
  "Statement": [{
    "Effect": "Allow",
    "Principal": "*",
    "Action": "s3:GetObject",
    "Resource": "arn:aws:s3:::my-static-site-szonja/*"
  }]
}
```

> 💡 **What this says:** anyone (`"Principal": "*"`) can read (`s3:GetObject`) any object inside your bucket. The `/*` at the end of the Resource means "everything inside the bucket".

### Enabling the public policy via the CLI (only if you chose the CLI path)

The command needs the policy saved to a file so your terminal doesn't mangle the quotes:

```bash
# Save the policy to a file to avoid shell quoting issues
cat > bucket-policy.json << EOF
{
  "Version": "2012-10-17",
  "Statement": [{
    "Effect": "Allow",
    "Principal": "*",
    "Action": "s3:GetObject",
    "Resource": "arn:aws:s3:::my-static-site-szonja/*"
  }]
}
EOF
aws s3api put-bucket-policy --bucket my-static-site-szonja --policy file://bucket-policy.json
```

> **💻 Windows PowerShell / CMD note:** Heredocs (`cat > file << EOF`) don't work in PowerShell or CMD. Create the file manually: make a new file called `bucket-policy.json`, paste the JSON above into it, save, then run:
> ```powershell
> aws s3api put-bucket-policy --bucket my-static-site-szonja --policy file://bucket-policy.json
> ```
> You need the local AWS CLI installed for this (PowerShell/CMD can't use Cloud Shell).

### Test it

Open the **Bucket website endpoint** from step 3 in an **incognito/private** browser window:
`http://my-static-site-szonja.s3-website-eu-west-2.amazonaws.com`

From a normal window it may look "worked" just because you're logged in; incognito makes sure a random visitor can really see it. A `403 Access Denied` means a public-read step got missed. An empty page usually means files aren't at the bucket root.

**Cost:** ~$0.023/GB/month for storage + pennies for data transfer. A personal blog costs about the same as a coffee per year.

---

## 5. Versioning — Never Lose a File

Enable **versioning** on a bucket and S3 keeps every version of every object.

```bash
aws s3api put-bucket-versioning --bucket my-app-bucket --versioning-configuration Status=Enabled
```

> 💻 **Windows tip:** PowerShell users write the whole thing on one line (no backtick needed for short commands). CMD users can use `^` if needed, but this one fits on one line.

Now if someone overwrites or deletes a file, you can restore the old version.

```
Object: db-backup.sql
├── Version 1 (original)
├── Version 2 (overwritten with corrupted data)
├── Version 3 (overwritten with corrected data)
└── Delete marker (file "deleted" but recoverable)
```

---

## 6. Real-World Use Cases

### App: User Uploads
Users upload profile pictures → store in S3 → serve via CloudFront (CDN) for fast global loading.

### Backup Automation
```bash
# Script to backup database daily
pg_dump mydb > /tmp/backup-$(date +%F).sql
aws s3 cp /tmp/backup-$(date +%F).sql s3://my-backups/database/
```

### Log Archive
```bash
# macOS / Linux — Move old logs to cheaper storage
aws s3 cp logs/ s3://my-logs/ --recursive
aws s3api put-object-tagging --bucket my-logs --key old-log.gz --tagging '{"TagSet": [{"Key": "class", "Value": "glacier"}]}'

# Windows PowerShell (write tagging JSON to file first to avoid quoting issues):
# Create a file tagging.json with: {"TagSet": [{"Key": "class", "Value": "glacier"}]}
# aws s3api put-object-tagging --bucket my-logs --key old-log.gz --tagging file://tagging.json
```

### Serving Static Assets
Images, CSS, JS files for your web app → S3 → CloudFront → user's browser. Cheap, fast, infinitely scalable.

---

## 7. Security Rules

By default, everything in S3 is **private**. You control access through:

1. **Bucket Policies** — permissions for the whole bucket (public access, restrict by IP, etc.)
2. **IAM Policies** — which users/roles can access which buckets
3. **Pre-signed URLs** — temporary links for specific files (valid for 1 hour, great for paid downloads)

```python
# Generate a pre-signed URL with boto3 (Python)
import boto3
s3 = boto3.client('s3')
url = s3.generate_presigned_url(
    'get_object',
    Params={'Bucket': 'my-app-bucket', 'Key': 'premium-report.pdf'},
    ExpiresIn=3600
)
print(url)  # Temporary link, expires in 1 hour
```

---

## 🔨 Your Turn

1. Create an S3 bucket (via console or CLI)
2. Upload a text file. Download it to a different location — verify it matches.
3. Enable versioning. Upload the same file twice with different content. List versions.
4. Create a simple `index.html` with your name on it. Host it as a static website — follow the two-path guide in **Section 4**, and test it in a private window.
5. Use the AWS Console to browse to a file and generate a pre-signed URL. Open it in an incognito window — does it work?

**Continue to [Lesson 05: EC2: Your First Cloud Server](05-aws-ec2.md)**
