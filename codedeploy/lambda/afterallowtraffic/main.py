import json
import urllib3
import os
import boto3

cd = boto3.client('codedeploy')

def lambda_handler(event, context):
    idDep = event["DeploymentId"]
    idHook = event["LifecycleEventHookExecutionId"]
    http = urllib3.PoolManager()
    url = os.environ["urlprod"]
    resultado = 'Succeeded'
    test = 1
    while test < 10 and resultado == 'Succeeded':
        print('Iniciando solicitudes a la URL: '+url)
        r = http.request('GET', url)
        if r.status != 200:
            resultado = 'Failed'
        print('Repuesta con codigo: '+str(r.status))
        print('Payload: ')
        print(r.data)
        test += 1
    response = cd.put_lifecycle_event_hook_execution_status(
        deploymentId=idDep,
        lifecycleEventHookExecutionId=idHook,
        status=resultado
    )
    return response
