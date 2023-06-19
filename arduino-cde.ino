  #include <SPI.h>
  #include <MFRC522.h>
  #include <Adafruit_MLX90614.h>
  #include <Arduino.h>
  #include <Wire.h>
  #include <LiquidCrystal_PCF8574.h>

  #define SS_PIN 10
  #define RST_PIN 9
  
  MFRC522 rfid(SS_PIN, RST_PIN); // Instance of the class
  LiquidCrystal_PCF8574 lcd(0x27);


  // Init array that will store id number
  byte nuidPICC[4];
  String idstr;
  Adafruit_MLX90614 mlx = Adafruit_MLX90614();

  //for timer in irsensor and temsensor
  unsigned long starttime;
  unsigned long endtime;
  const unsigned long period = 5000;

  // for led and buzzer
  int green = 2;
  int red = 3;
  int buzzer = 4;
  int irSensor = 5;
  bool tempStatus;
  float temp;
  void setup() { 
    pinMode(green,OUTPUT);
    pinMode(red, OUTPUT);
    pinMode(buzzer, OUTPUT);
    pinMode(irSensor, INPUT);

    Serial.begin(9600);
    //init for mfrc522
    SPI.begin(); 
    rfid.PCD_Init(); 
    //init for mlx
    mlx.begin();
    int error;
    Wire.begin();
    Wire.beginTransmission(0x27);
    error = Wire.endTransmission();
    Serial.print("Error: ");
    Serial.print(error);

    if (error == 0) {
      Serial.println(": LCD found.");
      lcd.begin(16, 2);  // initialize the lcd
    } else {
      Serial.println(": LCD not found.");
    }
  }


  void loop() {
    lcd.setBacklight(255);
    lcd.home();
    lcd.clear();
  

    lcd.setCursor(0,0);
    lcd.print("WELCOME TO UC!"); 
    lcd.setCursor(0,1); 
    lcd.print("SCAN ID AND TEMP");

    //check for new card and read id num
    if(rfid.PICC_IsNewCardPresent() && rfid.PICC_ReadCardSerial()){
      digitalWrite(green,HIGH);
      digitalWrite(red,LOW);
      digitalWrite(buzzer,HIGH);
      delay(100);
      digitalWrite(green, LOW);
      digitalWrite(red, LOW);
      digitalWrite(buzzer, LOW);
      // Store NUID into nuidPICC array
      idstr="";
      for (byte i = 0; i < 4; i++) {
        nuidPICC[i] = rfid.uid.uidByte[i];
        idstr+=rfid.uid.uidByte[i];
      }

      for(int i =0; i<4; i++){
        Serial.print(rfid.uid.uidByte[i]);
      }
      Serial.print(" ");
      rfid.PICC_HaltA();
      rfid.PCD_StopCrypto1();
      delay(500);
      checkSensor();

      if(tempStatus == false){
        Serial.println("");
        lcd.clear();
        lcd.setCursor(0, 0);
        lcd.print("No Temp");
        lcd.setCursor(0, 1);
        lcd.print("Detected!");

        digitalWrite(green, LOW);
        digitalWrite(red, HIGH);
        digitalWrite(buzzer, HIGH);
        delay(1000);
        digitalWrite(green, LOW);
        digitalWrite(red, LOW);
        digitalWrite(buzzer, LOW);

        
      }else{
        tempStatus = true;
      }
    }
  }

  void checkSensor(){
    starttime=millis();
    endtime=starttime;
    //given 5 seconds for user to present hand to measure temp
    while((endtime - starttime) <=5000){
      if(digitalRead(irSensor) == 0){
        delay(500);
        temp = mlx.readObjectTempC();
        checkTemp(temp);
        tempStatus=true;
        break;
      }else{
        tempStatus=false;
      }
      endtime=millis();
    }
  }

  void checkTemp(float temp1){
    Serial.println(temp1);
    if(temp1 >= 37.5){
      lcd.clear();
      lcd.setCursor(0, 0);
      lcd.print(idstr);
      lcd.setCursor(0, 1);
      lcd.print("Temp: ");
      lcd.setCursor(6, 1);
      lcd.print(temp1);

      digitalWrite(green, LOW);
      digitalWrite(red, HIGH);
      digitalWrite(buzzer, HIGH);
      delay(500);
      digitalWrite(buzzer, LOW);
      delay(500);
      digitalWrite(buzzer, HIGH);
      delay(500);
      digitalWrite(buzzer, LOW);
      delay(500);
      digitalWrite(buzzer, HIGH);
      delay(500);
      digitalWrite(green, LOW);
      digitalWrite(red, LOW);
      digitalWrite(buzzer, LOW);

      
    }else{
      lcd.clear();
      lcd.setCursor(0, 0);
      lcd.print("ID: ");
      lcd.setCursor(4, 0);
      lcd.print(idstr);
      lcd.setCursor(0, 1);
      lcd.print("Temp: ");
      lcd.setCursor(6, 1);
      lcd.print(temp1);

      digitalWrite(green, HIGH);
      digitalWrite(red, LOW);
      digitalWrite(buzzer, HIGH);
      delay(200);
      digitalWrite(green, HIGH);
      digitalWrite(red, LOW);
      digitalWrite(buzzer, LOW);
      delay(300);
      digitalWrite(green, LOW);
      delay(500);
    }
  }

