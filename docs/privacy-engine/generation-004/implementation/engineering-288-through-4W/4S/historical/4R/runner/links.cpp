// Shared tested portable SHA state helpers; separate lexical TSV generator.
#define main pairs_engine_main
#include "pairs.cpp"
#undef main
#include <tuple>
const char* LH="link_order\tfrom_token_id\tto_token_id\trelation_order\trelation_class\n";
struct Edge {uint32_t a,b,r;std::string k;};
int main(int argc,char**argv){try{
 if(argc!=7)throw std::runtime_error("links descriptor start-from-rank end-from-rank state engine seconds");
 auto began=std::chrono::steady_clock::now();double limit=std::stod(argv[6]);if(!(limit>0&&limit<=60))throw std::runtime_error("60 second cap");
 std::ifstream in(argv[1]);std::string tag;U n,m,f;in>>tag>>n>>m>>f;if(tag!="LINKS"||n<2||n>UINT32_MAX||f>n)throw std::runtime_error("links descriptor");std::vector<std::string> names(n);for(auto &s:names){in>>s;if(s.empty())throw std::runtime_error("token id");}
 std::vector<int> fixed(n,-1);std::vector<U> fixedids;for(U k=0;k<f;k++){U i;int g;in>>i>>g;if(i>=n||g<0||fixed[i]!=-1)throw std::runtime_error("fixed group");fixed[i]=g;fixedids.push_back(i);}
 std::vector<uint32_t> lex(n),rank(n);for(U i=0;i<n;i++)lex[i]=i;std::sort(lex.begin(),lex.end(),[&](auto a,auto b){return names[a]<names[b];});for(U i=0;i<n;i++){rank[lex[i]]=i;if(i&&names[lex[i]]==names[lex[i-1]])throw std::runtime_error("duplicate id");}
 std::vector<Edge> es;es.reserve(m);for(U k=0;k<m;k++){U a,b,r;std::string kind;in>>a>>b>>r>>kind;if(!in||a>=n||b>=n||r<1||r>999999||kind.empty())throw std::runtime_error("edge descriptor");es.push_back({rank[a],rank[b],uint32_t(r),kind});}std::string extra;if(in>>extra)throw std::runtime_error("trailing descriptor");
 auto less=[](const Edge&a,const Edge&b){return std::tie(a.a,a.b,a.r,a.k)<std::tie(b.a,b.b,b.r,b.k);};std::sort(es.begin(),es.end(),less);es.erase(std::unique(es.begin(),es.end(),[&](const Edge&a,const Edge&b){return !less(a,b)&&!less(b,a);}),es.end());
 U start=std::stoull(argv[2]),end=std::stoull(argv[3]);if(start>=end||end>n)throw std::runtime_error("range");
 std::vector<U> counts(n);for(U i=0;i<n;i++)counts[rank[i]]=n-i-1;for(auto i:fixedids)for(auto j:fixedids)if(i<j&&fixed[i]!=fixed[j])counts[rank[i]]--;for(auto&e:es)counts[e.a]++;
 U ordinal=0,rows=0,bytes=0;for(U i=0;i<start;i++)ordinal+=counts[i];U first_ordinal=ordinal;
 SHA256_CTX cumulative,segment;SHA256_Init(&segment);if(std::string(argv[4])=="INIT"){SHA256_Init(&cumulative);SHA256_Update(&cumulative,LH,strlen(LH));}else cumulative=restore(argv[4]);auto before=state(cumulative);
 std::string buffer;buffer.reserve(8*1024*1024+1024);double last=0;auto checktime=[&](){double sec=std::chrono::duration<double>(std::chrono::steady_clock::now()-began).count();if(sec>limit)throw std::runtime_error("time budget; no commit");if(sec-last>=10){std::cerr<<"{\"rows\":"<<rows<<",\"seconds\":"<<sec<<"}\n";last=sec;}};
 auto flush=[&](){SHA256_Update(&segment,buffer.data(),buffer.size());SHA256_Update(&cumulative,buffer.data(),buffer.size());bytes+=buffer.size();buffer.clear();checktime();};
 auto pad=[](U v){auto s=std::to_string(v);if(s.size()<6)s=std::string(6-s.size(),'0')+s;return s;};
 auto emit=[&](U a,U b,U rel,const std::string&kind){buffer+=pad(++ordinal);buffer+='\t';buffer+=names[lex[a]];buffer+='\t';buffer+=names[lex[b]];buffer+='\t';buffer+=pad(rel);buffer+='\t';buffer+=kind;buffer+='\n';rows++;if(buffer.size()>=8*1024*1024)flush();};
 size_t pos=std::lower_bound(es.begin(),es.end(),Edge{uint32_t(start),0,0,""},less)-es.begin();
 for(U a=start;a<end;a++){
  for(U b=0;b<n;b++){
   auto i=lex[a],j=lex[b];if(i<j&&(fixed[i]<0||fixed[j]<0||fixed[i]==fixed[j]))emit(a,b,0,"EQUALS");
   while(pos<es.size()&&es[pos].a==a&&es[pos].b==b){auto&e=es[pos++];emit(a,b,e.r,e.k);}
  }checktime();
 }flush();U expected=0;for(U i=start;i<end;i++)expected+=counts[i];if(rows!=expected)throw std::runtime_error("independent row-count mismatch");
 double sec=std::chrono::duration<double>(std::chrono::steady_clock::now()-began).count();
 std::cout<<"{\"start\":"<<start<<",\"end\":"<<end<<",\"rows\":"<<rows<<",\"bytes\":"<<bytes<<",\"first_row_ordinal\":"<<first_ordinal+1<<",\"segment_sha256\":\""<<finish(segment)<<"\",\"prefix_sha256\":\""<<finish(cumulative)<<"\",\"state_in\":\""<<before<<"\",\"state_out\":\""<<state(cumulative)<<"\",\"engine\":\"lexical-tsv\",\"seconds\":"<<std::setprecision(12)<<sec<<"}\n";
}catch(std::exception&e){std::cerr<<e.what()<<"\n";return 2;}}
