
const adapter = await navigator.gpu.requestAdapter();
const device = await adapter.requestDevice();

console.log(device);


const canvas = document.getElementById('canvas');
const canvasContext = canvas.getContext('webgpu');
const canvasFormat = navigator.gpu.getPreferredCanvasFormat();

canvasContext.configure({
    device: device,
    format: canvasFormat
});


const shaderContent = await fetch('./shaders.wgsl').then(response => response.text());
const shaderModule = device.createShaderModule({
    code: shaderContent
});

const pipeline = device.createRenderPipeline({
    vertex: {
        module: shaderModule
    },
    fragment: {
        module: shaderModule,
        targets: [{
            format: canvasFormat
        }]
    },
    layout: 'auto'
});

const commandEncoder = device.createCommandEncoder();

const renderPass = commandEncoder.beginRenderPass({
    colorAttachments: [{
        view: canvasContext.getCurrentTexture().createView(),
        loadOp: 'clear',
        clearValue: [0.3, 0, 0.8, 1.0],
        storeOp: 'store'
    }]
});

renderPass.setPipeline(pipeline);
renderPass.draw(3);
renderPass.end();

const commandBuffer = commandEncoder.finish();
device.queue.submit([commandBuffer]);