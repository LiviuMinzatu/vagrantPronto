def build_playbook(pacchetti: list, package_type: str = "apt") -> str:
    content = """---
- name: Setup packages
  hosts: all
  become: yes
  tasks:
"""
    pkg_module = "apt"

    if 'docker' in pacchetti:
        content += f"""    - name: Install Docker
      shell: |
        which {pkg_module} && sudo {pkg_module} install -y docker.io || echo 'Package manager not found'

"""

    if 'jenkins' in pacchetti:
        content += """    - name: Install Java (Jenkins dependency)
      apt:
        name: openjdk-11-jdk
        state: present
        update_cache: yes

    - name: Aggiungi chiave Jenkins in modo moderno
      get_url:
        url: https://pkg.jenkins.io/debian/jenkins.io-2023.key
        dest: /usr/share/keyrings/jenkins-keyring.asc
        mode: '0644'

    - name: Aggiungi repository Jenkins
      apt_repository:
        repo: "deb [signed-by=/usr/share/keyrings/jenkins-keyring.asc] https://pkg.jenkins.io/debian binary/"
        state: present
        filename: jenkins

    - name: Install Jenkins
      apt:
        name: jenkins
        state: present
        update_cache: yes

"""

    if 'git' in pacchetti:
        content += f"""    - name: Install Git
      {pkg_module}:
        name: git
        state: present
        update_cache: yes

"""

    if 'helm' in pacchetti:
        content += """    - name: Install Helm
      shell: curl https://raw.githubusercontent.com/helm/helm/main/scripts/get-helm-3 | bash

"""

    if 'kind' in pacchetti:
        content += """    - name: Install Kind
      shell: curl -Lo ./kind https://kind.sigs.k8s.io/dl/latest/kind-linux-amd64 && chmod +x ./kind && mv ./kind /usr/local/bin/kind

"""

    if 'ansible' in pacchetti:
        content += f"""    - name: Install Ansible
      {pkg_module}:
        name: ansible
        state: present
        update_cache: yes

"""

    if 'kubectl' in pacchetti:
        content += """    - name: Install kubectl
      shell: |
        curl -LO "https://dl.k8s.io/release/$(curl -L -s https://dl.k8s.io/release/stable.txt)/bin/linux/amd64/kubectl"
        chmod +x kubectl
        mv kubectl /usr/local/bin/kubectl

"""

    if 'python3' in pacchetti:
        content += f"""    - name: Install Python3 + pip
      {pkg_module}:
        name:
          - python3
          - python3-pip
        state: present
        update_cache: yes

"""

    return content
