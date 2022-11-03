#version 450

layout(triangle_strip, max_vertices = 4) out;

layout(points) in;

layout(location = 0) in flat float is_agents[];
layout(location = 1) in flat vec2 current_states[];

layout(location = 0) out vec2 center;
layout(location = 1) out flat float is_agent;
layout(location = 2) out flat vec2 current_state;

layout(push_constant) uniform Push {
	vec4 color;
    vec2 agent;
    vec2 size;
} push;

void main() {
    is_agent = is_agents[0];
    current_state = current_states[0];
    vec4 pos = gl_in[0].gl_Position;
    center = vec2(-1.0, -1.0);
    gl_Position = pos;
    EmitVertex();
    center = vec2(-1.0, 1.0);
    gl_Position = pos;
    gl_Position.y += push.size.y;
    gl_Position = gl_Position;
    EmitVertex();
    center = vec2(1.0, -1.0);
    gl_Position = pos;
    gl_Position.x += push.size.x;
    gl_Position = gl_Position;
    EmitVertex();
    center = vec2(1.0, 1.0);
    gl_Position = pos;
    gl_Position.x += push.size.x;
    gl_Position.y += push.size.y;
    gl_Position = gl_Position;
    EmitVertex();

    EndPrimitive();
}