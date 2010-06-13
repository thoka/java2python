// Copyright (c) 1995 - 2008 Sun Microsystems, Inc.  All rights reserved.


class ForDemo {
     public static void main(String[] args){
          for(int i=1; i<11; i++){
               if (i%2 ==0) continue;
               System.out.println("Count is: " + i);
          }
     }
}
