import stun

## Servidores stun de los que se obtiene respuesta
stun_servers = ['stun.12connect.com', 'stun.12voip.com', 'stun.aa.net.uk', 'stun.acrobits.cz', 'stun.actionvoip.com', 'stun.aeta-audio.com', 'stun.aeta.com', 'stun.antisip.com', 'stun.cheapvoip.com', 'stun.commpeak.com']

file = open('stuns.txt', 'r')

# for line in file:
#     nat_type, external_ip, external_port = stun.get_ip_info(stun_host=line.strip())
#     print(line, external_ip, external_port)
#     print('\n')



def queryServers():
    for server in stun_servers:
        nat_type, external_ip, external_port = stun.get_ip_info(stun_host=server)
        print('{: <10}'.format(server))

queryServers()