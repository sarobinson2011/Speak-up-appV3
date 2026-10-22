//! Thin RFC8032 decoder adapter and exact-message streaming CLI.
//! Curve, scalar and SHA-512 operations belong entirely to pinned libraries.
use curve25519_dalek::edwards::CompressedEdwardsY;
use ed25519_dalek::{Signature, VerifyingKey};
use sha2::{Digest, Sha256};
use std::io::{self, Read};

fn unhex<const N: usize>(s: &str) -> Result<[u8; N], String> {
    if s.len() != 2*N || !s.bytes().all(|b| b.is_ascii_digit() || (b'a'..=b'f').contains(&b)) {
        return Err("exact lowercase hex length".into());
    }
    let mut out=[0u8;N];
    for (i,v) in out.iter_mut().enumerate() { *v=u8::from_str_radix(&s[i*2..i*2+2],16).map_err(|_| "hex")?; }
    Ok(out)
}
fn canonical_point(bytes: [u8;32]) -> Result<(),String> {
    let point=CompressedEdwardsY(bytes).decompress().ok_or("point decompression")?;
    if point.compress().to_bytes()!=bytes { return Err("noncanonical point encoding".into()); }
    Ok(())
}
fn run() -> Result<i32,String> {
    let a:Vec<String>=std::env::args().collect();
    if a.len()==3 && a[1]=="encoding" {
        canonical_point(unhex::<32>(&a[2])?)?;
        println!("{{\"status\":\"CANONICAL-POINT\",\"verified\":false}}");return Ok(0);
    }
    if a.len()!=6 || a[1]!="verify" {return Err("usage: verify PUBHEX SIGHEX TOTAL LIMIT | encoding POINTHEX".into());}
    let pk=unhex::<32>(&a[2])?; let sigbytes=unhex::<64>(&a[3])?;
    let mut r=[0u8;32];r.copy_from_slice(&sigbytes[..32]);
    canonical_point(pk)?;canonical_point(r)?;
    let vk=VerifyingKey::from_bytes(&pk).map_err(|_| "public key")?;
    let sig=Signature::from_bytes(&sigbytes);
    // No legacy_compatibility feature: this call enforces canonical S < L.
    let mut verifier=vk.verify_stream(&sig).map_err(|_| "signature scalar")?;
    let total:u64=a[4].parse().map_err(|_| "total length")?;
    let limit:u64=a[5].parse().map_err(|_| "limit length")?;
    if limit>total {return Err("limit exceeds total".into());}
    let mut input=io::stdin().lock();let mut buf=[0u8;65536];let mut h=Sha256::new();let mut count=0u64;
    while count<limit {
        let n=(limit-count).min(buf.len() as u64) as usize;
        let got=input.read(&mut buf[..n]).map_err(|_| "input read")?;
        if got==0 {return Err("truncated transport; verification incomplete".into());}
        verifier.update(&buf[..got]);h.update(&buf[..got]);count+=got as u64;
    }
    if input.read(&mut buf[..1]).map_err(|_| "EOF read")?!=0 {return Err("extra transport bytes".into());}
    let digest=h.finalize().iter().map(|x|format!("{x:02x}")).collect::<String>();
    if count<total {
        println!("{{\"status\":\"PAUSED\",\"bytes\":{count},\"sha256\":\"{digest}\",\"verified\":false}}");return Ok(3);
    }
    verifier.finalize_and_verify().map_err(|_| "signature equation")?;
    println!("{{\"status\":\"VERIFIED-EXACT-MESSAGE\",\"bytes\":{count},\"sha256\":\"{digest}\",\"verified\":true}}");Ok(0)
}
fn main() {
    match run() {Ok(code)=>std::process::exit(code),Err(e)=>{eprintln!("{e}");println!("{{\"status\":\"REJECTED\",\"verified\":false}}");std::process::exit(2);}}
}
