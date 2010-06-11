// Copyright (c) 1995 - 2008 Sun Microsystems, Inc.  All rights reserved.

class Exceptionfoo {
     public static void main(String[] args) {
	try
	{
	    // tested statement(s);
	    System.out.println("tested statement");
	}
	catch (ExceptionName e1)
	{
	    // trap handler statement(s);
	    System.out.println("Exception 1: " + e1);
	}
	catch (ExceptionName e2)  // any number of catch statements
	{
	    // display exception to screen
	    System.out.println("Exception 2: " + e2);
	}
	finally
	{
	    // always executed block
	    System.out.println("finally");
	}
    }
}
