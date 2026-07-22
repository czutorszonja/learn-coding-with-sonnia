# 03 — S3: Store Everything in the Cloud

**← Back to [Lesson 02: IAM: Who Gets to Do What](02-aws-iam.md)**


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

### Setup

1. Create a bucket with the **same name as your domain** (or any name)
2. Enable **Static website hosting** in bucket properties
3. Upload your HTML files
4. Make them publicly readable

```
Bucket: my-static-site-szonja
├── index.html
├── style.css
└── script.js
```

Enable public access:

```bash
# Bucket policy (allows public reads)
aws s3api put-bucket-policy --bucket my-static-site-szonja --policy '{
  "Version": "2012-10-17",
  "Statement": [{
    "Effect": "Allow",
    "Principal": "*",
    "Action": "s3:GetObject",
    "Resource": "arn:aws:s3:::my-static-site-szonja/*"
  }]
}'
```

Turn on static hosting:

```bash
aws s3 website s3://my-static-site-szonja/ --index-document index.html
```

Your site is now live at:
`http://my-static-site-szonja.s3-website-eu-west-2.amazonaws.com`

**Cost:** ~$0.023/GB/month for storage + pennies for data transfer. A personal blog costs about the same as a coffee per year.

---

## 5. Versioning — Never Lose a File

Enable **versioning** on a bucket and S3 keeps every version of every object.

```bash
aws s3api put-bucket-versioning \
  --bucket my-app-bucket \
  --versioning-configuration Status=Enabled
```

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
# Move old logs to cheaper storage
aws s3 cp logs/ s3://my-logs/ --recursive
aws s3api put-object-tagging \
  --bucket my-logs \
  --key old-log.gz \
  --tagging '{"TagSet": [{"Key": "class", "Value": "glacier"}]}'
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
4. Create a simple `index.html` with your name on it. Host it as a static website.
5. Use the AWS Console to browse to a file and generate a pre-signed URL. Open it in an incognito window — does it work?

**Continue to [Lesson 04: EC2: Your First Cloud Server](04-aws-ec2.md)**

> **Next up:** Lesson 04 — EC2: Virtual Servers in the Cloud.
