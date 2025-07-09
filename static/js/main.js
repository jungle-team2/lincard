// async function createTextureFromElement(el) {
//   const canvas = await html2canvas(el, { backgroundColor: null });
//   return new THREE.CanvasTexture(canvas);
// }

// async function init() {
//   const scene = new THREE.Scene();
//   const camera = new THREE.PerspectiveCamera(
//     75,
//     window.innerWidth / window.innerHeight,
//     0.1,
//     1000
//   );
//   camera.position.z = 5;

//   console.log(document.getElementById("card"));
//   const texture = await createTextureFromElement(
//     document.getElementById("card")
//   );

//   const geometry = new THREE.BoxGeometry(1, 1, 1); // 박스
//   const material = new THREE.MeshBasicMaterial({ color: texture });
//   const cube = new THREE.Mesh(geometry, material);

//   scene.add(cube);

//   const renderer = new THREE.WebGLRenderer({ alpha: true });
//   renderer.setSize(window.innerWidth, window.innerHeight);
//   document.body.appendChild(renderer.domElement);

//   function animate() {
//     requestAnimationFrame(animate);
//     renderer.render(scene, camera);
//   }
//   animate();

//   const light = new THREE.DirectionalLight(0xffffff, 0.3);
//   light.position.set(5, 5, 5);
//   scene.add(light);

//   document.addEventListener("mousemove", (e) => {
//     const x = (e.clientX / window.innerWidth - 0.5) * 2;
//     const y = (e.clientY / window.innerHeight - 0.5) * 2;
//     cube.rotation.y = x;
//     cube.rotation.x = y;
//   });
// }

// window.addEventListener("DOMContentLoaded", () => {
//   init();
// });
