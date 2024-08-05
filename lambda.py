import json
import boto3

bedrock_runtime_client = boto3.client(service_name='bedrock-runtime')

def lambda_handler(event, context):
    user_prompt = event["key1"]
    model_id = 'anthropic.claude-3-5-sonnet-20240620-v1:0'
    system_prompt = "あなたは生成AIのエージェントです。ユーザからの質問に丁寧に回答してください。ユーザは自分が食べたものを入力して、食事を管理しようとしています。あなたの出力としては、まず初めに「朝食、昼食、夕食、間食」のどれかの文字を「」で括った状態で回答しつつ、その後「食品名、1人あたりのカロリー、1人あたりのPFCのそれぞれのグラム数」を1行ずつ出力してください。もしそれぞれの値を推定することが難しい場合はある程度推測しつつ、先述の出力を行い、その後推定した前提を最後に記載してください。前提を記述する際は「この推定値は」という文言から始めてください。"
    max_tokens = 1000
    temperature = 0

    user_message = {
        "role": "user",
        "content": user_prompt      
    }
    body = json.dumps(
        {
        "anthropic_version": "bedrock-2023-05-31",
        "max_tokens": max_tokens,
        "system": system_prompt,
        "messages": [user_message],
        "temperature": temperature
        }  
    )  

    response = bedrock_runtime_client.invoke_model(body=body, modelId=model_id)
    response_json = json.loads(response.get('body').read())
    
    return response_json['content'][0]['text']
