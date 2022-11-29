import java.io.*;
import java.net.*;
import java.nio.charset.StandardCharsets;
import java.util.*;

public class Send {
    private static InetAddress host;
    private static int port;
    private static DatagramSocket socket;
    private static DatagramPacket packet;
    private static final int MAX_SIZE = 1500;
    private static Scanner scanner = new Scanner(System.in);
    private static int os = 0;

    public static void main(String[] args) throws Exception {

        if (args.length != 2) {
            System.exit(1);
        }
        host = InetAddress.getByName(args[0]);
        port = Integer.parseInt(args[1]);

        if (System.getProperty("os.name").equals("Mac OS X")) os = 1;
        else if (System.getProperty("os.name").equals("Windows 11")) os = 2;

        try {
            send();
        } catch (Exception e) {
            System.err.println(e);
        }
    }


    private static void send() throws Exception {
        socket = new DatagramSocket(port);
        socket.send(new DatagramPacket("$$$start$$$".getBytes(StandardCharsets.UTF_8), "$$$start$$$".length(), host, port));
        packet = new DatagramPacket(new byte[MAX_SIZE], MAX_SIZE);
        socket.receive(packet);
        ArrayList<String> pathList = getSendFileList(scanner.nextLine());
        for (String path : pathList) {
            if (new File(path).isDirectory()) {
                sendDir(new File(path).getAbsolutePath());
            } else {
                sendSingleFile(new File(path).getAbsolutePath());
            }
        }
        socket.send(new DatagramPacket("$$$end$$$".getBytes(StandardCharsets.UTF_8), "$$$end$$$".length(), host, port));
    }

    private static void sendDir(String path) throws Exception {
        File[] dirList = new File(path).listFiles();
        String tempSend = '$' + new File(path).getName() + '$';
        socket.send(new DatagramPacket(tempSend.getBytes(StandardCharsets.UTF_8), tempSend.length(), host, port));
        socket.receive(packet);
        for (int loop = 0; loop < dirList.length; loop++) {
            File temp = dirList[loop];
            if (temp.isDirectory()) sendDir(temp.getAbsolutePath());
            else sendSingleFile(temp.getAbsolutePath());
        }
        socket.send(new DatagramPacket("$$".getBytes(StandardCharsets.UTF_8), 2, host, port));
        socket.receive(packet);
    }

    private static void sendSingleFile(String path) throws Exception {
        File f = new File(path);
        String filename = f.getName();
        socket.send(new DatagramPacket(filename.getBytes(StandardCharsets.UTF_8), filename.length(), host, port));
        packet = new DatagramPacket(new byte[MAX_SIZE], MAX_SIZE);
        socket.receive(packet);

        int TCPPort = Integer.parseInt(getData(packet));
        Socket socketTCP = new Socket(host, TCPPort);
        BufferedInputStream bufferedInputStream = new BufferedInputStream(new FileInputStream(path));
        byte[] bytes = new byte[MAX_SIZE];
        int length;
        OutputStream outputStream = socketTCP.getOutputStream();
        BufferedOutputStream bufferedOutputStream = new BufferedOutputStream(outputStream);
        while ((length = bufferedInputStream.read(bytes)) != -1)
            bufferedOutputStream.write(bytes, 0,length);
        bufferedOutputStream.flush();
        socketTCP.shutdownOutput();

        socketTCP.close();
        bufferedInputStream.close();

        socket.receive(packet);
    }

    private static ArrayList<String> getSendFileList(String p) {
        ArrayList<String> list = new ArrayList<>();
        StringBuilder stringBuilder = new StringBuilder();
        if (os == 1) {
            for (int loop = 0; loop < p.length(); loop++) {
                if (p.charAt(loop) == '\\') continue;
                if ((p.charAt(loop) == ' ' && loop - 1 >= 0 && p.charAt(loop - 1) != '\\')) {
                    list.add(stringBuilder.toString());
                    stringBuilder.delete(0, stringBuilder.length());
                } else if (loop == p.length() - 1) {
                    stringBuilder.append(p.charAt(loop));
                    list.add(stringBuilder.toString());
                } else  {
                    stringBuilder.append(p.charAt(loop));
                }
            }
        } else if (os == 2) {
            int status = 0;
            for (int loop = 0; loop < p.length(); loop++) {
                if (status == 0 && p.charAt(loop) == '\"') {
                    status = 1;
                } else if (status == 1 && p.charAt(loop) == '\"') {
                    list.add(stringBuilder.toString());
                    stringBuilder.delete(0, stringBuilder.length());
                    status = 0;
                    loop++;
                } else if (status == 0 && p.charAt(loop) == ' ') {
                    list.add(stringBuilder.toString());
                    stringBuilder.delete(0, stringBuilder.length());
                } else if (loop == p.length() - 1) {
                    stringBuilder.append(p.charAt(loop));
                    list.add(stringBuilder.toString());
                } else stringBuilder.append(p.charAt(loop));
            }
        }
        return list;
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
