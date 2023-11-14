# Badminton Automation Script

## Overview
This project contains a Python script for automating web interactions related to badminton activities, such as booking courts or registering for events. It's designed to run on AWS Lambda, triggered by AWS EventBridge, and uses Selenium for web automation. Sensitive information like passwords is securely managed through environment variables.

**Note:** This project is currently not open for public use. It's a private automation tool tailored for specific tasks and environments.

## Features
- **Automated Web Interactions:** Automates tasks on badminton websites using Selenium.
- **AWS Lambda Deployment:** Deployed on AWS Lambda for serverless execution.
- **Event-Driven Trigger:** Scheduled and triggered using AWS EventBridge.
- **Secure Credential Management:** Credentials are managed securely using AWS Lambda environment variables.

## Prerequisites
- AWS Account
- Python 3.x
- Selenium WebDriver
  
## AWS Lambda Deployment
- **Package the Script:**
Prepare a zip package for Lambda deployment.
- **Create a Lambda Function:**
Use AWS Lambda console to create and configure the function.
Upload the zipped package.
- **Set Environment Variables:**
Configure environment variables in Lambda settings.
- **Configure EventBridge:**
Set up an EventBridge rule for triggering the Lambda function.
- **Usage**
The script runs automatically based on the EventBridge schedule, performing automated tasks on the specified badminton website.
- **Security**
Credentials are not stored in the script but are set as environment variables in AWS Lambda.
- **Contributing**
This project is not currently open for public contribution.
