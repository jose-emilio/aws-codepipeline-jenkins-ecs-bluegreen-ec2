import json
import urllib3
import os
import boto3

cd = boto3.client('codedeploy')

def lambda_handler(event, context):
    idDep = event["DeploymentId"]
    idHook = event["LifecycleEventHookExecutionId"]
    http = urllib3.PoolManager()
    url = os.environ["urltest"]
    resultado = 'Failed'
    print('Iniciando solicitud a la URL: '+url)
    r = http.request('GET', url)
    if r.status == 200:
        resultado = 'Succeeded'
    print('Repuesta con codigo: '+str(r.status))
    print('Payload: ')
    print(r.data)
    response = cd.put_lifecycle_event_hook_execution_status(
        deploymentId=idDep,
        lifecycleEventHookExecutionId=idHook,
        status=resultado
    )
    return response
