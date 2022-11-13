#version 450
layout(location = 0) out vec4 outColor;

layout(location = 0) in vec2 center;
layout(location = 1) in flat float is_agent;
layout(location = 2) in flat vec2 current_state;
layout(push_constant) uniform Push {
	vec4 color;
    vec2 agent;
    vec2 size;
} push;

const float M_PI = 3.1415926538;

void main() {
    vec4 color = is_agent > .5 ? vec4(1., 0.6,0.,1.) : push.color;
    float  d = length( max(abs(center)-.8,0.) );
    if(current_state.x > 0.5 && is_agent < .5){
        outColor = vec4(vec3( smoothstep(.1,.15,d)* smoothstep(.1,.9,d)) ,1.0);
    }else if(current_state.y > 0.5 && is_agent < .5){   
        outColor = vec4(1.-vec3( smoothstep(.1,.15,d)* smoothstep(.9,.1,d)) ,1.0);
    }
    else{
        outColor = vec4(color.xyz-vec3( smoothstep(.1,.15,d)* smoothstep(.9,.1,d)) ,color.w);
    }
    
}