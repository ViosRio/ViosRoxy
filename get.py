import os
import sys
import time
import requests
from colorama import Fore, Style, init
import pyfiglet

# API KEY'İNİ BURAYA YAPIŞTIR
# https://www.webshare.io 
WEBSHARE_API_KEY = "npjct2zpnd5sgdhqpbw07f1yqch1tiv7qdpgm507"

init(autoreset=True)

def clear_screen():
    os.system("cls" if os.name == "nt" else "clear")

def show_banner():
    clear_screen()
    banner = pyfiglet.figlet_format("VIP PROXY", font="slant")
    print(f"{Fore.CYAN}{banner}")
    print(f"{Fore.YELLOW}➖➖➖➖➖➖➖➖➖➖➖➖➖➖➖➖➖")
    print(f"{Fore.GREEN}  ✨ Powered by DeepSeek & Vios Team")
    print(f"{Fore.YELLOW}➖➖➖➖➖➖➖➖➖➖➖➖➖➖➖➖➖{Style.RESET_ALL}\n")

def show_menu():
    print(f"{Fore.MAGENTA}[1] {Fore.YELLOW}Otomatik Proxy Seç & Bağlan")
    print(f"{Fore.MAGENTA}[2] {Fore.YELLOW}Manuel Proxy Gir")
    print(f"{Fore.MAGENTA}[3] {Fore.YELLOW}Çıkış")
    choice = input(f"\n{Fore.GREEN}>>> Seçiminiz (1-3): ")
    return choice

def get_proxies_from_webshare():
    try:
        response = requests.get(
            f"https://proxy.webshare.io/api/proxy/list/",
            headers={"Authorization": f"Token {WEBSHARE_API_KEY}"}
        )
        proxies = []
        for proxy in response.json()["results"]:
            proxy_str = f"http://{proxy['username']}:{proxy['password']}@{proxy['proxy_address']}:{proxy['ports']['http']}"
            proxies.append(proxy_str)
        return proxies
    except Exception as e:
        print(f"{Fore.RED}❌ Webshare API hatası: {e}")
        return []

def test_proxy_with_ping(proxy):
    try:
        start_time = time.time()
        response = requests.get(
            "https://api.ipify.org?format=json",
            proxies={"http": proxy, "https": proxy},
            timeout=10
        )
        ping_ms = int((time.time() - start_time) * 1000)
        print(f"\n{Fore.GREEN}✅ BAŞARILI! {Fore.YELLOW}IP: {response.json()['ip']} | Ping: {ping_ms}ms")
        return True, ping_ms
    except Exception as e:
        print(f"\n{Fore.RED}❌ HATA: {e}")
        return False, 0

def run_proxy(proxy, ping_ms):
    print(f"\n{Fore.GREEN}🔥 Proxy Aktif! (Ping: {ping_ms}ms) | Çıkmak için CTRL+C")
    try:
        while True:
            time.sleep(3)
            # Her 3 saniyede bir ping güncelle
            _, new_ping = test_proxy_with_ping(proxy)
            print(f"{Fore.CYAN}🔄 Bağlantı kontrolü | Ping: {new_ping}ms")
    except KeyboardInterrupt:
        print(f"\n{Fore.RED}⛔ Proxy sonlandırıldı.")

def auto_select_proxy():
    print(f"\n{Fore.CYAN}🔹 Webshare'den proxy listesi alınıyor...")
    proxies = get_proxies_from_webshare()
    if not proxies:
        print(f"{Fore.RED}❌ Proxy bulunamadı! API key veya internet bağlantını kontrol et.")
        return None
    
    print(f"{Fore.GREEN}✔ {len(proxies)} proxy bulundu. En hızlısı seçiliyor...")
    
    best_proxy = None
    best_ping = 9999
    
    for proxy in proxies:
        print(f"{Fore.YELLOW}⚡ Test ediliyor: {proxy[:50]}...")
        success, ping = test_proxy_with_ping(proxy)
        if success and ping < best_ping:
            best_proxy = proxy
            best_ping = ping
    
    return best_proxy, best_ping

def main():
    while True:
        show_banner()
        choice = show_menu()

        if choice == "1":
            proxy, ping = auto_select_proxy()
            if proxy:
                run_proxy(proxy, ping)
            else:
                print(f"{Fore.RED}\n❌ Çalışan proxy bulunamadı!")
                time.sleep(2)

        elif choice == "2":
            proxy = input(f"\n{Fore.YELLOW}🔹 Proxy adresini gir (http://user:pass@ip:port): ")
            success, ping = test_proxy_with_ping(proxy)
            if success:
                run_proxy(proxy, ping)
            else:
                print(f"{Fore.RED}\n❌ Proxy bağlantısı başarısız!")
                time.sleep(2)

        elif choice == "3":
            print(f"\n{Fore.RED}🚪 Çıkış yapılıyor...")
            time.sleep(1)
            sys.exit()

        else:
            print(f"{Fore.RED}\n⚠ Geçersiz seçim! 1-3 arası bir sayı gir.")
            time.sleep(1)

if __name__ == "__main__":
    main()
