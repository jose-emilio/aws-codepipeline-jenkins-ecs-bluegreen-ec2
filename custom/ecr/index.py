import boto3
import cfnresponse

response_data = {}

client = boto3.client('ecr')

def lambda_handler(event, context):
    try:
        repo=event['ResourceProperties']['RepoECR']
        if event['RequestType'] == 'Create':
            response = client.create_repository(
                repositoryName=repo.lower(),
                imageScanningConfiguration={
                'scanOnPush': True
                },
                encryptionConfiguration={
                'encryptionType': 'AES256'
                }
            )
            response_data['Uri'] = response['repository']['repositoryUri']
            response_data['Nombre'] = response['repository']['repositoryName']
        elif event['RequestType'] == 'Delete':
            client.delete_repository(
                repositoryName=repo.lower(),
                force=True
            )
        
        cfnresponse.send(event, context, cfnresponse.SUCCESS, response_data,repo.lower())
        
    except Exception as e:
        response_data['Error'] = str(e)
        cfnresponse.send(event, context, cfnresponse.FAILED, response_data)