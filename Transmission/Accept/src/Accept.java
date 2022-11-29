import java.io.*;
import java.net.*;
import java.nio.charset.StandardCharsets;

public class Accept {
    private static InetAddress host;
    private static int port;
    private static DatagramSocket socket;
    private static DatagramPacket packet;
    private static final int MAX_SIZE = 1500;
    private static String desktopPath;
    private static int os = 0;

    public static void main(String[] args) throws Exception {
        if (args.length != 2) {
            System.exit(1);
        }

        if (System.getProperty("os.name").equals("Mac OS X")) {
            desktopPath = "/Users/enmmmmovo/Desktop/";
            os = 1;
        } else if (System.getProperty("os.name").equals("Windows 11")) {
            desktopPath = "C:/Users/wangj/Desktop/";
            os = 2;
        }

        host = InetAddress.getByName(args[0]);
        port = Integer.parseInt(args[1]);

        try {
            accept();
        } catch (Exception e){
            System.err.println(e);
        }

    }

    private static void accept() throws Exception {
        socket = new DatagramSocket(port);
        packet = new DatagramPacket(new byte[MAX_SIZE], MAX_SIZE);
        socket.receive(packet);
        host = packet.getAddress();
        socket.send(new DatagramPacket("1".getBytes(StandardCharsets.UTF_8), 1, host, port));
        String path = desktopPath;

        while (true) {
            packet = new DatagramPacket(new byte[MAX_SIZE], MAX_SIZE);
            socket.receive(packet);
            if (getData(packet).equals("$$$end$$$")) break;


            String temp = getData(packet);
            if (temp.equals("$$")) {
                path = new File(path).getParent() + '/';
                socket.send(new DatagramPacket("1".getBytes(StandardCharsets.UTF_8), 1, host, port));
            } else if (temp.charAt(0) == '$') {
                StringBuilder stringBuilder = new StringBuilder();
                for (int loop = 1; temp.charAt(loop) != '$' && loop < temp.length(); loop++)
                    stringBuilder.append(temp.charAt(loop));
                path = path + stringBuilder.toString();
                new File(path).mkdir();
                path = path + '/';
                socket.send(new DatagramPacket("1".getBytes(StandardCharsets.UTF_8), 1, host, port));
            } else {
                ServerSocket TCPServerSocket = new ServerSocket(0);

                socket.send(new DatagramPacket(Integer.toString(TCPServerSocket.getLocalPort()).getBytes(),
                        Integer.toString(TCPServerSocket.getLocalPort()).length(), host, port));
                Socket TCPSocket = TCPServerSocket.accept();
                InputStream DWNInputStream = TCPSocket.getInputStream();
                BufferedInputStream DWNBufferedInputStream = new BufferedInputStream(DWNInputStream);


                FileOutputStream DWNFileOutputStream = new FileOutputStream(path + temp);
                BufferedOutputStream DWNBufferedOutputStream = new BufferedOutputStream(DWNFileOutputStream);

                byte[] DWNBytes = new byte[MAX_SIZE];
                int DWNLength;


                while ((DWNLength = DWNBufferedInputStream.read(DWNBytes)) != -1)
                    DWNBufferedOutputStream.write(DWNBytes, 0,DWNLength);
                DWNBufferedOutputStream.flush();
                DWNFileOutputStream.close();
                TCPServerSocket.close();

                socket.send(new DatagramPacket("1".getBytes(StandardCharsets.UTF_8), 1, host, port));
            }
        }
    }

    private static String getData(DatagramPacket datagramPacket) throws Exception {
        byte[] buf = datagramPacket.getData();
        ByteArrayInputStream bais = new ByteArrayInputStream(buf);
        InputStreamReader isr = new InputStreamReader(bais);
        BufferedReader br = new BufferedReader(isr);
        String temp = br.readLine();
        StringBuilder stringBuilder = new StringBuilder();
        for (int loop = 0; temp.charAt(loop) != '\0'; loop++)
            stringBuilder.append(temp.charAt(loop));
        return stringBuilder.toString();
    }
}
