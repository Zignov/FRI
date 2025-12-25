struct VertexInput {
    @builtin(vertex_index) vertexIndex: u32
}

struct VertexOutput {
    @builtin(position) clipPosition: vec4f,
    @location(0) texcoords: vec2f
}

struct FragmentOutput {
    @location(0) color: vec4f
}


@group(0) @binding(0) var imageTexture: texture_2d<f32>;
@group(0) @binding(1) var imageSampler: sampler;

const pos = array(
    vec2f( 0.0,  0.0),
    vec2f( 1.0,  0.0),
    vec2f( 0.0,  1.0),

    vec2f( 0.0,  1.0),
    vec2f( 1.0,  0.0),
    vec2f( 1.0,  1.0),
);

@vertex
fn vertex(input: VertexInput) -> VertexOutput {
    var output: VertexOutput;
    let xy = pos[input.vertexIndex];
    output.clipPosition = vec4f(xy * 2.0 - 1.0, 0.0, 1.0);
    output.texcoords = vec2f(xy.x, 1.0 - xy.y);
    return output;
}

@fragment
fn fragment(input: VertexOutput) -> FragmentOutput {
    var output: FragmentOutput;
    


    //velikost

    let texSize: vec2<u32> = textureDimensions(imageTexture);
    let texSizeF: vec2<f32> = vec2f(texSize);
    let texelSize: vec2<f32> = 1.0 / texSizeF;


    let uv: vec2<f32> = input.texcoords;


    //sosednji piksli
    let uv_mid: vec2<f32> = uv;
    let uv_right: vec2<f32> = uv + vec2f(texelSize.x, 0.0);
    let uv_down: vec2<f32> = uv + vec2f(0.0, texelSize.y);
    let uv_opposite: vec2<f32> = uv + vec2f(texelSize.x, texelSize.y);


    //barve v rgb

    let c_mid: vec3<f32> = textureSample(imageTexture, imageSampler, uv_mid).rgb;
    let c_right: vec3<f32> = textureSample(imageTexture, imageSampler, uv_right).rgb;
    let c_down: vec3<f32> = textureSample(imageTexture, imageSampler, uv_down).rgb;
    let c_opposite: vec3<f32> = textureSample(imageTexture, imageSampler, uv_opposite).rgb;




    //razlike diagonal

    let diff1: vec3<f32> = c_mid - c_opposite;
    let diff2: vec3<f32> = c_right - c_down;


    //skalarni produtkti

    let s = dot(diff1, diff1) + dot(diff2, diff2);
    

    //preverjanje roba

    let threshold: f32 = 0.01;
    let edge: f32 = select(0.0, 1.0, s > threshold);


    let finalColor: vec3<f32> = mix(c_mid, vec3f(0.0, 0.0, 0.0), edge);

    output.color = vec4f(finalColor, 1.0);
    return output;


}