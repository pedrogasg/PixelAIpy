#version 450

layout(location = 0) in vec2 position;
layout(location = 1) in vec4 state;

layout(location = 0) out flat float is_agent;

layout(push_constant) uniform Push {
	vec4 color;
	float size;
} push;

void main() {
	gl_Position = vec4(position, 0.0, 1.0);
	gl_PointSize = 1.0;
	if(state.x == 5. && state.y == 5.)
		is_agent = 1.;
	else
		is_agent = 0.;

}