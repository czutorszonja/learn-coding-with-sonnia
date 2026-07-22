# 02 — IAM: Who Gets to Do What

**← Back to [Lesson 01: Welcome to the Cloud: AWS Basics](01-aws-intro.md)**


IAM (Identity and Access Management) is the most important AWS service — and the most skipped by beginners.

**IAM controls who can do what in your AWS account.** Misconfigure IAM and either:
- A hacker gets into your account and launches $50,000 worth of Bitcoin miners
- Or your own code can't access the database you created

Spend time here. It's worth it.

---

## 1. The Mental Model

Everything in IAM is about one question: **who gets to do what to which resource?**

```
Who (user/role) ──▶ What action ──▶ Which resource
     │                    │               │
  "almond"            "s3:GetObject"  "bucket/sonia/*"
```

---

## 2. IAM Building Blocks

| Concept | What it is | Example |
|---|---|---|
| **Root User** | The account owner (email sign-up). Full access to everything. | Use only for account setup and billing |
| **IAM User** | A person or service that needs access | `szonja`, `deploy-bot` |
| **IAM Group** | A collection of users with the same permissions | `developers`, `admins` |
| **IAM Role** | Temporary permissions for something to assume | A role an EC2 instance uses to access S3 |
| **Policy** | A JSON document that defines permissions | "Allow s3:GetObject on bucket X" |

---

## 3. First Steps: Create an Admin User

**Never use the root account for daily work.** Create an admin user for yourself.

In the AWS Console:
1. Search for **IAM**
2. Go to **Users** → **Create user**
3. User name: `admin-szonja`
4. Check **Provide user access to the management console**
5. Choose **I want to create an IAM user**
6. Set a password (or auto-generate)
7. **Don't require password reset** (for personal accounts)
8. Next: **Permissions**
9. Click **Attach policies directly**
10. Search for and check **AdministratorAccess**
11. Next → Create user

Now **log out** of the root account and **log in** as `admin-szonja`. From now on, do everything from this user.

---

## 4. The Principle of Least Privilege

The golden rule of cloud security: **give only the permissions needed, nothing more.**

```
❌ Full admin access for a web server
✅ Only s3:GetObject on its specific bucket
✅ Only ec2:DescribeInstances for a monitoring script
```

A web server doesn't need to delete databases. A developer doesn't need to change billing. Grant the minimum.

---

## 5. Policies — Written Out

Policies look scary (JSON) but are simple once you understand the structure:

```json
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Effect": "Allow",
      "Action": [
        "s3:GetObject",
        "s3:PutObject"
      ],
      "Resource": "arn:aws:s3:::my-app-bucket/uploads/*"
    }
  ]
}
```

Translation: **Allow** the actions `s3:GetObject` and `s3:PutObject` on any object under the `uploads/` folder in the bucket `my-app-bucket`.

The ARN (Amazon Resource Name) identifies the specific resource. Format:
```
arn:partition:service:region:account-id:resource
arn:aws:s3:::my-bucket/*                          ← S3 bucket
arn:aws:ec2:eu-west-2:123456789:instance/*        ← EC2 instances
```

---

## 6. Access Keys: For Code (Not Logins)

Your code (running locally or on EC2) can't log in with a username and password. It needs **access keys**.

```bash
# In IAM → Users → your-user → Security Credentials
# Create Access Key

# Then in your terminal:
export AWS_ACCESS_KEY_ID=AKIAIOSFODNN7EXAMPLE
export AWS_SECRET_ACCESS_KEY=wJalrXUtnFEMI/K7MDENG/bPxRfiCYEXAMPLEKEY
```

**Never commit access keys to Git.** Ever. Use environment variables or AWS Secrets Manager.

---

## 7. IAM Roles: Permissions for AWS Services

Roles are for when an AWS service needs to do something — like an EC2 instance reading from S3.

```
EC2 Instance (assumes a Role)
    │
    ▼
[IAM Role with s3:GetObject policy]
    │
    ▼
S3 Bucket
```

You don't put access keys on the EC2 instance. You attach an IAM Role to it. AWS handles the credentials automatically — they rotate, and no one can steal them from a config file.

---

## 8. Common IAM Setup for a Small Project

```
Root User (only for billing + MFA)
    │
    └── IAM Group: admins
    │       └── admin-szonja (console access + admin policy)
    │
    └── IAM Group: developers
    │       └── dev-user (limited: can read logs, restart EC2, deploy)
    │
    └── IAM Role: ecs-task-role
    │       └── Allows ECS tasks to write logs to CloudWatch
    │
    └── IAM Role: lambda-basic-execution
            └── Allows Lambda to write logs and access DynamoDB
```

---

## 🔨 Your Turn

1. Create an admin IAM user for yourself (if you haven't already)
2. Create an IAM group called `developers` with a policy that allows:
   - `s3:GetObject` and `s3:PutObject` on a bucket called `my-app-{yourname}/*`
   - `ec2:DescribeInstances` (read-only)
   - `logs:DescribeLogGroups` and `logs:GetLogEvents`
3. Create an IAM user in that group named `ci-deploy` (for automated deployments) — generate access keys for it
4. Open **Credential Report** in IAM → check when each user last used their credentials

**Continue to [Lesson 03: S3: Store Everything in the Cloud](03-aws-s3.md)**

> **Next up:** Lesson 03 — S3: The World's Most Used Storage Service.
