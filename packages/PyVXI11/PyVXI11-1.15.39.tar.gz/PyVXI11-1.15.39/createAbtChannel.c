//
// 
//
#include <string.h>
#include <sys/types.h>
#include <rpc/rpc.h>
#include "VXI11.h"
#include <netinet/in.h>
#include <arpa/inet.h>
#include <rpc/svc.h>
#include <rpc/clnt.h>
#include <rpc/xdr.h>
#include <netdb.h>

CLIENT *createAbtChannel(char *clnt, u_short abortPort,
			 int *sockp, /* return value */
			 u_int prog, u_int version, 
			 u_int sendsz, u_int recvsz)
{
        struct sockaddr_in addr;
        struct hostent *he;
        CLIENT *retv;
        int     sock = RPC_ANYSOCK;
               

        bzero( &addr, sizeof(addr));
        addr.sin_family=AF_INET;
        addr.sin_port = htons(abortPort);
	
	/* { */
	/* 	int ret; */
	/* 	struct addrinfo *aip; */
	/* 	ret=getaddrinfo(clnt,NULL,NULL,&aip); */
	/* 	inet_aton(aip->ai_canonname, &addr.sin_addr); */
	/* } */
	
        /* follow http://www-cms.phys.s.u-tokyo.ac.jp/~naoki/CIPINTRO/NETWORK/struct.html to setup addr*/
	he=gethostbyname(clnt);
        inet_aton(he->h_addr_list[0], &addr.sin_addr);

        retv=clnttcp_create(&addr, 
                            prog, version,
                            &sock,
                            sendsz, recvsz);
        if (retv){
                *sockp=sock;
        }
        else{
		clnt_pcreateerror(__FILE__);
                *sockp=-1;
	}
        return retv;
}
