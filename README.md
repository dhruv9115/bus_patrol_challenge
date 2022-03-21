# Bus Patrol Challenge

# Docker

To run the docker image:
```
docker build -t bpchallenge:0.0.1 .
docker run -p 80:80 -e AWS_ACCESS_KEY_ID=<AWS_ACCESS_KEY_ID> -e AWS_SECRET_ACCESS_KEY=<AWS_SECRET_ACCESS_KEY> bpchallenge:0.0.1
```
Open in your web browser
```
localhost
```

To create a bucket
```
localhost/create_bucket/<bucket_name>
```
This will create an s3 bucket in your aws account in us-east-1 region

# CDK

To deploy this application to aws
To test the stack
```
cdk synth
```

To deploy
```
cdk deploy
```

This will deploy and trigger the cdk pipeline
![screencapture-us-east-1-console-aws-amazon-codesuite-codepipeline-pipelines-PipelineStack-Pipeline9850B417-YO01I94C49UT-view-2022-03-21-16_00_15](https://user-images.githubusercontent.com/56513566/159354293-9d3a0f1a-e871-4839-9374-df9ea30a4b4d.png)

Once the pipeline execution is completed and the app is deployed,
Copy the Load Balancer DNS and paste it on your browser

Run <URL>/create_bucket/<BUCKET_NAME> to create the s3 bucket
  
# IMPORTANT NOTE
  
  As this project uses connection arn to connect to github repo, using cdk deploy won't work, 
  However you can deploy the ```bus_patrol_challenge_stack``` directly without the pipeline
