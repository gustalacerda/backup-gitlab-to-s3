import gitlab
import os
import gitlab
import os
import zipfile
import boto3

# Configurações do GitLab
gitlab_url = "<insert>"  # Altere para o URL do seu GitLab
private_token = "<insert>"  # Substitua pelo seu token de acesso

# Configurações locais
clone_path = "<insert>"  # Substitua pelo diretório onde deseja clonar os repositórios
zip_dir = "<insert>"  # Diretório para armazenar os arquivos ZIP

# Configurações do S3
aws_access_key_id = "<insert>"
aws_secret_access_key = "<insert>"
s3_bucket_name = "<insert>"

# Pasta local contendo os arquivos que você deseja enviar
local_folder = '<insert>'

# Caminho dentro do bucket onde os arquivos serão armazenados
s3_path = '<insert>'  # Pode ser vazio ou ter uma estrutura de pastas

# Lista de IDs de grupos
group_ids = []  # Substitua pelos IDs dos grupos desejados

# Conectar ao GitLab
gl = gitlab.Gitlab(gitlab_url, private_token=private_token)

# Inicializar o cliente do S3
s3_client = boto3.client('s3', aws_access_key_id=aws_access_key_id, aws_secret_access_key=aws_secret_access_key)

# Função para clonar repositórios de um grupo
def clone_group_repositories(group_id):
    group = gl.groups.get(group_id)
    projects = group.projects.list(all=True)

    for project in projects:
        repo_name = project.name
        repo_url = project.ssh_url_to_repo

        clone_dir = os.path.join(clone_path, repo_name)

        if os.path.exists(clone_dir):
            print(f"O repositório {repo_name} já foi clonado.")
        else:
            print(f"Clonando repositório {repo_name}...")
            os.system(f"git clone {repo_url} {clone_dir}")
            print(f"Repositório {repo_name} clonado com sucesso.")

        # Compactar pasta do repositório
        zip_path = os.path.join(zip_dir, f"{repo_name}.zip")
        create_zip_file(clone_dir, zip_path)
        print(f"Pasta {repo_name} compactada em {zip_path}")

# Função para compactar uma pasta em um arquivo ZIP
def create_zip_file(source, target):
    with zipfile.ZipFile(target, 'w', zipfile.ZIP_DEFLATED) as zipf:
        for root, dirs, files in os.walk(source):
            for file in files:
                file_path = os.path.join(root, file)
                arcname = os.path.relpath(file_path, source)
                zipf.write(file_path, arcname=arcname)

# Clonar e compactar repositórios de todos os grupos da lista
for group_id in group_ids:
    print(f"Clonando e compactando repositórios do grupo ID {group_id}...")
    clone_group_repositories(group_id)
    print(f"Clonagem e compactação de todos os repositórios do grupo ID {group_id} concluída.")

print("Clonagem e compactação de todos os repositórios de grupos concluída.")

# Inicializar o cliente S3
s3_client = boto3.client('s3', aws_access_key_id=aws_access_key_id, aws_secret_access_key=aws_secret_access_key)

# Listar os arquivos na pasta local
for root, dirs, files in os.walk(local_folder):
    for file in files:
        local_file_path = os.path.join(root, file)
        
        # Determinar o nome do arquivo no S3
        relative_path = os.path.relpath(local_file_path, local_folder)
        s3_file_name = os.path.join(s3_path, relative_path)
        
        # Enviar o arquivo para o S3
        s3_client.upload_file(local_file_path, s3_bucket_name, s3_file_name)
        
        print(f'O arquivo {s3_file_name} foi enviado para o bucket {s3_bucket_name}')
