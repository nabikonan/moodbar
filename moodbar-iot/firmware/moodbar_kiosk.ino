// Écran LCD (mode parallèle, PAS I2C)
// RS, E, D4, D5, D6, D7
#include <LiquidCrystal.h>
LiquidCrystal lcd(12, 11, 5, 4, 3, 2);

// LEDs
#define LED_VERTE 7   // "HEUREUX"
#define LED_JAUNE 9   // "NEUTRE"
#define LED_ROUGE 10  // "TRISTE"

// Boutons
#define BTN_VERT 13
#define BTN_JAUNE 6
#define BTN_ROUGE A4

// Buzzer
#define BUZZER 8

void setup() {
  // envoie "VOTE:<humeur>" sur le port série à chaque vote, lu par
  // moodbar-iot/bridge/serial_to_api.py qui relaie vers le backend
  Serial.begin(9600);

  pinMode(LED_VERTE, OUTPUT);
  pinMode(LED_JAUNE, OUTPUT);
  pinMode(LED_ROUGE, OUTPUT);

  pinMode(BTN_VERT, INPUT_PULLUP);
  pinMode(BTN_JAUNE, INPUT_PULLUP);
  pinMode(BTN_ROUGE, INPUT_PULLUP);

  pinMode(BUZZER, OUTPUT);

  digitalWrite(LED_VERTE, LOW);
  digitalWrite(LED_JAUNE, LOW);
  digitalWrite(LED_ROUGE, LOW);

  lcd.begin(16, 2);

  lcd.setCursor(0, 0);
  lcd.print("MoodMap DIT");
  lcd.setCursor(0, 1);
  lcd.print("Bienvenue");

  delay(2000);
  menu();
}

void loop() {

  if (digitalRead(BTN_VERT) == LOW) {
    afficherHumeur(LED_VERTE, "HEUREUX :)", "content", 1000, 200);
  }
  else if (digitalRead(BTN_JAUNE) == LOW) {
    afficherHumeur(LED_JAUNE, "NEUTRE", "neutre", 700, 200);
  }
  else if (digitalRead(BTN_ROUGE) == LOW) {
    afficherHumeur(LED_ROUGE, "TRISTE", "pas_content", 400, 300);
  }
}

// `humeur` : mot-clé attendu par le backend (content / neutre / pas_content),
// séparé de `texte` qui reste libre pour l'affichage LCD
void afficherHumeur(int led, const char* texte, const char* humeur, int freq, int duree) {

  digitalWrite(LED_VERTE, LOW);
  digitalWrite(LED_JAUNE, LOW);
  digitalWrite(LED_ROUGE, LOW);

  digitalWrite(led, HIGH);
  tone(BUZZER, freq, duree);

  lcd.clear();
  lcd.setCursor(0, 0);
  lcd.print("Humeur:");
  lcd.setCursor(0, 1);
  lcd.print(texte);

  Serial.print("VOTE:");
  Serial.println(humeur);

  delay(2000);

  digitalWrite(led, LOW);

  menu();
}

void menu() {
  lcd.clear();
  lcd.setCursor(0, 0);
  lcd.print("Comment allez");
  lcd.setCursor(0, 1);
  lcd.print("vous ?");
}
