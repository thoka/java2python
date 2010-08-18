public final class StringTest {

    // test parsing of umlauts: öü

    public static void main(String... aargs){
        String s="Hällo World";
        System.out.println(s.substring(0,5));
        System.out.println(s.substring(6));
        System.out.println(s.indexOf("World"));
        System.out.println(s.indexOf("bla"));
        System.out.println(s.indexOf("l"));
        System.out.println(s.indexOf("l",3));
        System.out.println(s.lastIndexOf("o"));
        System.out.println(s.charAt(0));
        System.out.println(s.replace("o","a"));
        System.out.println(s.startsWith("Hällo"));
    }
}
