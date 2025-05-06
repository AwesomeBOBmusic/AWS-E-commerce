# AWS-E-commerce
Event-Driven Order Notification System, using 

• Amazon SNS for broadcasting notifications 

• Amazon SQS for queuing order events 

• AWS Lambda to process messages 

• Amazon DynamoDB to store order data


Step 1: DynamoDB Setup

1. Go to AWS Console > DynamoDB > Tables
2. Click "Create table"
3. Create a table named "Orders"
4. Partition key: "orderId" (String)
5. Leave all other settings default, click Create table

Step 2: Create SNS Topic

1. Go to SNS > Topics
2. Click “Create topic”
3. Select Standard
4. Name it: OrderTopic
5. Leave default settings, click Create topic

Step 3: Create SQS Queues
A. Create the Dead-Letter Queue

1. Go to SQS > Queues > Create queue
2. Select Standard Queue
3. Name it: OrderQueueDLQ
4. Keep all default settings
5. Click Create queue

B. Create the Main Queue

1. Create another queue named: OrderQueue
2. Scroll down to the Dead-letter queue (DLQ) section
3. Enable it, and select OrderQueueDLQ
4. Set maxReceiveCount = 3
5. Click Create queue

Step 4: Subscribe SQS Queue to SNS Topic
1. Go to SNS > OrderTopic > Subscriptions
2. Click “Create subscription”
3. Set: Protocol: Amazon SQS
4. Endpoint: ARN of OrderQueue
5. Click Create subscription

Step 5: Lambda Function (Python 3.9)

1. Go to AWS Lambda > Functions > Create function
2. Name it: ProcessOrderFunction
3. Set Runtime to Python 3.9
4. Set Handler to index.lambda_handler
5. Architecture x86_64

Step 6: Add the Code to Lambda
1. Add index.py file in code
2. Click Deploy

Step 7: Add Trigger to Lambda
1. Go to Lambda function
2. Click Add trigger
3. Choose SQS
4. Select OrderQueue
5. Click Add

Step 8: Add IAM Roles
1. Go to IAM
2. Click Roles
3. Choose ProcessOrderFunction-role
4. Add DynamoPutItemPolicy
{
	"Version": "2012-10-17",
	"Statement": [
		{
			"Effect": "Allow",
			"Action": "dynamodb:PutItem",
			"Resource": "arn:aws:dynamodb:us-east-1:481665095854:table/Orders"
		}
	]
}
5. Add SQSDeleteMessagePolicy
{
	"Version": "2012-10-17",
	"Statement": [
		{
			"Effect": "Allow",
			"Action": "sqs:DeleteMessage",
			"Resource": "arn:aws:sqs:us-east-1:481665095854:*"
		}
	]
}
6. Add SQSGetQueueAttributesPolicy
{
	"Version": "2012-10-17",
	"Statement": [
		{
			"Effect": "Allow",
			"Action": "sqs:GetQueueAttributes",
			"Resource": "arn:aws:sqs:us-east-1:481665095854:*"
		}
	]
}
7. Add SQSReceiveMessagePolicy
{
	"Version": "2012-10-17",
	"Statement": [
		{
			"Effect": "Allow",
			"Action": "sqs:ReceiveMessage",
			"Resource": "arn:aws:sqs:us-east-1:481665095854:*"
		}
	]
}

Step 9: Test the Full Flow
1. Go to SNS > OrderTopic > Publish message
2. Paste the following JSON into the Message body:
{
  "orderId": "O1234",
  "userId": "U123",
  "itemName": "Laptop",
  "quantity": 1,
  "status": "new",
  "timestamp": "2025-05-03T12:00:00Z"
}
3. Click Publish message

Step 10: ✅ Verify:

Message is in SQS
Lambda gets triggered
Data appears in DynamoDB > Orders table
Logs appear in Lambda > Monitor > View Logs in CloudWatch