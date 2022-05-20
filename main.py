def do_connect():
    global ssid, password
    wlan = network.WLAN(network.STA_IF)
    wlan.active(True)
    if not wlan.isconnected():
        print("Conectando")
        wlan.connect(ssid, password)
        while not wlan.isconnected():
            pass
    print("Config do Wi-Fi", wlan.ifconfig())
    return wlan


def stats_led(led):
    if led.value() == 1:
        print("ligado")
        return b"ligado"
    else: 
        print("desligado")
        return b"desligado"


def click_button(led):
    if led.value() == 0:
        led.value(1)
    else:
        led.value(0)


def sub_cb(topic, msg):
    global topic_pub, led
    if msg == b"ligar":
        led.on()
    elif msg == b"desligar":
        led.off()
    elif msg == None:
        pass
    else:
        client.publish(topic_pub, "mensagem incompreensível")

def connect_subscribe():
    global client_id, mqtt_server, topic_sub
    client = MQTTClient(client_id, mqtt_server, keepalive = 2000)
    client.set_callback(sub_cb)
    client.connect()
    client.subscribe(topic_sub)
    print("Broker Connectado e Topico inscrito")
    return client


def restart_and_reconnect():
    print('Falha na conexão. Reiniciando...')
    time.sleep(2)
    machine.reset()

try:
    wifi = do_connect()
    client = connect_subscribe()
except:
    restart_and_reconnect()

while True:
    if button.value() == 0:
        click_button(led)
    client.check_msg()
    client.publish(topic_pub, stats_led(led))
    time.sleep(.5)

