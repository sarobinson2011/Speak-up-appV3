// Supplied static links only. No potential-pair generator, replay, or row store.
#include <openssl/sha.h>
#include <algorithm>
#include <array>
#include <chrono>
#include <cmath>
#include <cstring>
#include <fstream>
#include <iomanip>
#include <iostream>
#include <sstream>
#include <stdexcept>
#include <string_view>
#include <unordered_map>
#include <vector>
#include <sys/resource.h>
using U=uint64_t;
const std::string HEADER="link_order\tfrom_token_id\tto_token_id\trelation_order\trelation_class\n";
struct Failure:std::runtime_error {std::string code;Failure(std::string c,std::string s):runtime_error(s),code(c){}};
void need(bool ok,const char*msg,const char*code="INVALID-PROFILE-SCHEMA"){if(!ok)throw Failure(code,msg);}
std::string hash(SHA256_CTX c){unsigned char d[32];SHA256_Final(d,&c);std::ostringstream o;o<<std::hex<<std::setfill('0');for(auto b:d)o<<std::setw(2)<<unsigned(b);return o.str();}
bool id(std::string_view s){auto al=[](unsigned char c){return (c>='a'&&c<='z')||(c>='A'&&c<='Z')||(c>='0'&&c<='9');};if(s.empty()||!al(s[0]))return false;for(auto c:s)if(!al(c)&&c!='.'&&c!='_'&&c!=':'&&c!='#'&&c!='-')return false;return true;}
bool model_id(std::string_view s){if(s.empty())return false;for(unsigned char c:s)if(c<33||c>126)return false;return true;}
bool digest(std::string_view s){return s.size()==64&&s.find_first_not_of("0123456789abcdef")==s.npos;}
std::string ordinal(U n){auto s=std::to_string(n);return s.size()<6?std::string(6-s.size(),'0')+s:s;}
// Hash the same descriptor bytes parsed, through one open stream: no hash/reopen gap.
struct HashBuf:std::streambuf {
 std::ifstream file;std::vector<char> b;SHA256_CTX ctx;U bytes=0;
 HashBuf(const char*path):file(path,std::ios::binary),b(1048576){need(bool(file),"descriptor missing","MISSING-EVIDENCE");SHA256_Init(&ctx);}
 int_type underflow() override {if(gptr()<egptr())return traits_type::to_int_type(*gptr());file.read(b.data(),b.size());auto n=file.gcount();need(!file.bad(),"descriptor read error","MISSING-EVIDENCE");if(!n)return traits_type::eof();SHA256_Update(&ctx,b.data(),n);bytes+=n;setg(b.data(),b.data(),b.data()+n);return traits_type::to_int_type(*gptr());}
};
struct Edge{uint32_t a,b,r;std::string k;bool operator<(const Edge&e)const{return std::tie(a,b,r,k)<std::tie(e.a,e.b,e.r,e.k);}bool operator==(const Edge&e)const{return a==e.a&&b==e.b&&r==e.r&&k==e.k;}};
struct Index {
 std::unordered_map<std::string,uint32_t> ids;std::vector<int> fixed;std::vector<Edge> edges;U potential=0,expected=0,n=0;size_t maxline=0;std::string descriptor_hash;
 Index(const char*path,const std::string&expected_hash){
  HashBuf buf(path);std::istream in(&buf);std::string tag;U m,f;in>>tag>>n>>m>>f;
  need(bool(in)&&tag=="LINKS"&&n>=2&&n<=1000000&&m<=10000000&&f<=n,"descriptor shape or local model index budget");
  auto word=[&](){std::string s;in>>std::setw(1025)>>s;need(bool(in)&&s.size()<=1024&&model_id(s),"descriptor identifier or local 1024-byte budget");return s;};
  size_t longest=0,maxkind=6;ids.reserve(n*2);fixed.assign(n,-1);
  for(U i=0;i<n;i++){auto s=word();longest=std::max(longest,s.size());need(ids.emplace(s,i).second,"duplicate model token id");}
  std::unordered_map<int,U> groups;
  for(U k=0;k<f;k++){U i,g;in>>i>>g;need(bool(in)&&i<n&&g<=1000000&&fixed[i]==-1,"fixed token group");fixed[i]=g;groups[g]++;}
  edges.reserve(m);
  for(U k=0;k<m;k++){U a,b,r;in>>a>>b>>r;need(bool(in)&&a<n&&b<n&&r>=1&&r<=999999,"model structural domain");auto kind=word();maxkind=std::max(maxkind,kind.size());edges.push_back({uint32_t(a),uint32_t(b),uint32_t(r),kind});}
  std::string trailing;in>>std::setw(1)>>trailing;need(trailing.empty()&&in.eof(),"descriptor trailing bytes");descriptor_hash=hash(buf.ctx);need(digest(expected_hash)&&descriptor_hash==expected_hash,"complete model descriptor digest mismatch","INVALID-EVIDENCE-DIGEST");
  std::sort(edges.begin(),edges.end());edges.erase(std::unique(edges.begin(),edges.end()),edges.end());
  potential=n*(n-1)/2-f*(f-1)/2;for(auto [g,c]:groups)potential+=c*(c-1)/2;expected=potential+edges.size();maxline=std::max(HEADER.size()-1,ordinal(std::max(U(1),expected)).size()+2*longest+6+maxkind+4);
 }
};
struct Parser {
 const Index&index;bool header=false;U rows=0,structural=0,potential=0;std::array<std::string,4> previous;bool have=false;
 Parser(const Index&i):index(i){}
 void line(std::string_view line){
  if(!header){need(line==std::string_view(HEADER).substr(0,HEADER.size()-1),"exact LINK_HEADER / UTF-8 no BOM");header=true;return;}
  std::array<std::string_view,5> c;size_t start=0;
  for(int k=0;k<5;k++){auto p=line.find('\t',start);if(k<4){need(p!=line.npos,"five cells required");c[k]=line.substr(start,p-start);start=p+1;}else{need(p==line.npos,"five cells required");c[k]=line.substr(start);}}
  need(model_id(c[1])&&model_id(c[2])&&id(c[4]),"canonical ASCII IDs / no CR, BOM or whitespace");need(c[3].size()==6&&c[3].find_first_not_of("0123456789")==c[3].npos,"closed relation ORD6");need(c[0]==ordinal(rows+1),"contiguous minimum-width link ordinal");
  std::array<std::string,4> current{std::string(c[1]),std::string(c[2]),std::string(c[3]),std::string(c[4])};need(!have||previous<current,"strict lexical four-cell order / uniqueness");
  auto a=index.ids.find(current[0]),b=index.ids.find(current[1]);need(a!=index.ids.end()&&b!=index.ids.end(),"orphan endpoint","INCOMPLETE-EVIDENCE-UNIVERSE");
  uint32_t r=0;for(char x:c[3])r=r*10+x-'0';
  if(!r){need(c[4]=="EQUALS","zero order requires EQUALS");need(a->second<b->second,"potential orientation i<j","INCOMPLETE-EVIDENCE-UNIVERSE");int x=index.fixed[a->second],y=index.fixed[b->second];need(x<0||y<0||x==y,"illegal potential membership","INCOMPLETE-EVIDENCE-UNIVERSE");potential++;}
  else {Edge e{a->second,b->second,r,current[3]};need(std::binary_search(index.edges.begin(),index.edges.end(),e),"structural relation/provenance membership","INCOMPLETE-EVIDENCE-UNIVERSE");structural++;}
  rows++;previous=std::move(current);have=true;need(structural<=index.edges.size()&&potential<=index.potential,"separate count overflow","INCOMPLETE-EVIDENCE-UNIVERSE");
 }
 void finish(){need(header,"missing LINK_HEADER");need(structural==index.edges.size(),"missing structural rows","INCOMPLETE-EVIDENCE-UNIVERSE");need(potential==index.potential,"missing potential rows","INCOMPLETE-EVIDENCE-UNIVERSE");}
};
int main(int argc,char**argv){
 auto began=std::chrono::steady_clock::now();SHA256_CTX input;SHA256_Init(&input);U consumed=0;bool eof=false,complete=false;std::string code,detail,desc_hash;U rows=0,srows=0,prows=0,sexpected=0,pexpected=0;size_t peak=0,chunk_size=0;double index_seconds=0;U n=0;
 try {
  need(argc==8,"usage: native descriptor descriptor-sha256 input-or-stdin expected-input-sha256-or-NONE chunk-bytes max-bytes seconds");
  chunk_size=std::stoull(argv[5]);U maxbytes=std::stoull(argv[6]);double seconds=std::stod(argv[7]);need(chunk_size>0&&chunk_size<=1048576&&maxbytes>0&&seconds>0&&std::isfinite(seconds),"local bounded read/time limits");
  Index index(argv[1],argv[2]);desc_hash=index.descriptor_hash;n=index.n;sexpected=index.edges.size();pexpected=index.potential;index_seconds=std::chrono::duration<double>(std::chrono::steady_clock::now()-began).count();
  Parser parser(index);std::ifstream file;if(std::string(argv[3])!="-"){file.open(argv[3],std::ios::binary);need(bool(file),"supplied input missing","MISSING-EVIDENCE");}std::istream&stream=std::string(argv[3])=="-"?std::cin:file;
  std::string expected=argv[4];need(expected=="NONE"||digest(expected),"expected input digest shape");std::vector<char> chunk(chunk_size);std::string pending;pending.reserve(index.maxline);double last=0;
  try {
   while(true){double elapsed=std::chrono::duration<double>(std::chrono::steady_clock::now()-began).count();need(elapsed<seconds,"local deadline; no complete digest","RESOURCE-LIMIT");need(consumed<maxbytes,"local byte budget; EOF not observed","RESOURCE-LIMIT");
    auto take=std::min(U(chunk_size),maxbytes-consumed);stream.read(chunk.data(),take);auto got=stream.gcount();need(!stream.bad(),"supplied stream I/O failure","MISSING-EVIDENCE");if(!got){eof=true;break;}
    SHA256_Update(&input,chunk.data(),got);consumed+=got;size_t start=0;
    while(start<size_t(got)){auto p=(char*)memchr(chunk.data()+start,'\n',got-start);size_t end=p?size_t(p-chunk.data()):got;need(pending.size()+end-start<=index.maxline,"row exceeds maximum legal size in this bound model");pending.append(chunk.data()+start,end-start);peak=std::max(peak,pending.size());if(!p)break;parser.line(pending);pending.clear();start=end+1;}
    if(elapsed-last>=10){std::cerr<<"{\"bytes_consumed\":"<<consumed<<",\"rows_validated\":"<<parser.rows<<",\"seconds\":"<<elapsed<<"}\n";last=elapsed;}
   }
   need(pending.empty(),"truncated row: terminal LF required");parser.finish();need(expected=="NONE"||hash(input)==expected,"exact consumed input digest mismatch","INVALID-EVIDENCE-DIGEST");complete=true;
  }catch(Failure&e){code=e.code;detail=e.what();}
  rows=parser.rows;srows=parser.structural;prows=parser.potential;
 }catch(Failure&e){code=e.code;detail=e.what();}catch(std::exception&e){code="INVALID-PROFILE-SCHEMA";detail="invalid arguments or local I/O/resource failure";}
 auto elapsed=std::chrono::duration<double>(std::chrono::steady_clock::now()-began).count();rusage usage{};getrusage(RUSAGE_SELF,&usage);
 std::cout<<"{\"result\":\""<<(complete?"PASS-SUPPLIED-LINK-STREAM":"REJECTED")<<"\",\"complete\":"<<(complete?"true":"false")<<",\"eof_observed\":"<<(eof?"true":"false")<<",\"bytes_consumed\":"<<consumed<<",\"consumed_sha256\":\""<<hash(input)<<"\",\"complete_stream_sha256\":"<<(complete?"\""+hash(input)+"\"":"null")<<",\"rows_validated\":"<<rows<<",\"structural_rows\":"<<srows<<",\"potential_rows\":"<<prows<<",\"expected_structural_rows\":"<<sexpected<<",\"expected_potential_rows\":"<<pexpected<<",\"model_tokens\":"<<n<<",\"descriptor_sha256\":\""<<desc_hash<<"\",\"peak_pending_line_bytes\":"<<peak<<",\"chunk_bytes\":"<<chunk_size<<",\"peak_rss_kib\":"<<usage.ru_maxrss<<",\"seconds\":"<<elapsed<<",\"index_seconds\":"<<index_seconds<<",\"failure\":";
 if(complete)std::cout<<"null";else std::cout<<"{\"code\":\""<<code<<"\",\"detail\":\""<<detail<<"\"}";
 std::cout<<",\"profile_admitted\":false,\"actual_qualification_established\":false}\n";return complete?0:2;
}
