import boto3
import cfnresponse

datos = {}

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
            datos['Uri'] = response['repository']['repositoryUri']
            datos['Nombre'] = response['repository']['repositoryName']
        elif event['RequestType'] == 'Delete':
            client.delete_repository(
                repositoryName=repo.lower(),
                force=True
            )
        
        cfnresponse.send(event, context, cfnresponse.SUCCESS, datos,repo.lower())
        
    except Exception as e:
        datos['Error'] = str(e)
        cfnresponse.send(event, context, cfnresponse.FAILED, datos)