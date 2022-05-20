"""GUi para controlar o led do esp32
"""
import dash
from dash.dependencies import Input, Output, State
from dash import html
from dash import dcc
import dash_daq as daq
import dash_mqtt

TEST_SERVER = 'IP_MQTT_SERVER'
SERVER_PORT = 9001
TOPIC_PUB = 'entrada'
TOPIC_SUB = 'saida'

app = dash.Dash(__name__,)


app.layout = html.Div([
    dash_mqtt.DashMqtt(
        id='mqtt',
        broker_url=TEST_SERVER,
        broker_port = SERVER_PORT,
        topics=[TOPIC_SUB]
    ),
    daq.PowerButton(
        id='button',
        on=False,
        size=100,
        label="led",
        labelPosition="top"
    ),
])


@app.callback(
        Output('mqtt', 'message'),
        Input('button', 'on')
    )
def controle_led(on):
    if on:
        estado = 'ligar'
    elif not on:
        estado = 'desligar'
    return {
            'topic': TOPIC_PUB,
            'payload' : estado
        }

@app.callback(
        Output('button', 'on'),
        Input('mqtt', 'incoming')
    )
def estado_led(incoming):
    if not incoming is None:
        estado = incoming['payload']
    if estado == 'ligado':
        return True
    else:
        return False


if __name__ == '__main__':
    app.run_server(debug=True)
