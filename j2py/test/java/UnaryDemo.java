// Copyright (c) 1995 - 2008 Sun Microsystems, Inc.  All rights reserved.

class UnaryDemo {

     public static void main(String[] args){
          int result = +1; // result is now 1
          System.out.println(result);
          result--;  // result is now 0
          System.out.println(result);
          result++; // result is now 1 
          System.out.println(result);
          result = -result; // result is now -1
          System.out.println(result);
          boolean success = false;
          System.out.println(success); // false
          System.out.println(!success); // true
     }
}