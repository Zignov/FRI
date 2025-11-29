import { quat, mat4 } from './glm.js';
import { Transform } from './Transform.js';
import { Camera } from './Camera.js';
import { Node } from './Node.js';
import {
    getGlobalModelMatrix,
    getGlobalViewMatrix,
    getProjectionMatrix,
} from './SceneUtils.js';

// Initialize WebGPU
const adapter = await navigator.gpu.requestAdapter();
const device = await adapter.requestDevice();
const canvas = document.querySelector('canvas');
const context = canvas.getContext('webgpu');
const format = navigator.gpu.getPreferredCanvasFormat();
context.configure({ device, format });


const imageBitmap = await fetch('image.png')
    .then(response => response.blob())
    .then(blob => createImageBitmap(blob));

const texture = device.createTexture({
    size: [imageBitmap.width, imageBitmap.height],
    format: 'rgba8unorm',
    usage:
        GPUTextureUsage.TEXTURE_BINDING |
        GPUTextureUsage.RENDER_ATTACHMENT |
        GPUTextureUsage.COPY_DST,
});


device.queue.copyExternalImageToTexture(
    { source: imageBitmap },
    { texture },
    [imageBitmap.width, imageBitmap.height]);



const sampler = device.createSampler({
    minFilter: 'linear',
    magFilter: 'linear',
});



// Create vertex buffer
const vertices = new Float32Array([
    // position                // texcoords (u, v)

    -1, -1,  1, 1,            0, 1,
     1, -1,  1, 1,            1, 1,
    -1,  1,  1, 1,            0, 0,
     1,  1,  1, 1,            1, 0,

     1, -1, -1, 1,            0, 1,
    -1, -1, -1, 1,            1, 1,
     1,  1, -1, 1,            0, 0,
    -1,  1, -1, 1,            1, 0,

    -1, -1, -1, 1,            0, 1,
    -1, -1,  1, 1,            1, 1,
    -1,  1, -1, 1,            0, 0,
    -1,  1,  1, 1,            1, 0,

     1, -1,  1, 1,            0, 1,
     1, -1, -1, 1,            1, 1,
     1,  1,  1, 1,            0, 0,
     1,  1, -1, 1,            1, 0,

    -1,  1,  1, 1,            0, 1,
     1,  1,  1, 1,            1, 1,
    -1,  1, -1, 1,            0, 0,
     1,  1, -1, 1,            1, 0,

    -1, -1, -1, 1,            0, 1,
     1, -1, -1, 1,            1, 1,
    -1, -1,  1, 1,            0, 0,
     1, -1,  1, 1,            1, 0,
]);

const vertexBuffer = device.createBuffer({
    size: vertices.byteLength,
    usage: GPUBufferUsage.VERTEX | GPUBufferUsage.COPY_DST,
});

device.queue.writeBuffer(vertexBuffer, 0, vertices);

// Create index buffer
const indices = new Uint32Array([
    // naprej
     0,  1,  2,
     2,  1,  3,

    // nazaj
     4,  5,  6,
     6,  5,  7,

    // levo
     8,  9, 10,
    10,  9, 11,

    // desno
    12, 13, 14,
    14, 13, 15,

    // gor
    16, 17, 18,
    18, 17, 19,

    // dol
    20, 21, 22,
    22, 21, 23,
]);


const indexBuffer = device.createBuffer({
    size: indices.byteLength,
    usage: GPUBufferUsage.INDEX | GPUBufferUsage.COPY_DST,
});

device.queue.writeBuffer(indexBuffer, 0, indices);

// Create the depth texture
const depthTexture = device.createTexture({
    size: [canvas.width, canvas.height],
    format: 'depth24plus',
    usage: GPUTextureUsage.RENDER_ATTACHMENT,
});

// Fetch and compile shaders
const code = await fetch('shader.wgsl').then(response => response.text());
const module = device.createShaderModule({ code });

// Create the pipeline
const vertexBufferLayout = {
    arrayStride: 24,
    attributes: [
        {
            shaderLocation: 0,
            offset: 0,
            format: 'float32x4',
        },
        {
            shaderLocation: 1,
            offset: 16,
            format: 'float32x2',
        },
    ],
};

const pipeline = device.createRenderPipeline({
    vertex: {
        module,
        entryPoint: 'vertex',
        buffers: [vertexBufferLayout],
    },
    fragment: {
        module,
        entryPoint: 'fragment',
        targets: [{ format }],
    },
    depthStencil: {
        depthWriteEnabled: true,
        depthCompare: 'less',
        format: 'depth24plus',
    },
    layout: 'auto',
});

// Create matrix buffer
const uniformBuffer = device.createBuffer({
    size: 16 * 4,
    usage: GPUBufferUsage.UNIFORM | GPUBufferUsage.COPY_DST,
});

// Create the bind group
const bindGroup = device.createBindGroup({
    layout: pipeline.getBindGroupLayout(0),
    entries: [
        { binding: 0, resource: { buffer: uniformBuffer } },
        { binding: 1, resource: texture.createView() },
        { binding: 2, resource: sampler },
    ]
});

// Create the scene
const model = new Node();
model.addComponent(new Transform());
model.addComponent({
    update() {
        const time = performance.now() / 1000;
        const transform = model.getComponentOfType(Transform);
        const rotation = transform.rotation;

        quat.identity(rotation);
        quat.rotateX(rotation, rotation, time * 0.6);
        quat.rotateY(rotation, rotation, time * 0.7);
    }
});

const camera = new Node();
camera.addComponent(new Camera());
camera.addComponent(new Transform({
    translation: [0, 0, 5]
}));

const scene = new Node();
scene.addChild(model);
scene.addChild(camera);

// Update all components
function update() {
    scene.traverse(node => {
        for (const component of node.components) {
            component.update?.();
        }
    });
}

function render() {
    // Get the required matrices
    const modelMatrix = getGlobalModelMatrix(model);
    const viewMatrix = getGlobalViewMatrix(camera);
    const projectionMatrix = getProjectionMatrix(camera);

    // Upload the transformation matrix
    const matrix = mat4.create()
        .multiply(projectionMatrix)
        .multiply(viewMatrix)
        .multiply(modelMatrix);

    device.queue.writeBuffer(uniformBuffer, 0, matrix);

    // Render
    const commandEncoder = device.createCommandEncoder();
    const renderPass = commandEncoder.beginRenderPass({
        colorAttachments: [{
            view: context.getCurrentTexture().createView(),
            loadOp: 'clear',
            clearValue: [0.7, 0.8, 0.9, 1],
            storeOp: 'store',
        }],
        depthStencilAttachment: {
            view: depthTexture.createView(),
            depthClearValue: 1,
            depthLoadOp: 'clear',
            depthStoreOp: 'discard',
        },
    });
    renderPass.setPipeline(pipeline);
    renderPass.setVertexBuffer(0, vertexBuffer);
    renderPass.setIndexBuffer(indexBuffer, 'uint32');
    renderPass.setBindGroup(0, bindGroup);
    renderPass.drawIndexed(indices.length);
    renderPass.end();
    device.queue.submit([commandEncoder.finish()]);
}

function frame() {
    update();
    render();
    requestAnimationFrame(frame);
}

requestAnimationFrame(frame);
