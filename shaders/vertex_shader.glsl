#version 430

layout (location = 0) in vec4 in_position;

void main() {
    gl_Position = vec4(in_position.xyz, 1.0);
    gl_PointSize = 1.0;  // Set the size of each particle point
}
