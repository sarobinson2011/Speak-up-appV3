// Keep everything the same until loadPetitions function, then replace with:

async function loadPetitions() {
  console.log('🔵 Loading petitions...');
  const startTime = performance.now();
  setLoadingPetitions(true);
  
  try {
    const provider = new ethers.JsonRpcProvider(RPC_URL);
    const registry = new ethers.Contract(REGISTRY_ADDRESS, REGISTRY_ABI, provider);
    
    // 1. Get petition count
    const count = await registry.petitionCount();
    console.log(`🔵 Checking ${count} potential petitions...`);
    
    if (count === 0) {
      setPetitions([]);
      return;
    }
    
    // 2. Filter to only EXISTING petitions
    const existingPetitions = [];
    for (let i = 1; i <= Number(count); i++) {
      const petition = await registry.getPetition(i);
      if (petition.exists) {
        existingPetitions.push({
          petitionId: i,  // REAL on-chain ID
          creator: petition.creator,
          createdAt: petition.createdAt,
          metadataURI: petition.metadataURI
        });
      }
    }
    
    console.log(`🔵 Found ${existingPetitions.length} existing petitions (out of ${count} total)`);
    
    if (existingPetitions.length === 0) {
      setPetitions([]);
      return;
    }
    
    // 3. Batch load signatures and metadata for existing petitions only
    const petitionIds = existingPetitions.map(p => p.petitionId);
    
    const [eventArrays, userSignedArray, metadataArray] = await Promise.all([
      // Load signature events
      Promise.all(petitionIds.map(id => {
        const filter = registry.filters.PetitionSigned(id);
        return registry.queryFilter(filter);
      })),
      
      // Check if user signed
      Promise.all(petitionIds.map(id => {
        if (!memberSecret) return false;
        
        const nullifier = ethers.keccak256(
          ethers.solidityPacked(
            ['bytes32', 'uint256', 'string'],
            [memberSecret, id, 'SIGN']
          )
        );
        return registry.hasSignedPetition(id, nullifier);
      })),
      
      // Load metadata from backend
      Promise.all(petitionIds.map(async id => {
        try {
          const response = await fetch(`${BACKEND_URL}/api/petition/${id}`);
          if (response.ok) {
            return await response.json();
          }
          return null;
        } catch (error) {
          console.warn(`Failed to load metadata for petition ${id}:`, error);
          return null;
        }
      }))
    ]);
    
    // 4. Combine all data
    const fullPetitions = existingPetitions.map((petition, idx) => ({
      ...petition,
      signatureCount: eventArrays[idx].length,
      userSigned: userSignedArray[idx],
      metadata: metadataArray[idx]
    }));
    
    setPetitions(fullPetitions);
    
    const elapsed = ((performance.now() - startTime) / 1000).toFixed(2);
    console.log(`🔵 Loaded ${fullPetitions.length} petitions in ${elapsed}s`);
    
  } catch (error) {
    console.error('❌ Error loading petitions:', error);
  } finally {
    setLoadingPetitions(false);
  }
}
