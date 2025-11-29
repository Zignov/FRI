
const adapter = await navigator.gpu.requestAdapter();
const device = await adapter.requestDevice();

console.log(device);


const canvas = document.getElementById('canvas');
const canvasContext = canvas.getContext('webgpu');
const canvasFormat = navigator.gpu.getPreferredCanvasFormat();

const positions = new Float32Array([
    -0.5, -0.5, 0,
     0.5, -0.5, 0,
     0.0,  0.5, 0,
]);

const positionBuffer = device.createBuffer({
    size: positions.byteLength,
    usage: GPUBufferUsage.VERTEX | GPUBufferUsage.COPY_DST,
});

device.queue.writeBuffer(positionBuffer, 0, positions);


const colors = new Float32Array([
    1, 0, 0, 1,
    0, 1, 0, 1,
    0, 0, 1, 1,
]);

const colorBuffer = device.createBuffer({
    size: colors.byteLength,
    usage: GPUBufferUsage.VERTEX | GPUBufferUsage.COPY_DST,
});

device.queue.writeBuffer(colorBuffer, 0, colors);



const positionBufferLayout = {
    arrayStride: 12,
    attributes: [{
        shaderLocation: 0,
        offset: 0,
        format: 'float32x3',
    }]
};

const colorBufferLayout = {
    arrayStride: 16,
    attributes: [{
        shaderLocation: 1,
        offset: 0,
        format: 'float32x4',
    }]
};



const vertices = new Float32Array([
    // position    // color
    -0.5, -0.5, 0,    1, 0, 0, 1,
     0.5, -0.5, 0,    0, 1, 0, 1,
    -0.5,  0.5, 0,    0, 0, 1, 1,
     0.5,  0.5, 0,    1, 1, 0, 1,
]);


const indices = new Uint32Array([
    // 1st triangle
    0, 1, 2,
    // 2nd triangle
    2, 1, 3,
]);

const indexBuffer = device.createBuffer({
    size: indices.byteLength,
    usage: GPUBufferUsage.INDEX | GPUBufferUsage.COPY_DST,
});

device.queue.writeBuffer(indexBuffer, 0, indices);


const vertexBufferLayout = {
    arrayStride: 28,
    attributes: [
        {
            shaderLocation: 0,
            offset: 0,
            format: 'float32x3',
        },
        {
            shaderLocation: 1,
            offset: 12,
            format: 'float32x4',
        },
    ]
};

const vertexBuffer = device.createBuffer({
    size: vertices.byteLength,
    usage: GPUBufferUsage.VERTEX | GPUBufferUsage.COPY_DST,
});
device.queue.writeBuffer(vertexBuffer, 0, vertices);




canvasContext.configure({
    device: device,
    format: canvasFormat
});


const shaderContent = await fetch('./shaders.wgsl').then(response => response.text());
const shaderModule = device.createShaderModule({
    code: shaderContent
});

const pipeline = device.createRenderPipeline({
    layout: 'auto',
    vertex: {
        module: shaderModule,
        entryPoint: 'vertex',
        buffers: [vertexBufferLayout],
    },
    fragment: {
        module: shaderModule,
        entryPoint: 'fragment',
        targets: [{ format: canvasFormat }],
    },
});


const uniformBuffer = device.createBuffer({
    size: 64,
    usage: GPUBufferUsage.UNIFORM | GPUBufferUsage.COPY_DST,
});


const bindGroup = device.createBindGroup({
    layout: pipeline.getBindGroupLayout(0),
    entries: [
        { binding: 0, resource: { buffer: uniformBuffer } },
    ]
});




function update() {
    const time = performance.now() / 1000;
    const radius = 0.5;
    const frequency = 0.5;
    const x = radius * Math.cos(frequency * time * 2 * Math.PI);
    const y = radius * Math.sin(frequency * time * 2 * Math.PI);

    device.queue.writeBuffer(uniformBuffer, 0, new Float32Array([
        1, 0, 0, 0,
        0, 1, 0, 0,
        0, 0, 1, 0,
        x, y, 0, 1,
    ]));
}

function render() {
    const commandEncoder = device.createCommandEncoder();

    const renderPass = commandEncoder.beginRenderPass({
        colorAttachments: [{
            view: canvasContext.getCurrentTexture().createView(),
            loadOp: 'clear',
            clearValue: [0.3, 0.0, 0.8, 1.0],
            storeOp: 'store'
        }]
    });

    renderPass.setPipeline(pipeline);
    renderPass.setBindGroup(0, bindGroup);
    renderPass.setVertexBuffer(0, vertexBuffer);
    renderPass.setIndexBuffer(indexBuffer, 'uint32');
    renderPass.drawIndexed(indices.length);
    renderPass.end();

    const commandBuffer = commandEncoder.finish();
    device.queue.submit([commandBuffer]);
}

function frame() {
    update();
    render();
    requestAnimationFrame(frame);
}

requestAnimationFrame(frame);