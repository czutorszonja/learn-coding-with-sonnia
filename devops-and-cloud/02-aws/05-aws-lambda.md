# 05 — Lambda: Code Without Servers

**← Back to [Lesson 04: EC2: Your First Cloud Server](04-aws-ec2.md)**


EC2 gives you a whole server. But what if you only need to **run a function** when something happens? No server to manage, no SSH, no patching — just code that runs when triggered.

That's **Lambda** — AWS's serverless compute service.

---

## 1. The Idea

```
Traditional:                    Serverless:
┌──────────────────────┐       ┌──────────────────────┐
│ Provision EC2        │       │ Write function        │
│ Patch OS             │       │ Upload to Lambda      │
│ Install dependencies │       │ Set a trigger         │
│ Start your app       │       │ Done ✓               │
│ Monitor uptime       │       │                       │
│ Auto-scale           │       │ AWS handles the rest  │
└──────────────────────┘       └──────────────────────┘
```

Lambda runs your code in response to events and charges only for the milliseconds it runs. No running server = no idle cost.

**Real-world use cases:**
- Resize image when uploaded to S3
- Process a database backup every night
- Validate form data from a webhook
- Send a welcome email after user sign-up

---

## 2. Your First Lambda Function

### Via Console

1. Go to **Lambda** → **Create function**
2. **Author from scratch**
3. Name: `hello-lambda`
4. Runtime: **Python 3.13**
5. Architecture: **x86_64**
6. Permissions: **Create a new role with basic Lambda permissions**
7. Click **Create function**

You'll see the Lambda editor with starter code:

```python
import json

def lambda_handler(event, context):
    # event = what triggered this function
    # context = info about the runtime environment
    return {
        'statusCode': 200,
        'body': json.dumps('Hello from Lambda!')
    }
```

Click **Test** → **Create new test event** → Event name: `test1` → Click **Save** → Click **Test**.

You should see:

```
Execution result: succeeded
Response: {"statusCode": 200, "body": "\"Hello from Lambda!\""}
```

**That's it.** You ran code in the cloud without managing a server.

---

## 3. The Magic — Triggers

Lambda is useless without triggers. A trigger is an AWS event that invokes your function automatically.

Common triggers:

| Trigger | When it fires | Example |
|---|---|---|
| **S3** | Object created/deleted in a bucket | Resize uploaded images |
| **API Gateway** | HTTP request to an endpoint | Build a serverless API |
| **DynamoDB** | Data changed in a table | Sync to another service |
| **SQS** | Message in a queue | Process background jobs |
| **CloudWatch Events** | Scheduled time | Daily backup at 2 AM |
| **SES** | Email received | Auto-reply or filter |

---

## 4. Real-World: Generate Thumbnails on Upload

This is the classic Lambda use case. User uploads a photo → S3 triggers Lambda → Lambda resizes the image → saves thumbnail to another bucket.

### Step 1: Create buckets

```bash
aws s3 mb s3://uploads-szonja --region eu-west-2
aws s3 mb s3://thumbnails-szonja --region eu-west-2
```

### Step 2: Write the Lambda function

```python
import boto3
from PIL import Image
import io
import os

s3 = boto3.client('s3')

def lambda_handler(event, context):
    # Get the bucket and key from the S3 event
    bucket = event['Records'][0]['s3']['bucket']['name']
    key = event['Records'][0]['s3']['object']['key']

    # Download the image from S3
    response = s3.get_object(Bucket=bucket, Key=key)
    image_data = response['Body'].read()

    # Resize it
    img = Image.open(io.BytesIO(image_data))
    img.thumbnail((200, 200))

    # Save to thumbnails bucket
    buffer = io.BytesIO()
    img.save(buffer, 'JPEG')
    buffer.seek(0)

    thumb_bucket = os.environ.get('THUMBNAIL_BUCKET', 'thumbnails-szonja')
    s3.put_object(
        Bucket=thumb_bucket,
        Key=f'thumb-{key}',
        Body=buffer,
        ContentType='image/jpeg'
    )

    return {'statusCode': 200}
```

### Step 3: Add the S3 trigger

1. In Lambda console → Add trigger
2. Select **S3**
3. Bucket: `uploads-szonja`
4. Event type: **All object create events**
5. **Acknowledge** recursive invocation warning

### Step 4: Add a layer for Pillow

Lambda doesn't have Pillow installed by default. You need to add a **Lambda Layer** (a ZIP of the library):

```bash
# Build Pillow as a Lambda layer
# Or use AWS's publicly available one:
# ARN: arn:aws:lambda:eu-west-2:770693421928:layer:Klayers-p313-Pillow:1
```

### Step 5: Test

Upload a JPEG to the `uploads-szonja` bucket. Within seconds, a thumbnail appears in `thumbnails-szonja`.

---

## 5. Lambda Limits (Important)

| Limit | Value |
|---|---|
| Memory | 128 MB – 10,240 MB |
| Timeout | 1 second – 15 minutes |
| Code size | 250 MB (compressed), 50 MB (ZIP direct) |
| Concurrent executions | 1,000 (soft limit) |
| Environment variables | 4 KB total |

**If your function runs longer than 15 minutes → use ECS or EC2 instead.**

---

## 6. Lambda + API Gateway: Serverless API

Combine Lambda with API Gateway to create a fully serverless REST API — no EC2 needed.

```
HTTP Request → API Gateway → Lambda → Response
```

```python
# api-lambda.py
import json
import boto3

dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table('notes')

def lambda_handler(event, context):
    method = event['httpMethod']

    if method == 'GET':
        response = table.scan()
        return {
            'statusCode': 200,
            'body': json.dumps(response['Items'])
        }

    if method == 'POST':
        body = json.loads(event['body'])
        table.put_item(Item=body)
        return {
            'statusCode': 201,
            'body': json.dumps(body)
        }

    return {'statusCode': 405, 'body': 'Method not allowed'}
```

Steps:
1. Create a DynamoDB table called `notes`
2. Write the Lambda function above
3. Create an API Gateway REST API with `GET /notes` and `POST /notes` endpoints
4. Point both to your Lambda function
5. Deploy the API → get a URL

Now `curl https://your-api.execute-api.eu-west-2.amazonaws.com/prod/notes` works — no servers to manage, no SSH. Just code + triggers.

---

## 7. Cost Example

A Lambda function that:
- Runs 1 million times/month
- Takes 200ms each time
- Uses 128 MB memory

**Cost: $0.00/month** (free tier covers 1M requests + 400,000 GB-seconds)

Compare to an EC2 t2.micro running 24/7: ~$8.50/month.

Lambda is dramatically cheaper for sporadic workloads.

---

## 🔨 Your Turn

1. Create a Lambda function that receives an event with your name and returns "Hello, {name}!"
2. Add an S3 trigger to a bucket — the Lambda should log the object key whenever a file is uploaded
3. (Advanced) Build a fully serverless URL shortener: API Gateway + Lambda + DynamoDB. The Lambda receives a URL, stores it in DynamoDB with a short code, and returns the short URL.
4. Check CloudWatch Logs to see your Lambda's `print()` output

**Continue to [Lesson 06: ECS: Running Apps at Scale on AWS](06-aws-ecs.md)**
