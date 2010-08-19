interface Runnable {
    void run();
}

public final class AnonymClass {

  static void run(Runnable r) {
      r.run();
   }

  public static void main( String... aArguments ) {

    run( new Runnable() {
        public void run() {
            System.out.println("running ...");
        }
    });
  }

}
