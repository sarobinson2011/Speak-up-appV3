// Exact binary stream engine. OpenSSL supplies SHA-256, never a predicate digest.
#include <openssl/sha.h>
#include <algorithm>
#include <chrono>
#include <cstring>
#include <fstream>
#include <iomanip>
#include <iostream>
#include <sstream>
#include <stdexcept>
#include <vector>
using U=uint64_t;
std::string hex(const unsigned char*p,size_t n){std::ostringstream o;o<<std::hex<<std::setfill('0');for(size_t i=0;i<n;i++)o<<std::setw(2)<<unsigned(p[i]);return o.str();}
std::vector<unsigned char> unhex(std::string s){if(s.size()%2)throw std::runtime_error("hex");std::vector<unsigned char> b;for(size_t i=0;i<s.size();i+=2){auto z=s.substr(i,2);if(z.find_first_not_of("0123456789abcdef")!=std::string::npos)throw std::runtime_error("hex");b.push_back(std::stoul(z,nullptr,16));}return b;}
std::string state(SHA256_CTX c){std::ostringstream o;o<<std::hex<<std::setfill('0');for(auto h:c.h)o<<std::setw(8)<<h;o<<":"<<std::dec<<((U(c.Nh)<<32|c.Nl)/8)<<":"<<hex((unsigned char*)c.data,c.num);return o.str();}
SHA256_CTX restore(std::string s){SHA256_CTX c;SHA256_Init(&c);auto a=s.find(':'),b=s.find(':',a+1);if(a!=64||b==std::string::npos)throw std::runtime_error("state shape");auto tail=unhex(s.substr(b+1));U n=std::stoull(s.substr(a+1,b-a-1));if(n>UINT64_MAX/8||tail.size()!=n%64)throw std::runtime_error("state length");for(int i=0;i<8;i++){auto v=unhex(s.substr(i*8,8));c.h[i]=(unsigned(v[0])<<24)|(unsigned(v[1])<<16)|(unsigned(v[2])<<8)|v[3];}c.Nl=unsigned(n*8);c.Nh=unsigned(n>>29);c.num=tail.size();memset(c.data,0,sizeof(c.data));memcpy(c.data,tail.data(),tail.size());return c;}
std::string finish(SHA256_CTX c){unsigned char b[32];SHA256_Final(b,&c);return hex(b,32);}
U rank0(U n,U i){return i*(2*n-i-1)/2;}
int main(int argc,char**argv){try{
 if(argc!=7)throw std::runtime_error("pairs descriptor start end state-or-INIT engine max-seconds");
 auto began=std::chrono::steady_clock::now();double limit=std::stod(argv[6]);if(!(limit>0&&limit<=60))throw std::runtime_error("hard 60-second cap");
 std::ifstream in(argv[1]);U n,m;in>>n>>m;if(!in||n<2||n>UINT32_MAX||m>n)throw std::runtime_error("descriptor bounds");std::vector<int> fixed(n,-1);std::vector<U> ids;for(U x=0;x<m;x++){U i;int g;in>>i>>g;if(!in||i>=n||g<0||fixed[i]!=-1)throw std::runtime_error("descriptor fixed group");fixed[i]=g;ids.push_back(i);}std::string extra;if(in>>extra)throw std::runtime_error("descriptor trailing");
 U start=std::stoull(argv[2]),end=std::stoull(argv[3]),total=n*(n-1)/2;if(start>=end||end>total)throw std::runtime_error("range");std::string engine=argv[5];if(engine!="complement"&&engine!="predicate")throw std::runtime_error("engine");
 std::vector<U> excluded;for(auto i:ids)for(auto j:ids)if(i<j&&fixed[i]!=fixed[j])excluded.push_back(rank0(n,i)+j-i-1);std::sort(excluded.begin(),excluded.end());
 SHA256_CTX cumulative,segment;SHA256_Init(&segment);if(std::string(argv[4])=="INIT"){SHA256_Init(&cumulative);const char*h="PE-G4-POTENTIAL-EQUALITY-PAIRS-V1\n";SHA256_Update(&cumulative,h,strlen(h));}else cumulative=restore(argv[4]);std::string before=state(cumulative);
 U lo=0,hi=n-1;while(lo+1<hi){U mid=(lo+hi)/2;if(rank0(n,mid)<=start)lo=mid;else hi=mid;}U i=lo,j=i+1+start-rank0(n,i),rows=0;size_t ex=std::lower_bound(excluded.begin(),excluded.end(),start)-excluded.begin();
 std::vector<unsigned char> buf(8*1024*1024);size_t used=0;double last=0;
 auto flush=[&](){SHA256_Update(&segment,buf.data(),used);SHA256_Update(&cumulative,buf.data(),used);used=0;double sec=std::chrono::duration<double>(std::chrono::steady_clock::now()-began).count();if(sec>limit)throw std::runtime_error("time budget; uncommitted segment discarded");if(sec-last>=10){std::cerr<<"{\"rows\":"<<rows<<",\"seconds\":"<<sec<<"}\n";last=sec;}};
 for(U r=start;r<end;r++){
  bool accept;if(engine=="predicate")accept=fixed[i]<0||fixed[j]<0||fixed[i]==fixed[j];else{accept=ex==excluded.size()||excluded[ex]!=r;if(!accept)ex++;}
  if(accept){uint32_t a=i,b=j;for(int k=3;k>=0;k--)buf[used++]=(a>>(8*k))&255;for(int k=3;k>=0;k--)buf[used++]=(b>>(8*k))&255;rows++;if(used==buf.size())flush();}
  if(++j==n){++i;j=i+1;}
 }flush();double sec=std::chrono::duration<double>(std::chrono::steady_clock::now()-began).count();
 std::cout<<"{\"start\":"<<start<<",\"end\":"<<end<<",\"rows\":"<<rows<<",\"bytes\":"<<rows*8<<",\"segment_sha256\":\""<<finish(segment)<<"\",\"prefix_sha256\":\""<<finish(cumulative)<<"\",\"state_in\":\""<<before<<"\",\"state_out\":\""<<state(cumulative)<<"\",\"engine\":\""<<engine<<"\",\"seconds\":"<<std::setprecision(12)<<sec<<"}\n";
}catch(std::exception&e){std::cerr<<e.what()<<"\n";return 2;}}
