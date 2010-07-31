import java.util.*;
import java.math.BigDecimal;

public final class ForEachExamples {

  public static void main(String... aArgs){
    List<Number> numbers = new ArrayList<Number>();
    numbers.add(new Integer(42));
    numbers.add(new Integer(-30));
    numbers.add(new BigDecimal("654.2"));

    //typical for-each loop
    //processes each item, without changing the collection or array.
    for ( Number number : numbers ){
      log(number);
    }

    //use with an array
    String[] names = {"Ethan Hawke", "Julie Delpy"};
    for( String name : names ){
      log("Name : " + name);
    }

    //removal of items requires an explicit iterator :
    Collection<String> words = new ArrayList<String>();
    words.add("Il ne lui faut que deux choses: ");
    words.add("le");
    words.add("pain");
    words.add("et");
    words.add("le");
    words.add("temps.");
    words.add("- Alfred de Vigny.");
    for(Iterator<String> iter = words.iterator(); iter.hasNext();){
      if (iter.next().length() == 4){
        iter.remove();
      }
    }
    log("Edited words: " + words.toString());

    //if used with a non-parameterized type, then Object must be used
    Collection stuff = new ArrayList();
    stuff.add("blah");
    for (Object thing : stuff){
      String item = (String)thing;
      log("Thing : " + item);
    }
  }

  // PRIVATE //
  private static void log(Object aThing){
    System.out.println(aThing);
  }
}
