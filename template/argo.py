import requests
import sys
from jinja2 import Template


argotoken = sys.argv[1]
headers = {'Authorization': 'Bearer ' + argotoken }
url = "http://argo.mgmt.stg.naemo.io/api/v1/applications"

res = requests.get(url, headers=headers).json()
items = res["items"]

for item in items:

    name = item["metadata"]["name"]
    repo = item["spec"]["source"]["repoURL"]
    targetRevision = item["spec"]["source"]["targetRevision"]
    namespace = item["status"]["sync"]['comparedTo']['destination']['namespace']
    project = item["spec"]["project"]
    server = ""

    if name == "fe-systemadmin":
        destination = item["status"]["sync"]['comparedTo']['destination']['server']
        server = destination
    else:
        destination = item["status"]["sync"]['comparedTo']['destination']['name']
        if destination == "eks-an2-stg-naemo-wallet":
            server = "https://F0FD857663A5804DA13E426623D8E405.yl4.ap-northeast-2.eks.amazonaws.com"
        else:
            server = "https://E1590B0C4B7CF0087E8224BE91AFDECA.gr7.us-east-2.eks.amazonaws.com"

    with open('./template.yml', 'r') as f:
        template_data = f.read()

        # 템플릿 객체 생성
        template = Template(template_data)

        # 템플릿 렌더링
        rendered_template = template.render(name=name, repo=repo, targetRevision=targetRevision, namespace=namespace, project=project, server=server)

        # 렌더링된 템플릿을 파일에 쓰기
        with open(f'../stg/{name}.yml', 'w') as f:
            f.write(rendered_template)
