//Brewing Java: A Tutorial Copyright 1995-1998, 2000-2002, 2004-2006 Elliotte Rusty Harold
// Print a Fahrenheit to Celsius table

class FahrToCelsius  {

  public static void main (String[] args) {
  
  int fahr, celsius;
  int lower, upper, step;

  lower = 0;      // lower limit of temperature table
  upper = 300;  // upper limit of temperature table
  step  = 20;     // step size

  fahr = lower;
  while (fahr <= upper) {  // while loop begins here
    celsius = 5 * (fahr-32) / 9;
    System.out.print(fahr);
    System.out.print(" ");
    System.out.println(celsius);
    fahr = fahr + step;
  } // while loop ends here
} // main ends here

} //FahrToCelsius ends here 