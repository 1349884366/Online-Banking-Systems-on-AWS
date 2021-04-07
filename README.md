# Online-Banking-Systems-on-AWS

## Part 1: Enabling *AWS S3* website hosting

1. Sign in to the AWS Management Console and open the Amazon S3 console at https://console.aws.amazon.com/s3/.
1. In the **Buckets** list, choose the name of the bucket that you want to enable static website hosting for.
1. Choose **Properties**.
1. Under **Static website hosting**, choose **Edit**.
1. Choose **Use this bucket to host a website**.
1. Under **Static website hosting**, choose **Enable**.
1. In **Index document**, enter the file name of the index document, typically index.html.
1. Choose **Save changes**.
1. Under **Static website hosting**, note the **Endpoint**.
The **Endpoint** is the Amazon S3 website endpoint for your bucket. After you finish configuring your bucket as a static website, you can use this endpoint to test your website.


## Part 2: Create and configure the lambda function

1.