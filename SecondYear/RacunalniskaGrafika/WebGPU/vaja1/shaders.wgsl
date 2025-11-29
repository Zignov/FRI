const positions = array(
    vec3f(-0.5, -0.5, 0.0),
    vec3f(0.5, 0.5, 0.2),
    vec3f(0.5, -0.3, 0.3)
);


const colors = array(
    vec4f(0.7, 0.2, 0.2, 1.0),
    vec4f(0.1, 0.9, 0.7, 1.0),
    vec4f(0.4, 0.4, 0.1, 1.0)
);

struct VertexOutput{
    @builtin(position) position: vec4f, 
    @location(0) color: vec4f
}


@vertex
fn vertex(@builtin(vertex_index) vertexIndex: u32) -> VertexOutput {

    let position = positions[vertexIndex];
    var output: VertexOutput;

    output.position = vec4f(position, 1.0);
    output.color = colors[vertexIndex];
    return output;
}
@fragment
fn fragment(input: VertexOutput) -> @location(0) vec4f{
    let color = input.color;
    return color;
}