byte byteRead;
long num1, num2, num3;
int mySwitch=0;

int green = 9;
int red = 10;
int blue = 11;

void setup() {                
/* Turn the Serial Protocol ON and 
   initialise num1 and num2 variables.*/
  Serial.begin(9600);
  num1=0;
  num2=0;
  num3=0;
  
  pinMode(red, OUTPUT);
  pinMode(green, OUTPUT);
  pinMode(blue,OUTPUT);
}

void loop() {
   /*  check if data has been sent from the computer: */
  while (Serial.available()) {
    /* read the most recent byte */
    byteRead = Serial.read();
    
    //listen for numbers between 0-9
    if(byteRead>47 && byteRead<58){
       //number found
      
       /* If mySwitch is true, then populate the num1 variable
          otherwise populate the num2 variable*/
       if(mySwitch==0){
         num1=(num1*10)+(byteRead-48);
       }else if(mySwitch==1){
         num2=(num2*10)+(byteRead-48);
       }
       else if(mySwitch==2){
         num3=(num3*10)+(byteRead-48);
       }
    }
    
    /*Listen for an smei-colon
      to calculate the answer and send it back to the
      serial monitor screen*/
    if(byteRead==59){
      analogWrite(blue, num3);
      analogWrite(green, num2);
      analogWrite(red, num1);
      /* Reset the variables for the next round */
      num1=0;
      num2=0;
      num3=0;
      mySwitch=0;
      
    /* Listen for the addition sign (byte code 43). This is
       used as a delimiter to help define num1 from num2 */  
    }else if (byteRead==44){
      mySwitch+=1;
    }
  }
}
