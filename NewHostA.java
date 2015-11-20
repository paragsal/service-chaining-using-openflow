import java.awt.image.BufferedImage;
import java.io.*; 
import java.net.*;
import java.util.Scanner;

import javax.imageio.ImageIO;

public class NewHostA 
{
	private static byte[] as;
	private static Scanner in;
	
	public static void main(String[] args) throws Exception 
	{	   
			
		Socket HostASocket = new Socket("127.0.0.1", 1409); 

	    DataOutputStream ToHostB = 
	    new DataOutputStream(HostASocket.getOutputStream()); 
	        
	    BufferedReader FromHostB = 
	    new BufferedReader(new
	    InputStreamReader(HostASocket.getInputStream())); 
		
	       
		BufferedImage image = null;
		in = new Scanner(System.in);
		System.out.println("Enter the path of image: ");
		String s = in.nextLine();
		    
		image = ImageIO.read(new File(s));
			
		ImageIO.write(image, "jpg", ToHostB);
			    
				
		//	String messageFromB; 
		//	messageFromB = FromHostB.readLine();
		//	System.out.println("Message from Server: "+ messageFromB+".");
		HostASocket.close(); 
		                   
	} 
		

}
	

