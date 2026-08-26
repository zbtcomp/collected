// Global reference for the instanced mesh containing all particles
let instancedMesh;

// Particle system configuration
const particleCount = 200; // Total number of cloud/fog planes to render
const spread = 80;         // The bounding area (cube) size where particles can exist
const data = [];           // Array to store individual particle position data

// Animation modifiers
const localJitter = 0.08;  // Small random offset applied to particles each frame
const driftSpeed = 0.07;   // Base speed for the global wind movement

function init() {
    // Hide the original placeholder mesh so only the instanced particles are visible
    this.visible = false; 

    // Ensure the mesh has a material assigned before proceeding
    if (!this.material) {
        console.error("No material found! Make sure this script is attached to a Mesh.");
        return;
    }
    
    // Clone the material to avoid mutating shared materials across other objects
    const cloudMaterial = this.material.clone(); 

    // Configure material properties specifically for a volumetric fog/cloud look
    cloudMaterial.transparent = true;
    cloudMaterial.opacity = 0.9;             // High opacity to keep the texture visible
    cloudMaterial.depthWrite = false;        // Prevents particles from z-fighting or occluding each other harshly
    cloudMaterial.blending = THREE.NormalBlending; 
    cloudMaterial.side = THREE.DoubleSide;   // Renders the texture on both sides of the plane

    // Create the geometry for a single particle (a 30x30 flat plane)
    const geometry = new THREE.PlaneGeometry(30, 30); 
    
    // Initialize the InstancedMesh which efficiently renders multiple copies of the same geometry
    instancedMesh = new THREE.InstancedMesh(geometry, cloudMaterial, particleCount);
    
    // A dummy Object3D used to calculate and extract transformation matrices for each instance
    const dummy = new THREE.Object3D();

    // Generate initial random positions for all particles
    for (let i = 0; i < particleCount; i++) {
        // Randomize x, y, and z coordinates within the 'spread' bounds
        const x = (Math.random() - 0.5) * spread;
        const y = (Math.random() - 0.5) * spread;
        const z = (Math.random() - 0.5) * spread;
        
        // Store the position data so we can update it in the animation loop
        data.push({ x, y, z });

        // Apply the position to the dummy object, calculate its matrix, and apply it to the specific instance
        dummy.position.set(x, y, z);
        dummy.updateMatrix();
        instancedMesh.setMatrixAt(i, dummy.matrix);
    }

    // Flag the matrix array to be updated on the GPU
    instancedMesh.instanceMatrix.needsUpdate = true;
    
    // Add the newly created particle system to the same parent as the original object
    this.parent.add(instancedMesh);
}

function update(event) {
    // Abort if the instanced mesh hasn't been initialized yet
    if (!instancedMesh) return;
    
    const dummy = new THREE.Object3D();

    // Calculate global wind movement using time and sine/cosine waves for organic drifting
    const time = performance.now() * 0.0003; 
    const windX = Math.sin(time) * driftSpeed;
    const windZ = Math.cos(time * 0.7) * driftSpeed; 
    const windY = Math.sin(time * 0.5) * (driftSpeed * 0.3); // Slower vertical drift

    // Update each particle's position and rotation
    for (let i = 0; i < particleCount; i++) {
        const p = data[i];

        // Apply local chaotic jitter combined with the global wind vectors
        p.x += (Math.random() - 0.5) * localJitter + windX;
        p.y += (Math.random() - 0.5) * localJitter + windY;
        p.z += (Math.random() - 0.5) * localJitter + windZ;

        // Bounding box logic: Wrap particles to the opposite side if they drift too far out of bounds
        const halfSpread = spread / 2;
        if (p.x > halfSpread) p.x = -halfSpread; else if (p.x < -halfSpread) p.x = halfSpread;
        if (p.y > halfSpread) p.y = -halfSpread; else if (p.y < -halfSpread) p.y = halfSpread;
        if (p.z > halfSpread) p.z = -halfSpread; else if (p.z < -halfSpread) p.z = halfSpread;

        // Apply the new position to our dummy object
        dummy.position.set(p.x, p.y, p.z);
        
        // Billboarding effect: Ensure every particle plane always faces the camera (if it exists)
        if (typeof camera !== 'undefined') {
            dummy.lookAt(camera.position);
        }
        
        // Update the transformation matrix for this specific particle instance
        dummy.updateMatrix();
        instancedMesh.setMatrixAt(i, dummy.matrix);
    }
    
    // Notify Three.js that the instance transformations have changed and need re-rendering
    instancedMesh.instanceMatrix.needsUpdate = true;
}