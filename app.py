from flask import Flask, render_template, request, send_file
import os
import signal
import subprocess
import sys
import zipfile
import io
from playbook_builder.generator import build_playbook

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'generated'
VERSION = "1.3.1"

def libera_porta(porta=5000):
    try:
        output = subprocess.check_output(f"lsof -ti tcp:{porta}", shell=True).decode().strip()
        if output:
            for pid in output.split('\n'):
                os.kill(int(pid), signal.SIGKILL)
            print(f"Porta {porta} liberata")
    except subprocess.CalledProcessError:
        pass

@app.route('/', methods=['GET', 'POST'])
def index():
    vagrantfile_preview = None
    playbook_content = None

    if request.method == 'POST':
        vm_name = request.form['vm_name'].strip() or "default-vm"
        box = request.form['box']
        use_dhcp = 'use_dhcp' in request.form
        ip = request.form['ip'].strip() if not use_dhcp else None
        if not use_dhcp and not ip:
            ip = "192.168.56.10"
        port = request.form['port'].strip() or "2222"
        cpu = request.form.get('cpu', '').strip() or "2"
        ram = request.form.get('ram', '').strip() or "2048"
        provision_shell = 'provision' in request.form

        tools = [tool for tool in request.form.getlist("tools") if tool != "terraform"]  # <-- Terraform escluso

        vm_folder = os.path.join(app.config['UPLOAD_FOLDER'], vm_name)
        os.makedirs(vm_folder, exist_ok=True)

        playbook_filename = None
        if tools:
            playbook_content_raw = build_playbook(tools, "apt")
            playbook_filename = "playbook.yml"
            playbook_full_path = os.path.join(vm_folder, playbook_filename)
            with open(playbook_full_path, 'w') as f:
                f.write(playbook_content_raw)
            playbook_content = playbook_content_raw

        shell_script = ''
        if provision_shell:
            shell_script = """  config.vm.provision \"shell\", inline: <<-SHELL
    sudo apt update && sudo apt upgrade -y
  SHELL

"""

        network_config = '  config.vm.network "private_network", type: "dhcp"\n' if use_dhcp else f'  config.vm.network "private_network", ip: "{ip}"\n'

        ansible_script = ''
        if playbook_filename:
            ansible_script = f"""  config.vm.provision \"ansible\" do |ansible|
    ansible.playbook = "{playbook_filename}"
    ansible.compatibility_mode = "2.0"
  end

"""

        vagrantfile_content = f"""Vagrant.configure("2") do |config|
  config.vm.box = "{box}"
  config.vm.hostname = "{vm_name}"
{network_config}  config.vm.network "forwarded_port", guest: 22, host: {port}
  config.vm.provider "virtualbox" do |vb|
    vb.memory = "{ram}"
    vb.cpus = {cpu}
  end

{shell_script}{ansible_script}end
"""

        vagrantfile_path = os.path.join(vm_folder, f"{vm_name}_Vagrantfile")
        with open(vagrantfile_path, 'w') as f:
            f.write(vagrantfile_content)

        vagrantfile_preview = {
            "name": vm_name,
            "content": vagrantfile_content,
            "path": os.path.join(vm_name, f"{vm_name}_Vagrantfile")
        }

    return render_template('index.html', vagrantfile=vagrantfile_preview, playbook_content=playbook_content, version=VERSION)

@app.route('/download/<vm_name>/<filename>')
def download(vm_name, filename):
    path = os.path.join('generated', vm_name, filename)
    return send_file(path, as_attachment=True) if os.path.exists(path) else ("File non trovato", 404)

@app.route('/download_zip/<vm_name>')
def download_zip(vm_name):
    folder_path = os.path.join('generated', vm_name)
    if not os.path.isdir(folder_path):
        return "Cartella non trovata", 404

    buffer = io.BytesIO()
    with zipfile.ZipFile(buffer, 'w') as z:
        for file_name in os.listdir(folder_path):
            file_path = os.path.join(folder_path, file_name)
            arcname = "Vagrantfile" if file_name.endswith("_Vagrantfile") else file_name
            z.write(file_path, arcname=arcname)

        script_path = os.path.join(os.getcwd(), 'script.sh')
        if os.path.exists(script_path):
            z.write(script_path, arcname='script.sh')

    buffer.seek(0)
    return send_file(buffer, as_attachment=True, download_name=f"{vm_name}.zip", mimetype='application/zip')

if __name__ == '__main__':
    try:
        port = int(os.environ.get("PORT", 5000))
        app.run(debug=True, host="0.0.0.0", port=port, use_reloader=False)
    except KeyboardInterrupt:
        libera_porta(port)
        sys.exit(0)
