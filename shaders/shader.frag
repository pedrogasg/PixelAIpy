#version 450
layout(location = 0) out vec4 outColor;

layout(location = 0) in vec2 center;
layout(location = 1) in flat float is_agent;
layout(location = 2) in flat float is_wall;
layout(push_constant) uniform Push {
	vec4 color;
    vec2 agent;
    float size;
} push;

const float M_PI = 3.1415926538;

void main() {
    vec4 color = is_agent > .5 ? vec4(1., 1.,1.,1.) : push.color;
    if(is_wall < 0.5){
        float distance = sqrt(dot(center, center));
        outColor = vec4(0.,0.,0.,1.2-distance);
    }else if (center.x < -0.9 || center.x > 0.9 || center.y < -0.9 || center.y > 0.9) {
        float distance = sqrt(dot(center, center));
        outColor = vec4(color.xyz, 1.2-distance);     
    }else{
        outColor = color;
    }
    
}