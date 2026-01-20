#include <WiFi.h>
#include <WebServer.h>
#include <Update.h>
#include <ArduinoJson.h>

const char* ssid = "YOUR_WIFI";
const char* password = "YOUR_PASSWORD";
const char* FIRMWARE_VERSION = "1.0.0";
const char* DEVICE_NAME = "ESP32_OTA";

WebServer server(80);

void setup() {
  Serial.begin(115200);

  WiFi.begin(ssid, password);
  while (WiFi.status() != WL_CONNECTED) delay(500);

  Serial.println("Connected");
  Serial.println(WiFi.localIP());

  server.on("/update", HTTP_POST,
    []() {
      server.sendHeader("Connection", "close");
      server.send(200, "text/plain", "Update successful. Rebooting...");
      delay(1000);
      ESP.restart();
    },
    []() {
      HTTPUpload& upload = server.upload();

      if (upload.status == UPLOAD_FILE_START) {
        Serial.println("OTA Start");
        Update.begin(UPDATE_SIZE_UNKNOWN);
      } 
      else if (upload.status == UPLOAD_FILE_WRITE) {
        Update.write(upload.buf, upload.currentSize);
      } 
      else if (upload.status == UPLOAD_FILE_END) {
        if (Update.end(true)) {
          Serial.println("OTA Success");
        } else {
          Serial.println("OTA Failed");
        }
      }
    }
  );

  // Device info endpoint
  server.on("/info", HTTP_GET, []() {
    StaticJsonDocument<200> doc;
    doc["name"] = DEVICE_NAME;
    doc["version"] = FIRMWARE_VERSION;
    doc["ip"] = WiFi.localIP().toString();
    doc["mac"] = WiFi.macAddress();
    doc["uptime"] = millis() / 1000;
    doc["rssi"] = WiFi.RSSI();
    
    String json;
    serializeJson(doc, json);
    server.send(200, "application/json", json);
  });

  // Status/ping endpoint
  server.on("/status", HTTP_GET, []() {
    server.send(200, "text/plain", "OK");
  });

  // Receive configuration endpoint (for future use)
  server.on("/config", HTTP_POST, []() {
    server.send(200, "text/plain", "Config received");
  });

  server.begin();
}

void loop() {
  server.handleClient();
}
