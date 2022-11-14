#version 450

layout(location = 0) in vec4 position;
layout(location = 1) in vec4 state;
layout(location = 0) out flat vec2 current_state;

layout(push_constant) uniform Push {
	vec4 color;
	vec2 agent;
	vec2 size;
} push;

void main() {
	current_state = vec2(0);
	if(state.x == 2){
		current_state.x = 2.;
		gl_Position = vec4(push.agent.x, push.agent.y, 0.0, 1.0);
		gl_PointSize = 1.0;
	} else{
		gl_Position = vec4(position.x, position.y, 0.0, 1.0);
		gl_PointSize = 1.0;
		if(state.x == 1)
			current_state.x = 1.;

		if(state.y == 1)
			current_state.y = 1.;
	}

}