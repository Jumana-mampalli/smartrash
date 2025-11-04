// Smart Bin Code - NodeMCU with Ultrasonic Sensor and LEDs

#include <ESP8266WiFi.h>
#include <ESP8266HTTPClient.h>

// WiFi Credentials
const char* ssid = "YOUR_WIFI_SSID";
const char* password = "YOUR_WIFI_PASSWORD";

// Server URL
const char* serverUrl = "http://YOUR_SERVER_IP:8000/api/bin/update/";

// Bin ID
String binId = "BIN001";

// Pins
const int trigPin = D1;
const int echoPin = D2;
const int blueLED = D5;   // WiFi indicator
const int greenLED = D6;  // Normal status
const int redLED = D7;    // Bin full

// Variables
long duration;
int distance;
int binHeight = 30;  // cm
int currentLevel = 0;
unsigned long lastUpdate = 0;
const long updateInterval = 60000;  // 1 minute

void setup() {
  Serial.begin(115200);
  
  pinMode(trigPin, OUTPUT);
  pinMode(echoPin, INPUT);
  pinMode(blueLED, OUTPUT);
  pinMode(greenLED, OUTPUT);
  pinMode(redLED, OUTPUT);
  
  // Connect to WiFi
  WiFi.begin(ssid, password);
  Serial.print("Connecting to WiFi");
  
  while (WiFi.status() != WL_CONNECTED) {
    delay(500);
    Serial.print(".");
  }
  
  Serial.println("\nWiFi Connected!");
  Serial.println(WiFi.localIP());
  
  digitalWrite(blueLED, HIGH);  // WiFi connected
  digitalWrite(greenLED, HIGH); // Normal status
}

void loop() {
  // Check WiFi connection
  if (WiFi.status() == WL_CONNECTED) {
    digitalWrite(blueLED, HIGH);
  } else {
    digitalWrite(blueLED, LOW);
  }
  
  // Measure distance
  digitalWrite(trigPin, LOW);
  delayMicroseconds(2);
  digitalWrite(trigPin, HIGH);
  delayMicroseconds(10);
  digitalWrite(trigPin, LOW);
  
  duration = pulseIn(echoPin, HIGH);
  distance = duration * 0.034 / 2;
  
  // Calculate fill level percentage
  if (distance < binHeight) {
    currentLevel = map(distance, binHeight, 0, 0, 100);
    currentLevel = constrain(currentLevel, 0, 100);
  } else {
    currentLevel = 0;
  }
  
  Serial.print("Distance: ");
  Serial.print(distance);
  Serial.print(" cm | Level: ");
  Serial.print(currentLevel);
  Serial.println("%");
  
  // Update LED status
  if (currentLevel >= 75) {
    digitalWrite(greenLED, LOW);
    digitalWrite(redLED, HIGH);
  } else {
    digitalWrite(greenLED, HIGH);
    digitalWrite(redLED, LOW);
  }
  
  // Send data to server every minute
  if (millis() - lastUpdate >= updateInterval) {
    sendDataToServer();
    lastUpdate = millis();
  }
  
  delay(5000);  // Check every 5 seconds
}

void sendDataToServer() {
  if (WiFi.status() == WL_CONNECTED) {
    HTTPClient http;
    WiFiClient client;
    
    http.begin(client, serverUrl);
    http.addHeader("Content-Type", "application/json");
    
    String jsonData = "{\"bin_id\":\"" + binId + "\",\"level\":" + String(currentLevel) + "}";
    
    int httpCode = http.POST(jsonData);
    
    if (httpCode > 0) {
      String response = http.getString();
      Serial.println("Server Response: " + response);
    } else {
      Serial.println("Error sending data");
    }
    
    http.end();
  }
}