// Copyright (c) 1995 - 2008 Sun Microsystems, Inc.  All rights reserved.

class ExceptionFoo {
    public static void main(String[] args) {
	    try
	    {
	        int a = 1;
	        int b = 0;
	        int c;
	        // tested statement(s);
	        System.out.println("tested statement");
	        c = a/b;
	    }
	    catch (ArithmeticException e1)
	    {
	        // trap handler statement(s);
	        System.out.println("Exception 1");
	    }
	    catch (Exception e2)  // any number of catch statements
	    {
	        // display exception to screen
	        System.out.println("Exception 2");
	    }
	    finally
	    {
	        // always executed block
	        System.out.println("finally");
	    }
    }
}
