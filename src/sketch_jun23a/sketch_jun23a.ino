void setup() 
{
  Serial.begin(9600);
}

void loop() 
{

  int value0 = analogRead(36);
  int value1 = analogRead(39);
  int value2 = analogRead(34);
  Serial.print(value0);
  Serial.print(" ");
  Serial.print(value1);
  Serial.print(" ");
  Serial.println(value2);

  delay(500);
}
