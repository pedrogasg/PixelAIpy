#version 450
layout(location = 0) out vec4 outColor;

layout(location = 0) in vec2 center;

layout(push_constant) uniform Push {
	vec4 color;
    float size;
} push;

const float M_PI = 3.1415926538;

void main() {
    if (center.x < -0.9 || center.x > 0.9 || center.y < -0.9 || center.y > 0.9) {
        float distance = sqrt(dot(center, center));
        outColor = vec4(push.color.xyz, 1.2-distance);     
    }else{
        outColor = push.color;
    }
    
}