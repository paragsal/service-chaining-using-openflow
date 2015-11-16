#include<stdlib.h>
#include<string.h>
#include <stdio.h>
#include <sys/socket.h>
#include <netinet/in.h>
#include <netdb.h>
#include <stdlib.h>
#include <sys/types.h>

void string_reverse(char * string_sid)
{

   char temp[100];
   int i =0;
/*   while (string_sid[i] != '\0') {
        
        temp[i] = string_sid[i] ;
        i++;
   }
  temp[i]='\0';
*/

  strcpy(temp, string_sid);

  //printf("%s \n", temp);
  //exit(0);
  i=strlen(temp);
  int j=0;
 
   bzero(string_sid, strlen(temp)+1); 
  //string_sid[strlen(temp)]='\0'; 
  --i; 
  for (j=0;j<strlen(temp); j++) {
     string_sid[i]= temp[j];
     //printf("\n%c", string_sid[i]);
     i--;
  }


/*   i=0;
   for (j=strlen(temp);j>=0; j--) {
      
     string_sid[i]= temp[j];
     i++;

   } 
*/

//  string_sid[i]='\0';
  
  //printf("IN %s\n", string_sid);
  
}

int main(int argc, char**argv)
{

   printf("Main Beg\n");
   int sockfd,n;
   char *Name = "Mahendra";
   struct sockaddr_in servaddr,cliaddr;
   char sendline[1000];
 
   char recvline[1000];
   char ncsu[5]="NCSU";
   long sid = 200107280;
   char string_sid[20];
   char ip[16] ="127.0.0.1";
   char *str1 ="CSC453-001 2015"  ; 

   bzero(sendline, 1000);

   if (argc != 2)
   {
      printf("usage:  %s <IP address>\n",argv[0]);
      exit(1);
   }


   
   sockfd=socket(AF_INET,SOCK_DGRAM,0);

   bzero(&servaddr,sizeof(servaddr));
   servaddr.sin_family = AF_INET;
   servaddr.sin_addr.s_addr=inet_addr(argv[1]);
   servaddr.sin_port=htons(8222);

   
   printf("After assignment\n");

int s;
   struct sockaddr_in sa;
   int sa_len;
   int j;

   sendline[0]= '1';
   sendline[1]= '2';
   sendline[2] = 'E';
   sendline[3] = 'H';

   sendline[4] = 'E';
   sendline[5] = 'I';

/*   for (j=0; j<strlen(Name);j++) {
      sendline[i+j]= Name[j];
   }
   sendline[i+j]='\0';
*/
//i+=j;
  // sendline[i++]='\0';
    
/*   for (j=0; j< strlen(string_sid);j++) {
      sendline[i+j]=string_sid[j];
   }
*/ 
/*   char *ptr = &(sendline[i]);
   memcpy((void *)ptr, (void *)string_sid, strlen(string_sid));  
  
   i+=strlen(string_sid);
*/   
   printf("\nBef\n");
   printf("SEND LINE %s\n", sendline);
   printf("After\n");
      sendto(sockfd,sendline,1000,0,
             (struct sockaddr *)&servaddr,sizeof(servaddr));
      n=recvfrom(sockfd,recvline,10000,0,NULL,NULL);
      recvline[n]=0;
      printf("\n Received from server: \n");
      fputs(recvline,stdout);
      printf("Enter string to send:\n");
}

