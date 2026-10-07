// Reuse the exact CP4B membership, ordering, framing and completeness rules.
#define main cp4b_legacy_main
#include "../link_stream/native.cpp"
#undef main
#include <unistd.h>
#include <signal.h>
#include <cerrno>
#include <openssl/crypto.h>

volatile sig_atomic_t pause_requested=0;
void pause_signal(int){pause_requested=1;}
std::string hexbytes(const unsigned char* p,size_t n){
 static const char* digits="0123456789abcdef";std::string s;
 for(size_t i=0;i<n;i++){s+=digits[p[i]>>4];s+=digits[p[i]&15];}return s;
}
std::string hexstr(const std::string&s){return hexbytes((const unsigned char*)s.data(),s.size());}
std::string unhex(std::string s){
 if(s=="-")return "";
 need(s.size()%2==0&&s.find_first_not_of("0123456789abcdef")==s.npos,"invalid checkpoint hex","INVALID-CHECKPOINT");
 std::string out;for(size_t i=0;i<s.size();i+=2)out+=char(std::stoul(s.substr(i,2),nullptr,16));return out;
}
// The controller authenticates the snapshot. This worker is not an admission API.
int main(int argc,char**argv){
 try{
  need(argc==9,"worker descriptor sha fd expected-sha chunk new-byte-budget seconds state-in-or-NONE");
  auto began=std::chrono::steady_clock::now();auto elapsed=[&](){return std::chrono::duration<double>(std::chrono::steady_clock::now()-began).count();};
  const size_t chunk_size=std::stoull(argv[5]);const U budget=std::stoull(argv[6]);const double seconds=std::stod(argv[7]);
  need(chunk_size>0&&chunk_size<=1048576&&budget>0&&seconds>0&&std::isfinite(seconds),"invalid local budgets");
  need(digest(argv[4]),"whole-file expected SHA-256 required");int fd=std::stoi(argv[3]);
  Index index(argv[1],argv[2]);Parser parser(index);SHA256_CTX ctx;SHA256_Init(&ctx);
  U consumed=0;size_t peak=0;std::string pending;
  if(std::string(argv[8])!="NONE"){
   std::ifstream saved(argv[8]);std::string version,block,part,expected_prefix;unsigned header,have;
   saved>>version>>consumed>>parser.rows>>parser.structural>>parser.potential>>header>>have>>peak;
   need(bool(saved)&&version=="CP4C-SHA256-1"&&header<=1&&have<=1,"state shape","INVALID-CHECKPOINT");
   parser.header=header;parser.have=have;
   for(int i=0;i<8;i++){U x;saved>>x;need(bool(saved)&&x<=UINT32_MAX,"SHA chaining word","INVALID-CHECKPOINT");ctx.h[i]=x;}
   saved>>block>>part;block=unhex(block);pending=unhex(part);
   for(auto&s:parser.previous){std::string t;saved>>t;s=unhex(t);}
   saved>>expected_prefix;std::string tail;saved>>tail;
   need(saved.eof()&&tail.empty()&&digest(expected_prefix),"state tail","INVALID-CHECKPOINT");
   need(consumed<=UINT64_MAX/8&&block.size()==consumed%64,"SHA length/block mismatch","INVALID-CHECKPOINT");
   ctx.Nl=uint32_t(consumed<<3);ctx.Nh=uint32_t(consumed>>29);ctx.num=block.size();
   std::memset(ctx.data,0,sizeof(ctx.data));std::memcpy(ctx.data,block.data(),block.size());
   need(hash(ctx)==expected_prefix,"SHA state identity","INVALID-CHECKPOINT");
   need(parser.rows==parser.structural+parser.potential&&parser.structural<=index.edges.size()&&parser.potential<=index.potential,"state count invariant","INVALID-CHECKPOINT");
   need(parser.have==(parser.rows!=0)&&(!parser.rows||parser.header)&&pending.size()<=index.maxline&&peak<=index.maxline,"parser state invariant","INVALID-CHECKPOINT");
   need(pending.find('\n')==pending.npos,"pending row contains LF","INVALID-CHECKPOINT");
  }
  need(lseek(fd,consumed,SEEK_SET)==off_t(consumed),"input seek failed","MISSING-EVIDENCE");
  signal(SIGTERM,pause_signal);signal(SIGINT,pause_signal);
  const U original=consumed;bool eof=false,complete=false;std::string code,detail;double last=0;
  std::vector<char> chunk(chunk_size);
  try{
   while(consumed-original<budget&&!pause_requested&&elapsed()<seconds){
    size_t take=std::min(U(chunk_size),budget-(consumed-original));ssize_t got=::read(fd,chunk.data(),take);
    if(got<0&&errno==EINTR)continue;
    need(got>=0,"supplied stream I/O failure","MISSING-EVIDENCE");if(!got){eof=true;break;}
    need(consumed<=UINT64_MAX/8-U(got),"SHA-256 maximum input length","INVALID-PROFILE-SCHEMA");
    SHA256_Update(&ctx,chunk.data(),got);consumed+=got;
    size_t start=0;
    while(start<size_t(got)){
     auto p=(char*)memchr(chunk.data()+start,'\n',got-start);size_t end=p?size_t(p-chunk.data()):got;
     need(pending.size()+end-start<=index.maxline,"row exceeds maximum legal size in this bound model");
     pending.append(chunk.data()+start,end-start);peak=std::max(peak,pending.size());
     if(!p)break;parser.line(pending);pending.clear();start=end+1;
    }
    if(elapsed()-last>=10){std::cerr<<"{\"phase\":\"validate\",\"bytes_consumed\":"<<consumed<<",\"rows\":"<<parser.rows<<"}\n";last=elapsed();}
   }
   if(eof){need(pending.empty(),"truncated row: terminal LF required");parser.finish();need(hash(ctx)==argv[4],"exact consumed input digest mismatch","INVALID-EVIDENCE-DIGEST");complete=true;}
  }catch(Failure&e){code=e.code;detail=e.what();}
  bool resumable=!complete&&code.empty();rusage usage{};getrusage(RUSAGE_SELF,&usage);
  std::string status=complete?"PASS-SUPPLIED-LINK-STREAM":(resumable?"PAUSED":"REJECTED");
  std::cout<<"{\"result\":\""<<status<<"\",\"complete\":"<<(complete?"true":"false")<<",\"eof_observed\":"<<(eof?"true":"false")<<",\"bytes_consumed\":"<<consumed<<",\"consumed_sha256\":\""<<hash(ctx)<<"\",\"complete_stream_sha256\":"<<(complete?"\""+hash(ctx)+"\"":"null")<<",\"rows_validated\":"<<parser.rows<<",\"structural_rows\":"<<parser.structural<<",\"potential_rows\":"<<parser.potential<<",\"expected_structural_rows\":"<<index.edges.size()<<",\"expected_potential_rows\":"<<index.potential<<",\"peak_pending_line_bytes\":"<<peak<<",\"peak_rss_kib\":"<<usage.ru_maxrss<<",\"seconds\":"<<elapsed()<<",\"failure\":";
  if(code.empty())std::cout<<"null";else std::cout<<"{\"code\":\""<<code<<"\",\"detail\":\""<<detail<<"\"}";
  std::cout<<",\"profile_admitted\":false,\"actual_qualification_established\":false,\"state\":";
  // No recovery from a parser error: the current chunk may contain unparsed read-ahead.
  if(!resumable)std::cout<<"null";
  else{
   std::cout<<"{\"offset\":"<<consumed<<",\"rows\":"<<parser.rows<<",\"structural\":"<<parser.structural<<",\"potential\":"<<parser.potential<<",\"header\":"<<parser.header<<",\"have\":"<<parser.have<<",\"peak\":"<<peak<<",\"sha_h\":[";
   for(int i=0;i<8;i++)std::cout<<(i?",":"")<<ctx.h[i];
   std::cout<<"],\"sha_block\":\""<<hexbytes((unsigned char*)ctx.data,ctx.num)<<"\",\"pending\":\""<<hexstr(pending)<<"\",\"previous\":[";
   for(int i=0;i<4;i++)std::cout<<(i?",":"")<<"\""<<hexstr(parser.previous[i])<<"\"";
   std::cout<<"],\"prefix_sha256\":\""<<hash(ctx)<<"\"}";
  }
  std::cout<<"}\n";return complete?0:(resumable?3:2);
 }catch(Failure&e){std::cerr<<e.code<<": "<<e.what()<<"\n";return 4;}
 catch(std::exception&e){std::cerr<<"worker local failure\n";return 4;}
}
