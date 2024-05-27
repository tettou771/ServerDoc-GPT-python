import json
import os
from utils.health_check import HealthCheck
from utils.gpt_client import GPTClient
from utils.email_sender import EmailSender

def main():
    # Get the directory where the script is located
    script_dir = os.path.dirname(os.path.abspath(__file__))
    
    # Load config
    config_path = os.path.join(script_dir, 'config.json')
    with open(config_path, 'r') as f:
        config = json.load(f)

    server_name = config['server_name']
    email = config['email']
    smtp_config = config['smtp']
    gpt_model = config['gpt_model']
    openai_api_key = config['openai_api_key']
    prompt = config['prompt']
    commands = config['commands']

    # Execute health checks
    health_check = HealthCheck(commands)
    report = health_check.generate_report()

    # Ask GPT for a detailed report
    gpt_client = GPTClient(api_key=openai_api_key, model=gpt_model)
    gpt_response = gpt_client.generate_report(prompt, report)
    
    print(gpt_response)
    
    # check error
    if gpt_response['error'] != 'noerror' :
        return

    # generate image
    gpt_response['image_url'] = gpt_client.generate_image(gpt_response['dall-e_prompt'])

    print(gpt_response['image_url'])

    # Send the report via email
    email_sender = EmailSender(smtp_config)
    email_sender.send_report(server_name, email, gpt_response['subject'], gpt_response['body'], gpt_response['image_url'], report)

if __name__ == '__main__':
    main()
