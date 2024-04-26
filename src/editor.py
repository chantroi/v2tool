import concurrent.futures

from protocols import trojan, vless, vmess


def editor(
    batch: list, values: set, uuid: str = None, sni: str = None, tag: str = None
):
    for link in batch:
        if link.startswith("vmess"):
            link = vmess.edit(link, uuid, sni, tag)
        elif link.startswith("trojan"):
            link = trojan.edit(link, uuid, sni, tag)
        elif link.startswith("vless"):
            link = vless.edit(link, uuid, sni, tag)
        if link:
            values.add(link)


def processes(links: list, uuid: str = None, sni: str = None, tag: str = None):
    batch_size = 10
    values = set()

    def process_batch(batch):
        try:
            editor(batch, values, uuid, sni, tag)
        except Exception as e:
            print(e)
            pass

    with concurrent.futures.ThreadPoolExecutor() as executor:
        executor.map(
            process_batch,
            (links[i : i + batch_size] for i in range(0, len(links), batch_size)),
        )
    return list(values)