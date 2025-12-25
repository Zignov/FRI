import { ResizeSystem } from 'engine/systems/ResizeSystem.js';
import { UpdateSystem } from 'engine/systems/UpdateSystem.js';

import { GLTFLoader } from 'engine/loaders/GLTFLoader.js';

import {
    Camera,
    Entity,
    Transform,
} from 'engine/core/core.js';

import { Renderer } from './Renderer.js';
import { Light } from './Light.js';

const canvas = document.querySelector('canvas');
const renderer = new Renderer(canvas);
await renderer.initialize();

const gltfLoader = new GLTFLoader();
await gltfLoader.load(new URL('./gltf/scena.gltf', import.meta.url));

const scene = gltfLoader.loadScene(gltfLoader.defaultScene);

const camera = scene.find(entity => entity.getComponentOfType(Camera));
const cameraTransform = camera.getComponentOfType(Transform);
cameraTransform.translation = [0, 1.5, 5];
cameraTransform.rotation = [-0.1, -0.1, 0, 1];

const light = new Entity();
light.addComponent(new Transform({
    translation: [3, 3, 3],
}));
light.addComponent(new Light({
    ambient: 0.3,
}));
scene.push(light);


function update(time, dt) {
    for (const entity of scene) {
        for (const component of entity.components) {
            component.update?.(time, dt);
        }
    }
}

function render() {
    renderer.render(scene, camera);
}

function resize({ displaySize: { width, height }}) {
    camera.getComponentOfType(Camera).aspect = width / height;
}

new ResizeSystem({ canvas, resize }).start();
new UpdateSystem({ update, render }).start();