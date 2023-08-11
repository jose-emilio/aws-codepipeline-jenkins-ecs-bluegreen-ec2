import boto3
import cfnresponse
import os

datos = {}

client = boto3.client('s3',os.environ['Region'])
resource = boto3.resource('s3',os.environ['Region'])

def lambda_handler(event, context):
    try:
        mibucket=event['ResourceProperties']['NombreBucket']
        if event['RequestType'] == 'Create':
            response = client.create_bucket(
                ACL='private',
                Bucket=mibucket
            )
            datos['NombreBucket'] = mibucket
            datos['Arn'] = 'arn:aws:s3:::'+mibucket
        elif event['RequestType'] == 'Delete':
            bucket = resource.Bucket(mibucket)
            bucket.objects.all().delete()
            response = client.delete_bucket(
                Bucket=mibucket
            )
        cfnresponse.send(event, context, cfnresponse.SUCCESS, datos, mibucket)
        
    except Exception as e:
        datos['Error'] = str(e)
        cfnresponse.send(event, context, cfnresponse.FAILED, datos)
