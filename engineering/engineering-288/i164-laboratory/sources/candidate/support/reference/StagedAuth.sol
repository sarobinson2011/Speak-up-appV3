// SPDX-License-Identifier: MIT
pragma solidity ^0.8.22;
import './Incremental512.sol';
import './Invocation.sol';
import './ProfileCaps.sol';
import './Incremental256.sol';
import './CarrierContext.sol';
import './Equation25519.sol';
import './LiveExactA.sol';
import './src/lib/libSCL_EIP6565.sol';
// ISOLATED CANDIDATE. Authentication only. No qualified release method or verdict cache.
interface ICleanupRegistry {function consumedU(bytes32 id) external view returns(bool);}
contract StagedAuth {
 using Incremental512 for Incremental512.State;
 using Incremental256 for Incremental256.State;
 enum Status{Unused,Open,Authenticated,Failed,Abandoned,Cleaned}
 address public executor;bytes32 public configuration;uint64 public epoch;
 Status public status;bytes32 public session;bytes32 public messageId;bytes32 public publicKey;bytes32 public r;bytes32 public s;
 bytes32 public u;uint64 public expiry;uint public total;uint public offset;uint public ordinal;bool public zk;
 bytes public bindingBytes;bytes32 public invocationId;bytes public suffix;bytes[] private values;uint public decoded;uint public mode;uint public cursor;uint public nibble;bool public half;
 Incremental512.State private signatureHash;Incremental256.State private identityHash;
 // Candidate vCleanup1. No history or identity is erased by cleanup.
 address public boundRegistry;bytes32 public boundRegistryCode;
 Status public terminalStatus;bytes32 public terminalIdentityHash;bytes32 public terminalSigHi;bytes32 public terminalSigLo;
 event Cleaned(bytes32 indexed session,bytes32 indexed u,Status terminal,bytes32 invocation,bytes32 message);
 event Transition(bytes32 indexed session,Status status,uint offset,uint ordinal,bytes32 detail);
 constructor(bytes32 config){executor=msg.sender;configuration=config;}
 modifier onlyExecutor(){require(msg.sender==executor,'EXECUTOR');_;}
 struct Begin {bytes32 key;bytes32 R;bytes32 S;bytes32 messageHash;uint length;bytes bindings;}
 function begin(Begin calldata b,bytes calldata invocation) external onlyExecutor {
  require(status==Status.Unused,'ONE-LIFETIME-SESSION');require(b.length>=41&&b.length<=1048617,'MESSAGE-BOUND');
  bytes[] memory c=CarrierContext.parse(b.bindings);
  require(CarrierContext.hexword(c[3],40)==uint160(address(this))&&CarrierContext.hexword(c[13],40)==uint160(executor),'ADDRESS-BINDING');
  require(CarrierContext.hexword(c[2],64)==uint(address(this).codehash),'CODE-BINDING');
  require(CarrierContext.dec(c[20])==block.chainid&&CarrierContext.dec(c[12])==epoch,'CHAIN/EPOCH');
  require(CarrierContext.hexword(c[8],64)==uint(configuration),'CONFIGURATION');
  require(CarrierContext.hexword(c[26],64)==uint(sha256(abi.encodePacked(b.key))),'KEY-BINDING');
  expiry=uint64(CarrierContext.dec(c[14]));require(block.timestamp<=expiry,'EXPIRED');u=bytes32(CarrierContext.hexword(c[30],64));
  zk=keccak256(c[18])==keccak256('signPetitionWithZKProof');
  Invocation.validate(invocation,zk);invocationId=sha256(invocation);require(CarrierContext.hexword(c[16],64)==uint(invocationId),'INVOCATION-BINDING');require(b.length<=(zk?21376:41972),'PROFILE-MESSAGE-BOUND');bindingBytes=b.bindings;boundRegistry=address(uint160(CarrierContext.hexword(c[27],40)));boundRegistryCode=bytes32(CarrierContext.hexword(c[28],64));
  // Final LF is included in canonical W(context), not inside the embedded JSON object.
  session=sha256(abi.encodePacked('I164-STAGING-SESSION-1\x00',b.bindings,'\n',b.messageHash,b.key,b.R,b.S,uint64(b.length)));
  suffix=abi.encodePacked(',"bindings":',b.bindings,',"format":"I164-A-STAGED-AUTHORIZED-INPUTS-2"}\n');
  total=b.length;messageId=b.messageHash;publicKey=b.key;r=b.R;s=b.S;status=Status.Open;
  signatureHash.init();signatureHash.update(abi.encodePacked(b.R,b.key));identityHash.init();emit Transition(session,status,0,0,0);
 }
 function prefix() internal pure returns(bytes memory){return bytes('I164-ARCHITECTURE-A-AUTHORIZED-INPUTS-V2\n{"authorized_values":[');}
 function typ(uint i) internal view returns(string memory){
  if(zk){if(i==0||i==15)return 'PE-TSE-UINT';if(i==3||i==5)return 'I164-UINT-PAIR';if(i==4)return 'I164-UINT-PAIR-PAIR';if(i==6)return 'I164-UINT-TRIPLE';if(i==7||i==8)return 'PE-TSE-BOOL3';if(i==17)return 'I164-LIVE-FACTS';}
  else {if(i==0||i==11)return 'PE-TSE-UINT';if(i==2||i==3)return 'PE-TSE-BOOL3';if(i==13)return 'I164-LIVE-FACTS';}
  return 'PE-TSE-BYTES';
 }
 function parse(bytes memory b) internal {
  bytes memory pre=prefix();bytes memory tail=suffix;
  for(uint i;i<b.length;i++){
   bytes1 c=b[i];
   if(mode==0){require(c==pre[cursor++],'PREFIX');if(cursor==pre.length){mode=1;cursor=0;}}
   else if(mode==1){require(c==0x22&&values.length<(zk?19:15),'VALUE-START/COUNT');values.push();mode=2;half=false;}
   else if(mode==2){if(c==0x22){require(!half,'ODD-HEX');bytes memory v=values[values.length-1];ProfileCaps.check(zk,values.length-1,v);mode=3;}
    else {uint n=CarrierContext.nib(uint8(c));if(!half){nibble=n;half=true;}else{require(values[values.length-1].length<ProfileCaps.maximum(zk,values.length-1)&&decoded<524288,'VALUE/ARENA-BOUND');values[values.length-1].push(bytes1(uint8(nibble*16+n)));decoded++;half=false;}}}
   else if(mode==3){if(c==0x2c)mode=1;else{require(c==0x5d&&values.length==(zk?19:15),'VALUE-END/COUNT');mode=4;cursor=0;}}
   else if(mode==4){require(cursor<tail.length&&c==tail[cursor++],'BINDING/FORMAT');if(cursor==tail.length)mode=5;}
   else revert('TRAILING');
  }
 }
 function absorb(bytes calldata b) external {require(msg.sender==address(this),'SELF-ONLY');signatureHash.update(b);identityHash.update(b);parse(b);}
 function append(bytes32 id,uint pos,bytes calldata b) external onlyExecutor returns(bool){
  require(status==Status.Open&&id==session,'SESSION/STATE');require(block.timestamp<=expiry,'EXPIRED');
  require(pos==offset&&b.length==(total-offset<512?total-offset:512)&&b.length>0,'OFFSET/CHUNK');
  try this.absorb(b){offset+=b.length;ordinal++;emit Transition(session,status,offset,ordinal,0);return true;}
  catch(bytes memory reason){status=Status.Failed;emit Transition(session,status,offset,ordinal,keccak256(reason));return false;}
 }
 function finalize() external onlyExecutor returns(bool){
  require(status==Status.Open&&block.timestamp<=expiry,'STATE/EXPIRY');
  // An attempted incomplete finalization is terminal, not a resumable success.
  if(offset!=total||mode!=5||identityHash.finish()!=messageId){status=Status.Failed;emit Transition(session,status,offset,ordinal,keccak256('INCOMPLETE/IDENTITY'));return false;}
  (bytes32 hi,bytes32 lo)=signatureHash.finish();uint256[2] memory w=[uint256(hi),uint256(lo)];uint hh=SCL_EIP6565.Red512Modq(SCL_sha512.Swap512(w));
  bool valid=Equation25519.verify(publicKey,r,s,hh);status=valid?Status.Authenticated:Status.Failed;emit Transition(session,status,offset,ordinal,bytes32(uint(valid?1:0)));return valid;
 }
 function invalidate(bytes32 config) external onlyExecutor {require(status!=Status.Cleaned,"CLEANED-TOMBSTONE");configuration=config;epoch++;if(status==Status.Open||status==Status.Authenticated)status=Status.Abandoned;emit Transition(session,status,offset,ordinal,config);}
 function abandon() external onlyExecutor {require(status==Status.Open||status==Status.Authenticated,'TERMINAL');status=Status.Abandoned;emit Transition(session,status,offset,ordinal,0);}
 function cleanup(bytes32 id) external onlyExecutor returns(bool) {
  require(id==session && id!=bytes32(0),"CLEANUP-SESSION");
  if(status==Status.Cleaned)return false;
  if(status==Status.Authenticated){
   // Frozen pinned registry code owns consumedU; both signing routes set it only
   // after accepted live comparison, atomically with the signing effect.
   require(boundRegistry.code.length>0 && boundRegistry.codehash==boundRegistryCode,"CLEANUP-REGISTRY-CODE");
   require(ICleanupRegistry(boundRegistry).consumedU(u),"CLEANUP-UNCONSUMED");
  } else require(status==Status.Failed || status==Status.Abandoned,"CLEANUP-NOT-TERMINAL");
  terminalStatus=status;terminalIdentityHash=identityHash.finish();
  (terminalSigHi,terminalSigLo)=signatureHash.finish();
  status=Status.Cleaned; // permanent; begin, append, finalize, values and invalidate cannot revive.
  delete values;delete signatureHash;delete identityHash;delete suffix;
  // Keep offset/ordinal/decoded/parser coordinates as terminal evidence, plus
  // exact signed binding bytes (history/profile/cut/issuer), key/R/S and IDs.
  emit Cleaned(session,u,terminalStatus,invocationId,messageId);return true;
 }
 function commitments() external view returns(bytes32,bytes32,bytes32){if(status==Status.Cleaned)return(terminalIdentityHash,terminalSigHi,terminalSigLo);(bytes32 a,bytes32 b)=signatureHash.finish();return(identityHash.finish(),a,b);}
 function authorizedValue(uint i) external view returns(bytes memory){require(status==Status.Authenticated,'NOT-AUTHENTICATED');return values[i];}
 function operationalPermit() external pure returns(bool){return false;}
}
// Separate hash-only boundary harness. Never used as an authorization manager.
contract HashBoundary {
 Incremental512.State private a;Incremental256.State private b;
 constructor(){Incremental512.init(a);Incremental256.init(b);}
 function append(bytes calldata x) external{Incremental512.update(a,x);Incremental256.update(b,x);}
 function hashes() external view returns(bytes32,bytes32,bytes32){(bytes32 x,bytes32 y)=Incremental512.finish(a);return(Incremental256.finish(b),x,y);}
}
