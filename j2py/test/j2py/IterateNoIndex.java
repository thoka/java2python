// from http://www.javapractices.com/topic/TopicAction.do?Id=88

import java.util.*;

/** Different iteration styles. */
public class IterateNoIndex {
   
  /** 
  * Iterating without an index is more compact and less 
  * error prone. 
  */
   public static void withoutIndex(){
     //for-each loop
     List<String> trees = Arrays.asList("Maple", "Birch", "Poplar");
     for(String tree: trees){
       log(tree);
     }
     
     //with an Iterator
     Iterator<String> iter = trees.iterator();
     while (iter.hasNext()) {
       log(iter.next());
     }
   }
   
   /** Iterating with an index is more error prone. */
   public static void withIndex(){
     //traditional for-loop
     for(int idx=0; idx < 10; ++idx){
       log("Iteration...");
     }
   }
   
   // PRIVATE //
   private static void log(String aMessage){
     System.out.println(aMessage);
   }
   
   public static void main( String... aArguments ) {
        withoutIndex();
        withIndex();
   }

}

