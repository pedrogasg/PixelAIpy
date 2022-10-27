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
        discard;
    }
    float distance = sqrt(dot(center, center));
    float cosDis = (cos(distance * M_PI));
    outColor = vec4(push.color.xyz + 0.1 * cosDis, cosDis);     
}