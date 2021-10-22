import testinfra.utils.ansible_runner
import os


testinfra_hosts = testinfra.utils.ansible_runner.AnsibleRunner(
    os.environ['MOLECULE_INVENTORY_FILE']).get_hosts('all')

# Verificação do docker runtime

def test_if_container_is_executing(host):
    
    cmd = host.run("docker container run -d --name molecule_nginx nginx")

    assert cmd.rc == 0

def test_if_container_is_running(host):
    
    container = host.docker('molecule_nginx')

    assert container.is_running

    host.run("docker container rm -f molecule_nginx")

# Testando versões do docker e containerd

def test_docker_containerd_version(host):
    
    runtimes = {
        'docker-ce': '5:20.10', 
        'docker-ce-cli': '5:20.10',
        'containerd.io': '1.4.9'
    }

    for packages, version in runtimes.items():

        container = host.package(packages)

        assert container.is_installed
        assert container.version.startswith(version)

# Verificação do arquivo do docker daemon.json

def test_hosts_file(host):
    
  file = '/etc/docker/daemon.json'
  f = host.file(file)
        
  assert f.exists

# Testando as configurações de bridge para Nomad e RKE

def test_bridge_config(host):

    path = '/etc/sysctl.d/20-net-bridge.conf'
    bridge = ['net.bridge.bridge-nf-call-arptables','net.bridge.bridge-nf-call-ip6tables','net.bridge.bridge-nf-call-iptables']
    f = host.file(path)

    assert f.exists

    for name in bridge:
        
        assert f.contains(name)



