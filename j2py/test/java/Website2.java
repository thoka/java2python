//Brewing Java: A Tutorial Copyright 1995-1998, 2000-2002, 2004-2006 Elliotte Rusty Harold

public class Website {

  public String name;
  public String url;
  public String description;
  public static int site_count = 0;
 
  public Website() {
    site_count++;
  }
  
  public void printme() {
     System.out.println(name + " at " + url + " is " + description);
     System.out.println("Number of class instances: " + site_count);
  }

  public static void main(String args[]) {
Website w = new Website();
w.name = "Jorika";
    w.url = "http://jorika.edu";
    w.description = "Really cool!";
    w.printme();
    
    Website w2 = new Website();
    w.name = "Foggi 4";
    w.url = "http://foggi4youevery.fa";
    w.description = "Foggi file!";
    w.printme();  
  }
}
