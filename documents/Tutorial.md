## Part 1: CREATE DYNAMODB DATABASE.
1. Log into the Amazon [AWS DynamoDB Console](https://console.aws.amazon.com/dynamodb/home).
1. Make sure you **note what region you are creating your function in**. You can see this at the very top of the page, next to your account name.
    ### Create the User Table
    1. Click the **blue** "Create table" button.
    1. Next to "Table name" type in User.
    1. In the "Primary Key" field type in User_ID.
    1. Click the **blue** "Create" button.
    1. **Copy the table's "Amazon Resource Name (ARN)"** from the right hand panel (you will need it later in part 2).
    ### Create the Activities Table
    1. Click the **blue** "Create table" button.
    1. Next to "Table name" type in Activities.
    1. In the "Primary Key" field type in "Activity_ID".
    1. Check the "Add sort key" checkbox and type "Time" in the field.
    1. Uncheck the "Use default settings" checkbox under "Form Settings".
    1. Click the **blue** "+ Add index" under the "Secondary indexes" section.
    1. In the "Primary Key" field type in "User".
    1. Check the "Add sort key" checkbox and type "Time" in the field.
    1. Click the **blue** "Add index" button.
    1. Click the **blue** "Create" button.
    1. **Copy the table's "Amazon Resource Name (ARN)"** from the right hand panel (you will need it later in part 2).
    ### Create the Transactions Table
    1. Click the **blue** "Create table" button.
    1. Next to "Table name" type in Transactions.
    1. In the "Primary Key" field type in "Transaction_ID".
    1. Check the "Add sort key" checkbox and type "Time" in the field.
    1. Uncheck the "Use default settings" checkbox under "Form Settings".
    1. Click the **blue** "+ Add index" under the "Secondary indexes" section.
    1. In the "Primary Key" field type in "Sender".
    1. Check the "Add sort key" checkbox and type "Time" in the field.
    1. Click the **blue** "Add index" button.
    1. Click the **blue** "Create" button.
    1. **Copy the table's "Amazon Resource Name (ARN)"** from the right hand panel (you will need it later in part 2).

## Part 2: BUILD SERVERLESS FUNCTION

1. In a new browser tab, log into the [AWS Lambda Console](https://console.aws.amazon.com/lambda/).
1. Make sure you **note what region you are creating your function in**. You can see this at the very top of the page, next to your account name.
1. Click on the **orange** "Create Function" button.
1. Under "Function Name" type in eBankFunction.
1. Select **Python 3.8** from the **runtime** drop-down.
1. Click on the **orange** "Create Function" button.
1. Open the **Upload from** drop-down menu.
1. Click **.zip file** button.
1. Click the **Upload** button, and then select "back-end.zip" to upload.
1. Click on the **"Permissions" tab**.
1. In the "Execution role" box **click on the role**. A new browser tab will open.
1. Click on "Add inline policy" on the right of the "Permissions policies" box.
1. Click on the "JSON" tab.
1. Paste the following policy in the text area, **taking care to replace your table's ARN(From part 1) in the "Resource" field on line 16,17,18**:
    ```json
    {
    "Version": "2012-10-17",
    "Statement": [
        {
            "Sid": "VisualEditor0",
            "Effect": "Allow",
            "Action": [
                "dynamodb:PutItem",
                "dynamodb:DeleteItem",
                "dynamodb:GetItem",
                "dynamodb:Scan",
                "dynamodb:Query",
                "dynamodb:UpdateItem"
            ],
            "Resource": [
                "YOUR-User-TABLE-ARN",
                "YOUR-User-TABLE-ARN/index/*",
                "YOUR-Transactions-TABLE-ARN",
                "YOUR-Transactions-TABLE-ARN/index/*",
                "YOUR-Activities-TABLE-ARN",
                "YOUR-Activities-TABLE-ARN/index/*"
            ]
        }
    ]
    }
    ```
1. Click the **blue** "Review Policy" button.
1. Next to "name" type in eBankDynamoPolicy.
1. Click the **blue** "Create Policy" button.

## Part 3: LINK SERVERLESS FUNCTION TO WEB APP
1. Log into the [AWS API Gateway Console](https://console.aws.amazon.com/apigateway/main/).
2. Click the **orange** "Create API" button.
3. Find the REST API box and click the **orange** "Build" button in it.
4. Under "Choose the protocol," select **REST**.
5. Under "Create new API," select **New API**.
6. In the "API name" field type in eBankAPI.
7. Select **"Edge optimized"** in the "Endpoint Type" drop-down
8. Click the **blue** "Create API" button. 
1. In the left nav, click on **"Resources"** under your eBank API.
1. With the "/" resource selected, click **"Create Method"** from the Action drop-down menu.
1. Select **POST** from the new drop-down that appears, then click on the checkmark.
1. Select **Lambda Function** for the integration type.
1. Type in eBankFunction into the "Function" field.
1. Click the **blue** "Save" button.
1. You should see a message letting you know you are giving the API you are creating permission to call your Lambda function. Click the **"OK"** button.
1. With the newly created POST method selected, select **"Enable CORS"** from the Action drop-down menu.
1. Leave the POST checkbox selected and click the blue **"Enable CORS and replace existing CORS headers"** button.
1. You should see a message asking you to confirm method changes. Click the blue **"Yes, replace existing values"** button.
1. In the **"Actions"** drop-down list select **"Deploy API."**
1. Select **"[New Stage]"** in the **"Deployment stage"** drop-down list.
1. Enter dev for the **"Stage Name."**
1. Choose **"Deploy."**
1. **Copy and save** the URL next to "Invoke URL" (you will need it in part 4).

## Part 4: CREATE WEB APP

1. Open the **script.js** file under the **fronted-end** directory.
1. **Replace the API Invoke URL on Line 2(From part 3)**
1. Save the file.
1. Log into the Amazon [AWS S3 Console](https://console.aws.amazon.com/s3/).
1. Choose **Create bucket**.
The Create bucket wizard opens.
1. In **Bucket name**, enter a DNS-compliant name for your bucket.
1. In **Region**, choose the AWS Region where you want the bucket to reside.
1. Choose **Create bucket**.
1. In the **Buckets** list, choose the name of the bucket that you just created.
1. Upload all files under the **fronted end** directory to this bucket.
1. Choose **Properties**.
1. Under **Static website hosting**, choose **Edit**.
1. Choose **Use this bucket to host a website**.
1. Under **Static website hosting**, choose **Enable**.
1. In **Index document**, enter **main.html**.
1. Choose **Save changes**.
1. Under **Static website hosting**, note the **Endpoint**.
The **Endpoint** is the Amazon S3 website endpoint for your bucket. After you finish configuring your bucket as a static website, you can use this endpoint to test your website.