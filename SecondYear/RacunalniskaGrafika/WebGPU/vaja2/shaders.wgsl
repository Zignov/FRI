@group(0) @binding(0) var<uniform> matrix: mat4x4f;

struct VertexInput {
    @location(0) position : vec3f,
    @location(1) color    : vec4f,
};

struct VertexOutput {
    @builtin(position) position : vec4f,
    @location(0) color          : vec4f,
};

@vertex
fn vertex(input : VertexInput) -> VertexOutput {
    var output : VertexOutput;

    output.position = matrix * vec4(input.position, 1);
    output.color = input.color;

    return output;
}

@fragment
fn fragment(input : VertexOutput) -> @location(0) vec4f {
    return input.color;
}
