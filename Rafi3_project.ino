#include <Arduino.h>
#include <ESP8266WiFi.h>
#include <ESP8266HTTPClient.h>
#include <WiFiClient.h>
#include <Servo.h>

String auth = "xEbrFlpbqoZvihlt2TrwIMU-jPuY2SqV";

const char *ssid = "rafi3";
const char *pass = "password1";
Servo servo;
Servo servo1;

float get_data_from_blynk(const String& token, int data_stream){
  float number = 0;

  WiFiClient _client;

  HTTPClient http_client;


  String fully_request = "http://blynk.cloud/external/api/get?token=" + token + "&v" + String(data_stream);

  http_client.begin(_client, fully_request.c_str());
  http_client.addHeader("Content-Type", "text/plain");


  long elapsed = millis();  
  int return_code = http_client.GET();
  Serial.printf("[ elapsed time in ms = %ld]\n", millis() - elapsed);
  Serial.printf("[return code %d]\n", return_code);

  if(return_code > 0){

    String payload = http_client.getString();
    Serial.printf("[Response: %s]\n", payload.c_str());

    if(return_code == HTTP_CODE_OK) {
      number = payload.toFloat();
    }
  } else {
    number = 0.0;
  }

  http_client.end();

  return number;
}

void setup() {
  // put your setup code here, to run once:
  Serial.begin(115200);
  servo.attach(2);
  servo1.attach(4);

  Serial.printf("Connecting to %s\n", ssid);
  WiFi.begin(ssid, pass);
  while(WiFi.status() != WL_CONNECTED){
    delay(100);
    Serial.print(".");
  }

  Serial.printf("\n WiFi connected");


  delay(1000);
  Serial.println("Doing... some requests");
  float value = get_data_from_blynk("xEbrFlpbqoZvihlt2TrwIMU-jPuY2SqV", 4);

}

void loop() {
  // put your main code here, to run repeatedly:
  float azm_value = get_data_from_blynk("xEbrFlpbqoZvihlt2TrwIMU-jPuY2SqV", 4);
  float elev_value = get_data_from_blynk("xEbrFlpbqoZvihlt2TrwIMU-jPuY2SqV", 5);
  servo.write(azm_value);
  servo1.write(elev_value);
  delay(1000);
  
}
