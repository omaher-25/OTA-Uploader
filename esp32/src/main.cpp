#include <WiFi.h>
#include <WebServer.h>
#include <Update.h>

const char* ssid = "YOUR_WIFI";
const char* password = "YOUR_PASSWORD";

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

  server.begin();
}

void loop() {
  server.handleClient();
}
