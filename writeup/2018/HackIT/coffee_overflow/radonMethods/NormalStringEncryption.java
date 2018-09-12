package me.itzsomebody.radon.templates;

class NormalStringEncryption {
    public static String decrypt(Object encryptedString, Object useless, int key3) {
        if (useless == null && key3 != 0) {
            String msg = (String) encryptedString;
            StackTraceElement ste = new Throwable().getStackTrace()[0];
            int key1 = ste.getClassName().hashCode();
            int key2 = ste.getMethodName().hashCode();
            int i = 0;
            char[] chars = msg.toCharArray();
            char[] returnThis = new char[chars.length];
            while (i < msg.toCharArray().length) {
                returnThis[i] = (char) (chars[i] ^ key1 ^ key2 ^ (int) key3);
                i++;
            }
            return new String(returnThis);
        }
        return null;
    }
}



"rabbit hole"
"nice kitten"
"mad dog!"
"the winrar is u! subit password as flag!"