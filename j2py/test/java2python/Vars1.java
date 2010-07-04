class Vars1 {
    static int a = 100;
    static int b = 2;
    int c;

    private void x() {
	    System.out.println('x');
    }

    private void y() {
        a++;
  	    System.out.println(a);
    }


    private void z(int a) {
	    System.out.println(a);
    }
    
    public static void main(String[] args) {
	    System.out.println(a);
	    System.out.println(b);

	    Vars1 v = new Vars1();
	    v.x();
	    v.y();
	    v.y();
	    v.y();
	    v.z(3);
	    System.out.println(a);

    }
}
