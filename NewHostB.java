import java.awt.image.BufferedImage;
import java.io.*; 
import java.net.*;

import javax.imageio.ImageIO;
import javax.swing.ImageIcon;
import javax.swing.JFrame;
import javax.swing.JLabel; 
import java.awt.Graphics2D;

class NewHostB { 

	private static byte[] recoveredData;
	private static ServerSocket HostBSocket;
	public static void main(String argv[]) throws IOException 
    
	{ 
	        
		HostBSocket = new ServerSocket(1409); 
  
		while(true) 
		{ 
  
        Socket SocketWithA = HostBSocket.accept(); 

        DataInputStream FromHostA = 
        new DataInputStream(SocketWithA.getInputStream()); 

        DataOutputStream ToHostA = 
        new DataOutputStream(SocketWithA.getOutputStream()); 

                  
           
        BufferedImage recoveredImage ;
       		
       		
       	recoveredImage = ImageIO.read(ImageIO.createImageInputStream(FromHostA));

       	ImageIO.write(recoveredImage, "jpg", new File("newImageAtB.jpg"));
  		//String msg;
		//msg = "Received modified image at HostB + '\n'";
		//ToHostA.writeBytes(msg);     		
		
		BufferedImage newimg = new BufferedImage (1000,1000, recoveredImage.getType());
		Graphics2D graph = newimg.createGraphics();
		graph.drawImage(recoveredImage,0,0,1000,1000,0,0,recoveredImage.getWidth(), recoveredImage.getHeight(),null);
		graph.dispose();
       	ImageIcon icon = new ImageIcon(newimg);
       	JLabel label = new JLabel(icon);
       	JFrame frame = new JFrame();
       	frame.add(label);
       	frame.setDefaultCloseOperation
       	(JFrame.EXIT_ON_CLOSE);
       	frame.pack();
       	frame.setVisible(true);
 
        } 
    } 
} 
 
