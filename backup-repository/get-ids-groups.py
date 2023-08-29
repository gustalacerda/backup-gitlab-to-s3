import gitlab

# Configurações do GitLab
gitlab_url = "<insert>"
private_token = "<insert>"

# Conectar ao GitLab
gl = gitlab.Gitlab(gitlab_url, private_token=private_token)

# Obter a lista de todos os grupos
groups = gl.groups.list(all=True)

# Extrair IDs dos grupos
group_ids = [group.id for group in groups]

print("Lista de IDs de grupos:")
print(group_ids)
