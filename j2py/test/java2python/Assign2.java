class Assign2 {
    public static void main(String[] args) {
        int x = 42, y=7;
        System.out.println(x);

        x >>>= 1;        
        System.out.println(x);
        
        x = 2 + x >>> 1;
        System.out.println(x);
        System.out.println(y);

        y = x++;
        System.out.println(x);
        System.out.println(y);
                
        y = ++x;
        System.out.println(x);
        System.out.println(y);
                

        y = x--;
        System.out.println(x);
        System.out.println(y);
                
        y = --x;
        System.out.println(x);
        System.out.println(y);

        x++; --y;
        System.out.println(x);
        System.out.println(y);
                
        --y; ++x;
        System.out.println(x);
        System.out.println(y);


    }
}
