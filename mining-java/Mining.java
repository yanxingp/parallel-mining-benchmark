import java.security.MessageDigest;
import java.nio.charset.StandardCharsets;

public class Mining
{
    static String data = "parallel-mining-benchmark";
    static String global_result = "";
    static int ntrial = 10;
    static int difficulty = 5;
    static String prefix;

    private static final char[] HEX_ARRAY = "0123456789ABCDEF".toCharArray();

    public static String bytesToHex(byte[] bytes) {
        char[] hexChars = new char[bytes.length * 2];
        for (int j = 0; j < bytes.length; j++) {
            int v = bytes[j] & 0xFF;
            hexChars[j * 2] = HEX_ARRAY[v >>> 4];
            hexChars[j * 2 + 1] = HEX_ARRAY[v & 0x0F];
        }
        return new String(hexChars);
    }

    public static void sequential() {
        for (int i = 0; i < ntrial; i++) {
            String ldata = data + i;
            int nonce = 0;
            while (true) {
                String s = ldata + nonce;
                MessageDigest digest = null;
                try {
                    digest = MessageDigest.getInstance("SHA-256");
                } catch (Exception e) {}
                String hash = bytesToHex(digest.digest(s.getBytes(StandardCharsets.UTF_8)));

                if (hash.startsWith(prefix)) {
                    global_result = hash;
                    break;
                }
                nonce++;
            }
        }
    }

    static class Control {
        public volatile boolean found = false;
    }

    static class MiningWorker implements Runnable {
        int id;
        int nthread;
        String ldata;
        Control control;

        MiningWorker(int id, int nthread, String ldata, Control control) {
            this.id = id;
            this.nthread = nthread;
            this.ldata = ldata;
            this.control = control;
        }

        @Override
        public void run() {
            int nonce = id;
            while (!control.found) {
                String s = ldata + nonce;
                MessageDigest digest = null;
                try {
                    digest = MessageDigest.getInstance("SHA-256");
                } catch (Exception e) {}
                String hash = bytesToHex(digest.digest(s.getBytes(StandardCharsets.UTF_8)));

                if (hash.startsWith(prefix)) {
                    global_result = hash;
                    control.found = true;
                    break;
                }
                nonce += nthread;
            }
        }
    }

    public static void parallelMultithread(int nthread) {
        Thread threads[] = new Thread[nthread];
        for (int i = 0; i < ntrial; i++) {
            String ldata = data + i;
            Control control = new Control();
            for (int j = 0; j < nthread; j++) {
                threads[j] = new Thread(new MiningWorker(j, nthread, ldata, control));
            }
            for (int j = 0; j < nthread; j++) {
                threads[j].start();
            }
            for (int j = 0; j < nthread; j++) {
                try {
                    threads[j].join();
                } catch (Exception e) {
                    e.printStackTrace();
                }
            }
        }
    }

    public static void main( String[] args )
    {
        String line = "";
	    for (int i = 0; i < 40; i++) {
		    line += "-";
	    }

        prefix = "";
        for (int i = 0; i < difficulty; i++) {
            prefix += "0";
        }

        System.out.println(line);
	    System.out.println("Java Version:");
        System.out.println("difficulty: " + difficulty + ", number of trials: " + ntrial);

        // sequential
        System.out.println(line);
        long start = System.nanoTime();
        sequential();
        long elapsed = System.nanoTime() - start;
        System.out.println("sequential version:");
        System.out.println("total time consumed: " + 
            String.format("%.4f", (double) elapsed / 1_000_000_000));
        System.out.println("average time consumed: " + 
            String.format("%.4f", (double) elapsed / 1_000_000_000 / ntrial));
        System.out.println("last hash computed: " + global_result);

        // multi-thread parallel
        int nthreads[] = {2, 4, 8, 16};
        for (int i = 0; i < nthreads.length; i++) {
            System.out.println(line);
            long startp = System.nanoTime();
            parallelMultithread(nthreads[i]);
            long elapsedp = System.nanoTime() - startp;
            System.out.println(Integer.toString(nthreads[i]) + " thread parallel version:");
            System.out.println("total time consumed: " + 
                String.format("%.4f", (double) elapsedp / 1_000_000_000));
            System.out.println("average time consumed: " + 
                String.format("%.4f", (double) elapsedp / 1_000_000_000 / ntrial));
            System.out.println("last hash computed: " + global_result);
        }
    }
}
