import network
import _thread
import machine
import time
import socket

SSID = 'esp32_webserver'
PASSWORD = 'esp32123'
LED_PIN = 2
HTML_FILE = 'index.html'
ALAMAT_WEB_SERVER = '192.168.4.1'

led = machine.Pin(LED_PIN, machine.Pin.OUT)
wlanAp = network.WLAN(network.AP_IF)
wlanwifi = network.WLAN(network.STA_IF)

def log_info(pesan):
    print(f"[INFO] {pesan}")

def log_error(pesan):
    print(f"[ERROR] {pesan}")

def led_on():
    log_info("LED menyala!")
    led.value(1)

def led_off():
    log_info("LED mati!")
    led.value(0)

def led_blink():
    while True:
        led.value(1)
        time.sleep(0.2)
        led.value(0)
        time.sleep(0.2)

def led_program_kedip():
    _thread.start_new_thread(led_blink, ())

def wifiAp_on():
    try:
        led_off()
        led_program_kedip()
        wlanAp.active(True)
        log_info("Akses poin menyala")
        wlanAp.config(essid=SSID, password=PASSWORD)
    except Exception as e:
        log_error(f"Kesalahan: {e}")

def wifiAp_off():
    try:
        wlanAp.active(False)
        log_info("Mematikan akses point")
        led_off()
    except Exception as e:
        log_error(f"Kesalahan: {e}")

def wifi_on():
    try:
        if not wlanwifi.isconnected():
            wlanwifi.active(True)
            log_info("WiFi menyala!")
            led_on()
        else:
            log_info("WiFi sudah menyala!")
    except Exception as e:
        log_error(f"Kesalahan: {e}")

def wifi_off():
    try:
        if wlanwifi.isconnected():
            wlanwifi.active(False)
            log_info("WiFi mati!")
            led_off()
        else:
            log_info("WiFi sudah mati!")
    except Exception as e:
        log_error(f"Kesalahan: {e}")

def hubungkan_wifi(ssid, password):
    try:
        wlanwifi.connect(ssid, password)
        log_info("Terhubung ke WiFi!")
        led_on()
    except Exception as e:
        log_error(f"Kesalahan: {e}")
        led_off()

def cari_wifi():
    try:
        led_off()
        led_blink()
        log_info("Mencari jaringan WiFi...")
        wlanwifi.active(True)
        wifi_list = wlanwifi.scan()
        return wifi_list
    except Exception as e:
        log_error(f"Kesalahan: {e}")
        return []

def web_server():
    try:
        led_off()
        led_program_kedip()
        log_info(f"Web server aktif di {ALAMAT_WEB_SERVER}")
        s = socket.socket()
        s.bind((ALAMAT_WEB_SERVER, 80))
        s.listen(5)
        while True:
            conn, addr = s.accept()
            request = conn.recv(1024).decode()
            log_info(f"Request: {request}")
            perintah = request.split()[1]
            if perintah == "/cari_wifi":
                wifi_list = cari_wifi()
                respons = f"Jaringan WiFi yang tersedia:\n{wifi_list}"
                conn.sendall(f"HTTP/1.1 200 OK\n\n{respons}".encode())
            elif perintah == "/wifi_on":
                wifi_on()
                conn.sendall(f"HTTP/1.1 200 OK\n\nWiFi menyala!".encode())
            elif perintah == "/hubungkan_wifi":
            	hubungkan_wifi(,password=)
            	conn.sendall(f"HTTP/1.1 200 OK\n\nmenyambungkan ke jaringan WIFI".encode())
            elif perintah == "/wifi_off":
                wifi_off()
                conn.sendall(f"HTTP/1.1 200 OK\n\nWiFi mati!".encode())
            else:
                try:
                    conn.sendall(open(HTML_FILE, 'r').read().encode())
                except FileNotFoundError:
                    conn.sendall("File tidak ditemukan".encode())
                except Exception as e:
                    conn.sendall("Kesalahan membaca file".encode())
            conn.close()
    except Exception as e:
        log_error(f"Kesalahan: {e}")

def main():
    log_info("Program ESP32 Web Server")
    log_info("Silahkan sambungkan ke WiFi:")
    log_info(f"SSID: {SSID}")
    log_info(f"Password: {PASSWORD}")
    wifiAp_on()
    web_server()
    
if __name__=="__main__":
	main()