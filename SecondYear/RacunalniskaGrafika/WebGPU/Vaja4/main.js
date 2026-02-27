import { ResizeSystem } from 'engine/systems/ResizeSystem.js';
import { UpdateSystem } from 'engine/systems/UpdateSystem.js';
import { GLTFLoader } from 'engine/loaders/GLTFLoader.js';
import { UnlitRenderer } from 'engine/renderers/UnlitRenderer.js';
import { OrbitController } from 'engine/controllers/OrbitController.js';
import { RotateAnimator } from 'engine/animators/RotateAnimator.js';
import { MyRenderer } from './MyRenderer.js';


import {
    Camera,
    Model,
    Entity,
    Transform,
} from 'engine/core/core.js';

const canvas = document.querySelector('canvas');

function update(time, dt) {}
function render() {}
function resize({ displaySize: { width, height }}) {}

new ResizeSystem({ canvas, resize }).start();
new UpdateSystem({ update, render }).start();

const gltfLoader = new GLTFLoader();
await gltfLoader.load(new URL('./models/monkey/monkey.gltf', import.meta.url));

const scene = gltfLoader.loadScene(gltfLoader.defaultScene);
const camera = scene.find(entity => entity.getComponentOfType(Camera));

function resize({ displaySize: { width, height }}) {
    camera.getComponentOfType(Camera).aspect = width / height;
}


const renderer = new MyRenderer(canvas);
await renderer.initialize();

function render() {
    renderer.render(scene, camera);
}


camera.addComponent(new OrbitController(camera, document.body, {
    distance: 8,
}));

const model = scene.find(node => node.getComponentOfType(Model));
model.addComponent(new RotateAnimator(model, {
    startRotation: [0, 0, 0, 1],
    endRotation: [0.7071, 0, 0.7071, 0],
    duration: 5,
    loop: true,
}));


function update(time, dt) {
    for (const entity of scene) {
         for (const component of entity.components) {
               component.update?.(time, dt);
         }
    }
}



