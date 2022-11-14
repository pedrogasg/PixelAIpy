#version 450
layout(location = 0) out vec4 outColor;

layout(location = 0) in vec2 center;
layout(location = 1) in flat vec2 current_state;
layout(push_constant) uniform Push {
	vec4 color;
    vec2 agent;
    vec2 size;
} push;

const float M_PI = 3.1415926538;

void main() {
    vec4 color = push.color;
    float  d = length( max(abs(center)-.8,0.) );
    if(current_state.x == 1.){
        outColor = vec4(vec3( smoothstep(.1,.15,d)* smoothstep(.1,.9,d)) ,1.0);
    }else if(current_state.y == 1.){   
        outColor = vec4(1.-vec3( smoothstep(.1,.15,d)* smoothstep(.9,.1,d)) ,1.0);
    }
    else{
        outColor = vec4(color.xyz-vec3( smoothstep(.1,.15,d)* smoothstep(.9,.1,d)) ,color.w);
    }
    
}