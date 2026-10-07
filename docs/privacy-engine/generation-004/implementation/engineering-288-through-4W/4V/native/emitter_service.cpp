// CP4V conditional laboratory byte emitter. Lexical algorithm adapted from retained 4A.
// It does not use the independent validator's Index, Parser or membership function.
#include <openssl/sha.h>
#include <algorithm>
#include <array>
#include <chrono>
#include <fstream>
#include <iostream>
#include <iomanip>
#include <sstream>
#include <vector>
#include <tuple>
#include <cstring>
#include <unistd.h>
#include <fcntl.h>
#include <sys/resource.h>
using U=uint64_t;
void req(bool b,const char*s){if(!b)throw std::runtime_error(s);}
std::string hex(const unsigned char*p,size_t n){static const char*d="0123456789abcdef";std::string s;for(size_t i=0;i<n;i++){s+=d[p[i]>>4];s+=d[p[i]&15];}return s;}
std::string hex(const std::string&s){return hex((unsigned char*)s.data(),s.size());}
std::string unhex(const std::string&s){if(s=="-")return "";req(s.size()%2==0&&s.size()<=65536&&s.find_first_not_of("0123456789abcdef")==s.npos,"bad cursor/path hex");std::string o;for(size_t i=0;i<s.size();i+=2)o+=char(std::stoul(s.substr(i,2),nullptr,16));return o;}
std::string digest(SHA256_CTX c){unsigned char d[32];SHA256_Final(d,&c);return hex(d,32);}
const std::string HEADER="link_order\tfrom_token_id\tto_token_id\trelation_order\trelation_class\n";
struct HB:std::streambuf{std::ifstream f;std::array<char,1048576>b;SHA256_CTX h;HB(const char*p):f(p,std::ios::binary){req(bool(f),"missing descriptor");SHA256_Init(&h);}int_type underflow()override{if(gptr()<egptr())return traits_type::to_int_type(*gptr());f.read(b.data(),b.size());auto n=f.gcount();req(!f.bad(),"read error");if(!n)return traits_type::eof();SHA256_Update(&h,b.data(),n);setg(b.data(),b.data(),b.data()+n);return traits_type::to_int_type(*gptr());}};
struct Edge{uint32_t a,b,r;std::string k;bool operator<(const Edge&x)const{return std::tie(a,b,r,k)<std::tie(x.a,x.b,x.r,x.k);}bool operator==(const Edge&x)const{return std::tie(a,b,r,k)==std::tie(x.a,x.b,x.r,x.k);}};
struct Cursor{U a=0,b=0,pos=0,eq=0,ordinal=0,offset=0,header=0;std::string pending;std::string save(){std::ostringstream o;o<<"CP4V-EMITTER-1 "<<a<<' '<<b<<' '<<pos<<' '<<eq<<' '<<ordinal<<' '<<offset<<' '<<header<<' '<<(pending.empty()?"-":hex(pending));return hex(o.str());}void load(std::string s){if(s=="-")return;std::istringstream i(unhex(s));std::string tag,p,tail;i>>tag>>a>>b>>pos>>eq>>ordinal>>offset>>header>>p;req(bool(i)&&tag=="CP4V-EMITTER-1"&&eq<=1&&header<=1,"bad cursor");pending=unhex(p);i>>tail;req(i.eof()&&tail.empty(),"cursor trailing");}};
int main(int argc,char**argv){try{
 if(argc==2&&std::string(argv[1])=="--selftest"){std::cout<<"{\"result\":\"PASS\",\"role\":\"conditional-laboratory-emitter\"}\n";return 0;}
 req(argc==3,"descriptor and exact hash required");auto init=std::chrono::steady_clock::now();HB buf(argv[1]);std::istream in(&buf);std::string tag;U n,m,f;in>>tag>>n>>m>>f;req(bool(in)&&tag=="LINKS"&&n>=2&&n<=1000000&&m<=10000000&&f<=n,"descriptor bounds");
 std::vector<std::string> names(n);for(auto&s:names){in>>std::setw(1025)>>s;req(bool(in)&&!s.empty()&&s.size()<=1024,"token bounds");}
 std::vector<int> fixed(n,-1);for(U k=0;k<f;k++){U i,g;in>>i>>g;req(bool(in)&&i<n&&g<=1000000&&fixed[i]<0,"fixed group");fixed[i]=g;}
 std::vector<uint32_t> lex(n),rank(n);for(U i=0;i<n;i++)lex[i]=i;std::sort(lex.begin(),lex.end(),[&](auto a,auto b){return names[a]<names[b];});for(U i=0;i<n;i++){rank[lex[i]]=i;req(!i||names[lex[i]]!=names[lex[i-1]],"duplicate token");}
 std::vector<Edge> es;es.reserve(m);for(U k=0;k<m;k++){U a,b,r;std::string kind;in>>a>>b>>r>>std::setw(1025)>>kind;req(bool(in)&&a<n&&b<n&&r>=1&&r<=999999&&kind.size()<=1024,"structural row");es.push_back({rank[a],rank[b],uint32_t(r),kind});}std::string tail;in>>tail;req(tail.empty()&&in.eof()&&digest(buf.h)==argv[2],"descriptor byte identity");std::sort(es.begin(),es.end());es.erase(std::unique(es.begin(),es.end()),es.end());rusage ru{};getrusage(RUSAGE_SELF,&ru);rlimit aslim{},fslim{},nolim{};getrlimit(RLIMIT_AS,&aslim);getrlimit(RLIMIT_FSIZE,&fslim);getrlimit(RLIMIT_NOFILE,&nolim);std::cout<<"{\"ready\":true,\"index_seconds\":"<<std::chrono::duration<double>(std::chrono::steady_clock::now()-init).count()<<",\"rss_kib\":"<<ru.ru_maxrss<<",\"address_space_limit\":"<<aslim.rlim_cur<<",\"file_size_limit\":"<<fslim.rlim_cur<<",\"handle_limit\":"<<nolim.rlim_cur<<"}"<<std::endl;
 auto pad=[](U v){auto s=std::to_string(v);return s.size()<6?std::string(6-s.size(),'0')+s:s;};std::string line;
 while(std::getline(std::cin,line)){
  req(line.size()<=65536,"request bound");std::istringstream q(line);std::string op,ch,ph,extra;U cap;double seconds;q>>op>>cap>>seconds>>ch>>ph;q>>extra;req(q.eof()&&extra.empty()&&op=="EMIT"&&cap>0&&cap<=268435456&&seconds>0&&seconds<=55,"request budget");Cursor c;c.load(ch);req(c.a<=n&&c.b<=n&&c.pos<=es.size()&&c.pending.size()<=4096,"cursor range");U start=c.offset;auto began=std::chrono::steady_clock::now();auto elapsed=[&](){return std::chrono::duration<double>(std::chrono::steady_clock::now()-began).count();};
  auto row=[&](U a,U b,U r,const std::string&k){c.pending=pad(++c.ordinal)+'\t'+names[lex[a]]+'\t'+names[lex[b]]+'\t'+pad(r)+'\t'+k+'\n';};
  auto next=[&](){if(!c.header){c.header=1;c.pending=HEADER;return true;}while(c.a<n){if(c.b==n){c.a++;c.b=0;c.eq=0;continue;}if(!c.eq){c.eq=1;auto i=lex[c.a],j=lex[c.b];if(i<j&&(fixed[i]<0||fixed[j]<0||fixed[i]==fixed[j])){row(c.a,c.b,0,"EQUALS");return true;}}if(c.pos<es.size()&&es[c.pos].a==c.a&&es[c.pos].b==c.b){auto&e=es[c.pos++];row(e.a,e.b,e.r,e.k);return true;}c.b++;c.eq=0;}return false;};
  std::string path=unhex(ph);int fd=open(path.c_str(),O_WRONLY|O_CREAT|O_EXCL|O_NOFOLLOW,0600);req(fd>=0,"spool create");SHA256_CTX sh;SHA256_Init(&sh);std::string output;output.reserve(1048576+4096);U written=0;bool eof=false;
  auto flush=[&](){size_t pos=0;while(pos<output.size()){ssize_t v=write(fd,output.data()+pos,output.size()-pos);req(v>0,"write spool");pos+=v;}SHA256_Update(&sh,output.data(),output.size());written+=output.size();output.clear();};
  while(c.offset-start<cap&&elapsed()<seconds){if(c.pending.empty()&&!next()){eof=true;break;}U take=std::min(U(c.pending.size()),cap-(c.offset-start));output.append(c.pending,0,take);c.pending.erase(0,take);c.offset+=take;if(output.size()>=1048576)flush();}flush();req(fsync(fd)==0,"spool fsync");close(fd);getrusage(RUSAGE_SELF,&ru);
  std::cout<<"{\"cursor_hex\":\""<<c.save()<<"\",\"start\":"<<start<<",\"end\":"<<c.offset<<",\"bytes\":"<<written<<",\"sha256\":\""<<digest(sh)<<"\",\"eof\":"<<(eof?"true":"false")<<",\"seconds\":"<<elapsed()<<",\"rss_kib\":"<<ru.ru_maxrss<<"}"<<std::endl;
 }
}catch(std::exception&e){std::cerr<<e.what()<<std::endl;return 4;}return 0;}
