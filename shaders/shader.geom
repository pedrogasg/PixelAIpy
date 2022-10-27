#version 450

layout(triangle_strip, max_vertices = 4) out;

layout(points) in;

layout(location = 0) out vec2 center;

layout(push_constant) uniform Push {
	vec4 color;
    float size;
} push;

void main() {
    vec4 pos = gl_in[0].gl_Position;
    float size = push.size;
    center = vec2(-1.0, -1.0);
    gl_Position = pos;
    EmitVertex();
    center = vec2(-1.0, 1.0);
    gl_Position = pos;
    gl_Position.y += size;
    gl_Position = gl_Position;
    EmitVertex();
    center = vec2(1.0, -1.0);
    gl_Position = pos;
    gl_Position.x += size;
    gl_Position = gl_Position;
    EmitVertex();
    center = vec2(1.0, 1.0);
    gl_Position = pos;
    gl_Position.x += size;
    gl_Position.y += size;
    gl_Position = gl_Position;
    EmitVertex();

    EndPrimitive();
}