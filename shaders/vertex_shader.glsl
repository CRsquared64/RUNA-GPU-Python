#version 430

layout (location = 0) in vec4 in_position;

uniform mat4 projection;

void main() {
    gl_Position = projection * vec4(in_position.xyz, 1.0);
    gl_PointSize = 0.2;  // Set the size of each particle point
}
