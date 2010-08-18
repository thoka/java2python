//Brewing Java: A Tutorial Copyright 1995-1998, 2000-2002, 2004-2006 Elliotte Rusty Harold
class iWebsite {

  public String name;
  public String url;
  public String description;
  public static int site_count = 0;

  public iWebsite() {
    site_count++;
  }

  public void printme() {
     System.out.println(name + " at " + url + " is " + description);
     System.out.println("Number of class instances: " + site_count);
  }
}


public class Website2 {

  public static void main(String args[]) {
    iWebsite w = new iWebsite();
    w.name = "Jorika";
    w.url = "http://jorika.edu";
    w.description = "Really cool!";
    w.printme();
    //
    iWebsite w2 = new iWebsite();
    w2.name = "Foggi 4";
    w2.url = "http://foggi4youevery.fa";
    w2.description = "Foggi file!";
    w2.printme();
  }
}
