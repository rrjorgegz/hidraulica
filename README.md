# hidraulica
Odoo para hidraulica VC 
## instalar en proxmox
1 - Create CT de la plantilla ubuntu-20.04-standard_20.04-1_amd64.tar.gz
2 - user root y poner la pass 
3 - apt update
4 - apt upgrade
5 - crear usuario odoo (adduser odoo) y añadir a grupo sudo (usermod -aG sudo odoo)
6 - (apt install wireguard resolvconf) y copiar para /etc/wireguard/ la configuracion de wg0.conf que se obtiene de descargar de tu cuenta protonvpn.com 
7 - habilitar vpn (wg-quick up wg0) y desabilitar (wg-quick down wg0) para activar de forma permanente luego de habilitar vpn ponemos (systemct enable wg-quick) y desabilitar (systemct disable wg-quick),
8 - instalar docker https://docs.docker.com/engine/install/ubuntu/ , apt install ca-certificates curl, install -m 0755 -d /etc/apt/keyrings, curl -fsSL https://download.docker.com/linux/ubuntu/gpg -o /etc/apt/keyrings/docker.asc, chmod a+r /etc/apt/keyrings/docker.asc, echo "deb [arch=$(dpkg --print-architecture) signed-by=/etc/apt/keyrings/docker.asc] https://download.docker.com/linux/ubuntu $(. /etc/os-release && echo "${UBUNTU_CODENAME:-$VERSION_CODENAME}") stable" | sudo tee /etc/apt/sources.list.d/docker.list > /dev/null, apt update, apt install docker-ce docker-ce-cli containerd.io docker-buildx-plugin docker-compose-plugin
9 - añadir a grupo docker (usermod -aG docker odoo)
10 - descargar repositorio en /home/odoo (git clone https://github.com/rrjorgegz/hidraulica.git)

## Desplegar 
docker compose -f 'docker-compose.yml' up -d --build
