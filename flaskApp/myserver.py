from flask import Flask, request, jsonify
from sagemaker_utility import build_model, deploy_endpoints
import mlflow
app = Flask(__name__)

region = 'eu-west-1'
execution_role_arn = 'arn:aws:iam::438478214470:role/service-role/AmazonSageMaker-ExecutionRole-20200324T112499'


@app.route('/build', methods=['GET'])
def build():
    s3_path = request.args.get('s3_path', '')
    repo_name = request.args.get('repo_name', '')
    result = build_model(s3_path, repo_name)
    if not result:
        return jsonify({'error': 'Error in building Model Image'}, 500)

    return jsonify({'image_uri':result})

@app.route('/deploy', methods=['POST'])
def deploy():
    data = request.get_json(force=True)
    image_uri = data.get('image_uri', '')
    app_name = data.get('app_name', '')
    model_path = data.get('model_path', '')

    try:
        print('ok')
        #mlflow.sagemaker.deploy(app_name, model_path, execution_role_arn, image_url=image_uri, region_name=region)
    except Exception as e:
        print(e)
        return jsonify({'error': 'Error in building Model Image'}, 500)

        return jsonify({'status': 'success'})


if __name__ == '__main__':
    app.run(debug=True, port=4000, host='0.0.0.0')