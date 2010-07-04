public class StatInit {

    static int i = 0;
    
    static {
      someStatMethod();
    }

    static void someStatMethod() {
       i++;
       System.out.println(i);
    }
    
    public static void main(String[] args) {
        System.out.println(i);
    }
    
}


