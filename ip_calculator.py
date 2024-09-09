import ipaddress

def netmask_to_cidr(netmask):
    """將網絡掩碼轉換為 CIDR"""
    try:
        return sum([bin(int(x)).count('1') for x in netmask.split('.')])
    except ValueError:
        raise ValueError("無效的網絡掩碼")

def cidr_to_netmask(cidr):
    """將 CIDR 轉換為網絡掩碼"""
    try:
        cidr = int(cidr)
        mask = (0xffffffff >> (32 - cidr)) << (32 - cidr)
        return f"{(mask >> 24) & 255}.{(mask >> 16) & 255}.{(mask >> 8) & 255}.{mask & 255}"
    except ValueError:
        raise ValueError("無效的 CIDR")

def calculate_ip_info(input_value):
    """根據用戶的輸入（IP + 掩碼），計算網段相關信息"""
    if '/' in input_value:
        ip, mask_value = input_value.split('/')
        if '.' in mask_value:
            cidr = netmask_to_cidr(mask_value)
            network = ipaddress.ip_network(f"{ip}/{cidr}", strict=False)
        else:
            network = ipaddress.ip_network(f"{ip}/{mask_value}", strict=False)
    else:
        raise ValueError("輸入格式錯誤，請使用 CIDR 或網絡掩碼格式")

    network_address = network.network_address
    broadcast_address = network.broadcast_address
    total_ips = network.num_addresses
    usable_ips = total_ips - 2 if total_ips > 2 else 0
    first_usable_ip = network[1] if usable_ips > 0 else 'N/A'
    last_usable_ip = network[-2] if usable_ips > 0 else 'N/A'

    result = (f"網段: {network_address}\n"
              f"廣播地址: {broadcast_address}\n"
              f"總 IP 數: {total_ips}\n"
              f"可用 IP 數: {usable_ips}\n"
              f"第一個可用 IP: {first_usable_ip}\n"
              f"最後一個可用 IP: {last_usable_ip}")
    return result

