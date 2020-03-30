import RPi.GPIO as GPIO  # import GPIO
import mysql.connector;
import paho.mqtt.client as mqtt

####### Connection to database
cnx = mysql.connector.connect(user='pi', password='pi',
                              host='localhost',
                              port='3306',
                              database='Warehouse'
                              );
cursor = cnx.cursor();

### receiving message
def on_message(client, userdata, message):
    msg = str(message.payload.decode("UTF-8"))
    print("message received: ", msg)
    print("message topic: ", message.topic)
    tpc = message.topic
    if tpc == "WS/shelf/white": #### every topic gets a product ID
        product = 1
    if tpc == "WS/shelf/gray":
        product = 2
    if tpc == "WS/shelf/caribbeanBlue":
        product = 3
    if tpc == "WS/shelf/red":
        product = 4
    if tpc == "WS/shelf/yellow":
        product = 5
    if tpc == "WS/shelf/blue":
        product = 6
    
    
    try:
        query = "INSERT INTO shelf (topic, weight, productID) VALUES (%s, %s, %s)";
        int (msg)
        vals = (tpc, msg, product);
        result = cursor.execute(query, vals)
        cnx.commit()
        print('writen success to database')
    except:
        cnx.rollback()
        print('cant mysql');

def on_connect(client, userdata, flags, rc):
    client.subscribe('WS/shelf/#')

BROKER_ADDRESS = "localhost"

client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message

client.connect(BROKER_ADDRESS)
print("Connected to MQTT Broker: "+ BROKER_ADDRESS)
client.loop_forever()
