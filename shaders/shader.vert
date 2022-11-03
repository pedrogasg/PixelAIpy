#version 450

layout(location = 0) in vec4 position;
layout(location = 1) in vec4 state;
layout(location = 0) out flat float is_agent;
layout(location = 1) out flat vec2 current_state;

layout(push_constant) uniform Push {
	vec4 color;
	vec2 agent;
	vec2 size;
} push;

void main() {
	gl_Position = vec4(position.x, position.y, 0.0, 1.0);
	gl_PointSize = 1.0;

	if(position.w == push.agent.x && position.z == push.agent.y)
		is_agent = 1.;
	else
		is_agent = 0.;
	current_state = vec2(0);
	if(state.x == 1)
		current_state.x = 1.;

	if(state.y == 1)
		current_state.y = 1.;

}