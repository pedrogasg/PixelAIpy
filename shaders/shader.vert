#version 450

layout(location = 0) in vec2 position;
layout(location = 1) in vec4 state;

layout(location = 0) out vec4 cellColor;

layout(push_constant) uniform Push {
	vec4 color;
	float size;
} push;

void main() {
	gl_Position = vec4(position, 0.0, 1.0);
	gl_PointSize = 1.0;
	cellColor = push.color;

}