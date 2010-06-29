class Base {
    public int x = 42;
    public String y = null;

    public Base() {
        System.out.println("Base Constr ()");
        x = 43;
    }

    public Base(String arg) {
        System.out.println("Base Constr (string)");
        y = arg;
    }

    public Base(int arg) {
        System.out.println("Base Constr (int)");
        x = arg;
    }
}

class Test1 extends Base {
    public Test1() {
        System.out.println("Test1 Constr ()");
    }
}


class Test2 extends Base {
    public Test2() {
        super();
        System.out.println("Test2 Constr ()");
    }
}


class Test3 extends Base {
    public Test3() {
        super("arg");
        System.out.println("Test3 Constr ()");
    }
}


class Test4 extends Base {
    public Test4(int arg) {
        super(arg);
        System.out.println("Test4 Constr ()");
    }
}


public class Ctor3  {
    public static void main(String[] args) {
        System.out.println("----1----");
        Test1 t1 = new Test1();
        System.out.println(43 == t1.x ? 1 : 0);

        System.out.println("----2----");
        Test2 t2 = new Test2();
        System.out.println(43 == t2.x ? 1 : 0);

        System.out.println("----3----");
        Test3 t3 = new Test3();
        System.out.println("arg" == t3.y ? 1 : 0);
        System.out.println(42 == t3.x ? 1 : 0);

        System.out.println("----4----");
        Test4 t4 = new Test4(10);
        System.out.println(10 == t4.x ? 1 :0);
    }
}
