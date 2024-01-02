#vless
def edit(link, set_uuid=None, set_sni=None, set_tag=None):
  link = link.split('://')[1]
  uuid = link.split('@')[0]
  ip, port = link.split('@')[1].split('?')[0].split(':')
  if port == 443:
    sni, tag = link.split('sni=')[1].split('#')
  else:
    sni = link.split('host=')[1].split('&')[0]
    tag = link.split('#')[1]
  key = { f'{ip}:{port}' : uuid }
  if ip in ['127.0.0.1', '1.1.1.1', '0.0.0.0', '8.8.8.8']:
    return
  if set_uuid:
    link = link.replace(uuid, set_uuid)
  if set_sni:
    link = link.replace(sni, set_sni)
  if set_tag:
    link = link.replace(tag, set_tag)
  full_link = f"vless://{link}"
  return full_link, key
  