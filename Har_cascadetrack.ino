//Pre-set-up

char temp;
char serial_input;
bool b_left=false;
bool b_right=false;
bool b_up=false;
bool b_down=false;


//The stepper motors gave me the most trouble of //the entire project.
#include <Stepper.h>
  Stepper myStepper(200, 8,10);
  Stepper myStepper2(200,7,11);
 // Stepper myStepper(200, 9, 10, 11, 12);






byte dir=8;
byte stp=10;
byte dir2=7;
byte stp2=11;



void serial_read_and_bool_determination();
void motorRight();
void motorLeft();
void motorUp();
void motorDown();




void setup() {

  Serial.begin(9600);       
  pinMode(dir, OUTPUT); //dir
  pinMode(stp, OUTPUT); //step
  pinMode(dir2,OUTPUT);
  pinMode(stp2,OUTPUT);
  digitalWrite(dir, LOW);
  digitalWrite(stp, LOW);
  digitalWrite(dir2, LOW);
  digitalWrite(stp2, LOW);
  
  
  



}


//**MAIN LOOP********//
void loop()    {
  
  
  //constantly checking the pi for updates.
  //the pi is the brain. The arduino just executes commands, like a perfect soldier.
  serial_read_and_bool_determination();

  if(b_right )
  {
    motorRight();
    
   }
  
      
  if(b_left)
  {
    motorLeft();
  }

  if(b_up) 
  { 
    motorUp();
  }
  if(b_down )
  {
   motorDown();
   
  }
    
    
   
   
        }
  
    
  
    
  
    
 

//**END MAIN LOOP********//

//Here are all the serial read commands and most //of the logic that determines the robots entire //entire functionality.
void serial_read_and_bool_determination(){
    if(Serial.available()>0){
      temp=Serial.read();
      //delay(1000);
      
      
      if((temp!='\n')&&(temp!='\r')){
        serial_input=temp;
        digitalWrite(8,LOW);
        digitalWrite(10,LOW);
       // digitalWrite(11,LOW);
       // digitalWrite(12,LOW);
    
        switch (serial_input){
          case 'l':
            b_right=false;
            b_left=true;
            
            
           break;
          case 'r':
            b_left=false;
            b_right=true;
            
            
            break;
          case'u':
            b_up=true;
            b_down=false;
            
            break;
          case'd':
            b_up=false;
            b_down=true;
            break;  
          case's':
          Serial.flush();
          delay(100000);
          return 0 ;
          
            
  break;
        }
      }   
    }
}

//the rest of this code is pretty self-explanatory //through the simple fact that I used very //descriptive and relevant variable/function names.





void motorRight(){
    myStepper.setSpeed(10);
    myStepper.step(1);
    
    //Serial.write(byte('f'));
    }
    
void motorUp()
{
  
   myStepper2.setSpeed(10);
    myStepper2.step(1);
  
  }
void motorDown()
{
  
   myStepper2.setSpeed(10);
    myStepper2.step(-1);
  
}
void motorLeft(){
    myStepper.setSpeed(10);
    myStepper.step(-1);
    //Serial.write(byte('f'));
    }
