/*
 * retrodiosa_IR_bypass
 * 
 * scans the serial port for a code and sends a IR code to the tv or performs a task (like turn on or off the TV).
 * 
 * serial port baudrate: 9600
 * 
 * compiled with Arduino 1.8.7
 */


#define PIN 3

#define ANALOG_TV_LED_PIN A0

unsigned int rawDataLen = 67;

const uint16_t onOffRawData[67] PROGMEM = {4550,4350, 700,1500, 700,1550, 700,1500, 700,450, 700,450, 700,450, 650,450, 700,500, 700,1550,
                                650,1550, 700,1550, 700,400, 700,450, 700,450, 700,450, 650,500, 700,450, 700,1550, 650,450, 700,450,
                                700,450, 700,400, 700,450, 700,500, 700,1550, 650,450, 700,1550, 700,1500, 700,1550, 700,1500,
                                700,1550, 700,1550, 700};  // SAMSUNG E0E040BF

const uint16_t chanPlusRawData[67] PROGMEM = {4500,4450, 600,1600, 650,1600, 600,1600, 650,500, 650,500, 600,500, 650,500, 650,550, 650,1550,
                                    650,1600, 650,1550, 650,500, 650,500, 600,550, 600,500, 650,550, 650,500, 650,500, 600,500, 650,500,
                                    650,1600, 600,1600, 650,1600, 600,600, 600,1600, 650,1600, 600,1600, 650,1600, 600,500, 650,500,
                                    600,550, 600,1600, 650};  // SAMSUNG E0E00EF1

const uint16_t chanMinusRawData[67] PROGMEM = {4600,4350, 650,1550, 700,1550, 650,1550, 700,450, 700,450,
                                                                            650,450, 700,450, 700,500, 700,1500, 700,1550, 700,1550,
                                                                            650,450, 700,450, 700,450, 650,450, 700,500, 700,1550,
                                                                            700,400, 700,450, 700,450, 700,1500, 700,1550, 700,1500,
                                                                            700,500, 700,450, 700,1550, 650,1550, 700,1550, 700,400,
                                                                            700,450, 700,450, 700,1500, 700};  // SAMSUNG E0E08E71

const uint16_t volPlusRawData[67] PROGMEM = {4550,4350, 700,1550, 650,1550, 700,1550, 650,450, 700,450, 700,450, 700,400, 700,500, 700,1550,
                                    700,1500, 700,1550, 700,450, 650,450, 700,450, 700,450, 700,500, 650,450, 700,1550, 700,450, 650,450,
                                    700,1550, 700,1500, 700,1550, 700,500, 700,1500, 700,450, 700,1550, 650,1550, 700,450, 700,400,
                                    700,450, 700,1550, 700};  // SAMSUNG E0E04EB1

const uint16_t volMinusRawData[67] PROGMEM = {4500,4400, 650,1600, 650,1550, 650,1600, 650,450, 700,450, 650,500, 650,450, 700,500, 700,1550,
                                              650,1550, 700,1550, 650,500, 650,450, 700,450, 700,450, 650,550, 650,1550, 650,1600, 650,450,
                                              700,450, 650,1600, 650,1550, 650,1600, 650,550, 650,450, 700,450, 650,1600, 650,1550, 650,500,
                                              650,450, 700,450, 650,1600, 650};  // SAMSUNG E0E0CE31


const uint16_t muteRawData[67] PROGMEM = {4600,4300, 750,1500, 700,1500, 750,1500, 700,450, 700,400, 750,400, 700,450, 700,500, 700,1500, 750,1500,
                                  700,1500, 750,400, 700,450, 700,400, 750,400, 700,500, 700,1550, 700,1500, 700,450, 700,400, 750,400,
                                  750,1500, 700,400, 750,450, 750,400, 700,450, 700,1500, 750,1500, 700,1500, 750,400, 700,1550, 700,1500,
                                  750};  // SAMSUNG E0E0C43B

const uint16_t menuRawData[67] PROGMEM = {4600,4300, 700,1550, 700,1500, 750,1500, 700,400, 750,400, 700,450, 700,400, 750,450, 750,1500, 700,1500,
                                  750,1500, 700,450, 700,400, 750,400, 750,400, 700,500, 700,1500, 750,1500, 700,1500, 750,1500, 700,450,
                                  700,400, 750,400, 700,500, 700,450, 700,400, 750,400, 700,450, 700,1500, 750,1500, 700,1500, 750,1500,
                                  700};  // SAMSUNG E0E0F00F

const uint16_t exitRawData[67] PROGMEM = {4550,4350, 700,1500, 700,1550, 700,1500, 700,450, 700,450, 700,400, 700,450, 700,500, 700,1550, 650,1550,
                                  700,1550, 700,400, 700,450, 700,450, 700,400, 700,500, 700,450, 700,450, 700,1500, 700,1550, 700,450,
                                  650,1550, 700,450, 700,500, 700,1500, 700,1550, 700,400, 700,450, 700,1550, 700,400, 700,1550, 700,1550,
                                  700};  // SAMSUNG E0E034CB

const uint16_t okRawData[67] PROGMEM = {4550,4350, 700,1500, 700,1550, 700,1500, 700,450, 700,450, 700,450, 700,400, 750,450, 700,1550, 700,1500,
                                700,1550, 700,450, 650,450, 750,400, 700,450, 700,500, 650,450, 700,1550, 700,400, 700,1550, 700,1550,
                                650,450, 700,450, 700,500, 700,1500, 700,450, 700,1550, 650,450, 700,450, 700,1550, 650,1550, 700,1550,
                                700};  // SAMSUNG E0E058A7

const uint16_t arrowUpRawData[67] PROGMEM = {4550,4350, 650,1550, 650,1600, 650,1550, 650,500, 650,500, 650,450, 650,500, 650,550, 650,1600,
                                    600,1600, 650,1600, 600,500, 650,500, 650,500, 650,450, 650,550, 650,500, 650,1600, 600,500, 650,500,
                                    650,1600, 600,500, 650,500, 650,550, 650,1550, 650,500, 650,1600, 600,1600, 650,500, 650,1550,
                                    650,1600, 650,1600, 600};  // SAMSUNG E0E048B7

const uint16_t arrowDownRawData[67] PROGMEM = {4550,4350, 700,1500, 750,1500, 700,1500, 750,400, 750,400, 700,450, 700,400, 750,450, 700,1550,
                                      700,1500, 700,1550, 700,450, 700,400, 700,450, 700,450, 700,500, 650,450, 700,450, 700,450, 700,400,
                                      700,1550, 700,450, 650,450, 700,500, 700,1550, 700,1500, 700,1550, 700,1500, 750,400, 700,1550,
                                      700,1500, 700,1550, 700};  // SAMSUNG E0E008F7

const uint16_t arrowRightRawData[67] PROGMEM = {4550,4350, 700,1550, 650,1550, 700,1550, 650,450, 700,450, 700,450, 700,400, 700,500, 700,1550,
                                        700,1500, 700,1550, 700,450, 650,450, 700,450, 700,450, 700,500, 650,1550, 700,1550, 700,1500,
                                        700,450, 700,450, 650,450, 700,450, 700,500, 700,450, 700,400, 700,450, 700,1550, 650,1550,
                                        700,1550, 700,1500, 700,1550, 700};  // SAMSUNG E0E0E01F

const uint16_t arrowLeftRawData[67] PROGMEM = {4550,4400, 600,1600, 650,1600, 600,1600, 650,500, 650,500, 600,500, 650,500, 650,550, 650,1550,
                                      650,1600, 650,1550, 650,500, 650,500, 650,500, 600,500, 650,550, 650,1600, 600,1600, 650,500,
                                      650,1550, 650,500, 650,500, 650,500, 600,550, 650,500, 650,500, 650,1550, 650,500, 650,1600,
                                      600,1600, 650,1600, 650,1550, 650};  // SAMSUNG E0E0D02F

const uint16_t selectTvRawData[67] PROGMEM = {4550,4350, 700,1500, 700,1550, 700,1500, 700,450, 700,450, 700,450, 650,450, 700,500, 700,1550,
                                      700,1500, 700,1550, 700,400, 700,450, 700,450, 700,450, 650,500, 700,1550, 700,450, 700,400,
                                      700,450, 700,450, 700,400, 700,450, 700,500, 700,450, 700,1500, 700,1550, 700,1500, 700,1550,
                                      700,1500, 700,1550, 700,1550, 700};  // SAMSUNG E0E0807F

const uint16_t selectPcRawData[67] PROGMEM = {4500,4450, 650,1550, 650,1600, 650,1550, 700,450, 700,450, 650,450, 700,450, 700,500, 700,1500,
                                      700,1550, 700,1500, 700,450, 700,450, 700,450, 650,450, 700,500, 700,1550, 700,400, 700,450,
                                      700,1550, 650,450, 700,1550, 700,1500, 700,500, 700,450, 700,1550, 650,1550, 700,450, 700,1500,
                                      700,450, 700,450, 700,1500, 700};  // SAMSUNG E0E09669

const uint16_t selectVideoRawData[67] PROGMEM = {4550,4350, 700,1500, 700,1550, 700,1550, 650,450, 700,450, 700,450, 700,400, 750,450, 700,1550,
                                        700,1500, 700,1550, 700,450, 650,450, 700,450, 700,450, 700,500, 700,400, 700,450, 700,450,
                                        700,1500, 700,1550, 700,1500, 700,1550, 700,500, 700,1500, 700,1550, 700,1500, 700,450, 700,450,
                                        700,400, 700,450, 700,1550, 700};  // SAMSUNG E0E01EE1

const uint16_t selectScartRawData[67] PROGMEM = {4550,4350, 600,1600, 600,1650, 600,1600, 600,550, 600,550, 600,500, 600,550, 600,600, 600,1650,
                                        550,1650, 600,1650, 600,500, 600,550, 600,550, 600,500, 600,600, 650,1600, 600,550, 600,500,
                                        650,1600, 600,1600, 600,1650, 600,1600, 600,600, 650,500, 600,1650, 600,1600, 650,500, 600,550,
                                        600,500, 650,500, 600,1650, 600};  // SAMSUNG E0E09E61

const uint16_t pipSourceLeftRawData[67] PROGMEM = {4550,4350, 650,1600, 650,1550, 650,1600, 650,500, 650,450, 650,500, 650,500, 650,550, 650,1550,
                                          650,1600, 650,1550, 650,500, 650,500, 650,450, 650,500, 650,550, 650,500, 650,1550, 650,500,
                                          650,500, 650,1550, 650,1600, 650,450, 650,550, 650,1600, 650,500, 650,1550, 650,1600, 600,500,
                                          650,500, 650,1600, 600,1600, 650};  // SAMSUNG E0E04CB3

const uint16_t pipSourceRightRawData[67] PROGMEM = {4550,4350, 700,1500, 700,1550, 700,1550, 650,450, 700,450, 700,450, 700,400, 700,500, 700,1550,
                                             700,1500, 700,1550, 700,450, 650,450, 700,450, 700,450, 700,500, 650,1550, 700,450, 700,450,
                                             650,450, 700,450, 700,450, 650,450, 700,1600, 700,450, 700,1500, 700,1550, 700,1500,
                                             700,1550, 700,1500, 700,1550, 700,450, 700};  // SAMSUNG E0E0817E


struct menu_to_rawdata_mapping {
  char menu;
  const uint16_t *rawData;
};

const int menu_map_len = 19;
struct menu_to_rawdata_mapping menu_map[] = {{.menu='q', .rawData=onOffRawData},
                                            {.menu='w', .rawData=chanPlusRawData},
                                            {.menu='e', .rawData=chanMinusRawData},
                                            {.menu='r', .rawData=volPlusRawData},
                                            {.menu='t', .rawData=volMinusRawData},
                                            {.menu='y', .rawData=muteRawData},
                                            {.menu='u', .rawData=menuRawData},
                                            {.menu='i', .rawData=exitRawData},
                                            {.menu='o', .rawData=okRawData},
                                            {.menu='p', .rawData=arrowUpRawData},
                                            {.menu='a', .rawData=arrowDownRawData},
                                            {.menu='s', .rawData=arrowRightRawData},
                                            {.menu='d', .rawData=arrowLeftRawData},
                                            {.menu='f', .rawData=selectTvRawData},
                                            {.menu='g', .rawData=selectPcRawData},
                                            {.menu='h', .rawData=selectVideoRawData},
                                            {.menu='j', .rawData=selectScartRawData},
                                            {.menu='k', .rawData=pipSourceLeftRawData},
                                            {.menu='l', .rawData=pipSourceRightRawData}};



void send_raw_data_no_modulated(unsigned int *rawdata, unsigned int len){

  digitalWrite(PIN, HIGH);
  for (int i = 0; i < len; i++){
    digitalWrite(PIN, !digitalRead(PIN));
    delayMicroseconds(rawdata[i]);
  }
  digitalWrite(PIN, HIGH);
}


void send_raw_data_no_modulated_from_progmem(unsigned int *rawdata, unsigned int len){

  digitalWrite(PIN, HIGH);
  for (int i = 0; i < len; i++){
    digitalWrite(PIN, !digitalRead(PIN));
    delayMicroseconds(pgm_read_word_near(rawdata + i));
  }
  digitalWrite(PIN, HIGH);
}

bool is_tv_on(){
  int val = analogRead(ANALOG_TV_LED_PIN);
  if (val < 300){
    return true;
  }
  return false;
}


void send_command_if_available(char a){
  for (int i = 0; i < menu_map_len; i ++){
    if (a == menu_map[i].menu){
      send_raw_data_no_modulated_from_progmem(menu_map[i].rawData, rawDataLen);
      return -1;
    }
  }
}


void perform_task_if_available(char a){

  // Turn ON
  if (a == '1'){
    for(int i = 0; i < 10; i++){
      if (is_tv_on()){
        break;
      }
      else {
        send_raw_data_no_modulated_from_progmem(onOffRawData, rawDataLen);
        delay(500);
      }
    }
  }
  else if (a == '2'){
    for (int i = 0; i < 10; i++){
      if (is_tv_on()){
        send_raw_data_no_modulated_from_progmem(onOffRawData, rawDataLen);
        delay(500);
      }
      else {
        break;
      }
    }
  }
}

void setup()
{
  pinMode(PIN, OUTPUT);
  digitalWrite(PIN, HIGH);
  Serial.begin(9600);
}


void loop()
{
  if (Serial.available() > 0) {
    char a = Serial.read();
    Serial.write(a);
    send_command_if_available(a);
    perform_task_if_available(a);
  }
  is_tv_on();
}
